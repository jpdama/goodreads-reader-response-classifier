from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List

import pandas as pd


LEXICON: Dict[str, List[str]] = {
    "joy": ["happy", "fun", "delight", "smile", "excited"],
    "love": ["love", "loved", "adore", "favorite", "obsessed"],
    "surprise": ["surprise", "shocked", "unexpected", "twist", "did not see"],
    "contentment": ["satisfying", "satisfied", "cozy", "comfort", "pleasant"],
    "interest": ["interesting", "intriguing", "engaging", "curious", "hooked"],
    "anger": ["angry", "furious", "rage", "outraged", "blood boil"],
    "frustration": ["frustrating", "annoying", "irritating", "confusing", "impatient"],
    "disappointment": ["disappointed", "letdown", "let down", "wanted to love", "fell flat"],
    "sadness": ["sad", "cried", "cry", "heartbroken", "devastated"],
    "fear": ["scared", "terrified", "creepy", "creeped", "dread"],
    "disgust": ["disgusting", "gross", "repulsive", "revolting", "sick"],
    "boredom": ["boring", "bored", "dull", "tedious", "dragged"],
}


def contains(text: str, cue: str) -> bool:
    return re.search(rf"\b{re.escape(cue)}\b", text, flags=re.IGNORECASE) is not None


def predict(text: str) -> dict:
    lower = text.lower()
    emotions = [label for label, cues in LEXICON.items() if any(cue in lower for cue in cues)]
    if not emotions:
        emotions = ["none"]

    commitment = "medium"
    if any(phrase in lower for phrase in ["next book", "sequel", "continue the series", "read more by", "everything this author"]):
        commitment = "high"
    if any(phrase in lower for phrase in ["never read", "quit the series", "no interest in the sequel", "not read another"]):
        commitment = "low"

    recommendation = "neutral"
    if any(phrase in lower for phrase in ["highly recommend", "must read", "everyone should read", "recommend this"]):
        recommendation = "would_recommend"
    if any(phrase in lower for phrase in ["do not read", "don't read", "would not recommend", "skip it", "waste your time"]):
        recommendation = "would_not"

    return {"emotions": emotions, "commitment": commitment, "recommendation": recommendation}


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a transparent dictionary baseline.")
    parser.add_argument("--input", default=Path("data/processed/holdout_locked.csv"), type=Path)
    parser.add_argument("--output", default=Path("data/results/dictionary_baseline_predictions.csv"), type=Path)
    args = parser.parse_args()
    df = pd.read_csv(args.input)
    rows = []
    for _, row in df.iterrows():
        pred = predict(str(row["review_text"]))
        rows.append({
            "review_uid": row["review_uid"],
            "emotions": ",".join(pred["emotions"]),
            "commitment": pred["commitment"],
            "recommendation": pred["recommendation"],
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(args.output, index=False)
    print(json.dumps({"output": str(args.output), "rows": len(rows)}, indent=2))


if __name__ == "__main__":
    main()

