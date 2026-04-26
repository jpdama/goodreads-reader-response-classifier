from __future__ import annotations

import csv
import gzip
import html
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List


EMOTION_LABELS = [
    "joy",
    "love",
    "surprise",
    "contentment",
    "interest",
    "anger",
    "frustration",
    "disappointment",
    "sadness",
    "fear",
    "disgust",
    "boredom",
    "none",
]

COMMITMENT_LABELS = ["low", "medium", "high"]
RECOMMENDATION_LABELS = ["would_not", "neutral", "would_recommend"]


def read_jsonl_gz(path: Path) -> Iterator[Dict[str, Any]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def extract_review_text(row: Dict[str, Any]) -> str:
    if row.get("review_text"):
        return str(row.get("review_text", ""))
    sentences = row.get("review_sentences")
    if isinstance(sentences, list):
        parts = []
        for item in sentences:
            if isinstance(item, list) and len(item) >= 2:
                parts.append(str(item[1]))
            elif isinstance(item, str):
                parts.append(item)
        return " ".join(parts)
    return ""


def normalize_text(text: str) -> str:
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text or ""))


def length_bucket(count: int) -> str:
    if count < 30:
        return "short"
    if count < 150:
        return "medium"
    return "long"


def quality_issue(text: str) -> bool:
    if not text or word_count(text) < 3:
        return True
    alpha = sum(ch.isalpha() for ch in text)
    return alpha < max(4, len(text) * 0.25)


def write_csv(path: Path, rows: Iterable[Dict[str, Any]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def read_csv_dicts(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_emotions(value: str) -> List[str]:
    if value is None:
        return []
    raw = str(value).replace(";", ",").replace("|", ",")
    labels = [part.strip().lower() for part in raw.split(",") if part.strip()]
    return [label for label in labels if label in EMOTION_LABELS]


def validate_label_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    emotions = payload.get("emotions", ["none"])
    if isinstance(emotions, str):
        emotions = parse_emotions(emotions)
    emotions = [str(label).strip().lower() for label in emotions if str(label).strip().lower() in EMOTION_LABELS]
    if not emotions:
        emotions = ["none"]
    if "none" in emotions and len(emotions) > 1:
        emotions = [label for label in emotions if label != "none"]

    commitment = str(payload.get("commitment", "medium")).strip().lower()
    if commitment not in COMMITMENT_LABELS:
        commitment = "medium"

    recommendation = str(payload.get("recommendation", "neutral")).strip().lower()
    if recommendation not in RECOMMENDATION_LABELS:
        recommendation = "neutral"

    return {
        "emotions": emotions,
        "commitment": commitment,
        "recommendation": recommendation,
        "quality_issue": bool(payload.get("quality_issue", False)),
        "rationale": str(payload.get("rationale", ""))[:500],
    }
