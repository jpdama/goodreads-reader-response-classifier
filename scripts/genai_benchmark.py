from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from common import validate_label_payload


MODEL_PRICES_PER_1M_TOKENS = {
    # Update before final submission using provider pricing pages.
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "claude-3-5-haiku-latest": {"input": 0.80, "output": 4.00},
    "claude-3-7-sonnet-latest": {"input": 3.00, "output": 15.00},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
}


def render_prompt(template: str, review_text: str) -> str:
    return template.replace("{{review_text}}", review_text)


def rough_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def estimate_cost(model: str, prompt: str, output: str) -> float:
    price = MODEL_PRICES_PER_1M_TOKENS.get(model, {"input": 0.0, "output": 0.0})
    return (rough_tokens(prompt) / 1_000_000 * price["input"]) + (rough_tokens(output) / 1_000_000 * price["output"])


def call_openai(model: str, prompt: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model,
        input=prompt,
        temperature=0,
        text={"format": {"type": "json_object"}},
    )
    return response.output_text


def call_anthropic(model: str, prompt: str) -> str:
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model=model,
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if getattr(block, "type", "") == "text")


def call_google(model: str, prompt: str) -> str:
    from google import genai

    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"temperature": 0, "response_mime_type": "application/json"},
    )
    return response.text or "{}"


def call_model(supplier: str, model: str, prompt: str) -> str:
    supplier_lower = supplier.lower()
    if supplier_lower == "openai":
        return call_openai(model, prompt)
    if supplier_lower == "anthropic":
        return call_anthropic(model, prompt)
    if supplier_lower == "google":
        return call_google(model, prompt)
    raise ValueError(f"Unsupported supplier: {supplier}")


def label_file(input_path: Path, prompt_path: Path, output_path: Path, supplier: str, model: str, limit: int | None) -> Dict[str, Any]:
    df = pd.read_csv(input_path)
    if limit:
        df = df.head(limit).copy()
    template = prompt_path.read_text(encoding="utf-8")
    rows: List[Dict[str, Any]] = []
    start_all = time.perf_counter()
    failures = 0
    total_cost = 0.0

    for idx, row in df.iterrows():
        prompt = render_prompt(template, str(row["review_text"]))
        start = time.perf_counter()
        raw_output = ""
        parsed: Dict[str, Any]
        try:
            raw_output = call_model(supplier, model, prompt)
            parsed = validate_label_payload(json.loads(raw_output))
        except Exception as exc:
            failures += 1
            parsed = validate_label_payload({"emotions": ["none"], "commitment": "medium", "recommendation": "neutral", "quality_issue": True, "rationale": str(exc)})
        elapsed = time.perf_counter() - start
        cost = estimate_cost(model, prompt, raw_output)
        total_cost += cost
        rows.append({
            "review_uid": row["review_uid"],
            "supplier": supplier,
            "model": model,
            "emotions": ",".join(parsed["emotions"]),
            "commitment": parsed["commitment"],
            "recommendation": parsed["recommendation"],
            "quality_issue": parsed["quality_issue"],
            "rationale": parsed["rationale"],
            "runtime_seconds": elapsed,
            "estimated_cost_usd": cost,
        })
        if (idx + 1) % 50 == 0:
            print(f"{supplier}/{model}: labeled {idx + 1} rows")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_path, index=False)
    summary = {
        "supplier": supplier,
        "model": model,
        "input_path": str(input_path),
        "output_path": str(output_path),
        "rows": len(rows),
        "parse_or_api_failures": failures,
        "total_runtime_seconds": time.perf_counter() - start_all,
        "estimated_total_cost_usd": total_cost,
    }
    output_path.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one genAI model against a labeled or unlabeled review file.")
    parser.add_argument("--input", default=Path("data/processed/holdout_locked.csv"), type=Path)
    parser.add_argument("--prompt", default=Path("config/prompt_template.md"), type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--supplier", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--limit", default=None, type=int)
    args = parser.parse_args()
    summary = label_file(args.input, args.prompt, args.output, args.supplier, args.model, args.limit)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

