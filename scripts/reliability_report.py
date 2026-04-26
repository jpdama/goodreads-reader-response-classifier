from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
import pandas as pd

from common import COMMITMENT_LABELS, EMOTION_LABELS, RECOMMENDATION_LABELS, parse_emotions


def nominal_alpha(matrix: Sequence[Sequence[object]]) -> float:
    """Krippendorff alpha for nominal labels; rows are items, columns are coders."""
    values = [value for row in matrix for value in row if pd.notna(value) and value != ""]
    if not values:
        return float("nan")
    categories = sorted(set(values))
    n_total = 0
    observed = 0
    for row in matrix:
        clean = [value for value in row if pd.notna(value) and value != ""]
        for a, b in itertools.combinations(clean, 2):
            n_total += 1
            observed += 0 if a == b else 1
    if n_total == 0:
        return float("nan")
    do = observed / n_total
    counts = Counter(values)
    total = sum(counts.values())
    if total <= 1:
        return float("nan")
    de = 1 - sum((counts[cat] / total) ** 2 for cat in categories)
    if de == 0:
        return 1.0 if do == 0 else float("nan")
    return 1 - (do / de)


def percent_agreement(matrix: Sequence[Sequence[object]]) -> float:
    agreed = 0
    total = 0
    for row in matrix:
        clean = [value for value in row if pd.notna(value) and value != ""]
        if len(clean) < 2:
            continue
        total += 1
        if len(set(clean)) == 1:
            agreed += 1
    return agreed / total if total else float("nan")


def majority(values: List[str], default: str) -> tuple[str, bool]:
    clean = [value for value in values if value]
    if not clean:
        return default, True
    counts = Counter(clean)
    top = counts.most_common()
    if len(top) > 1 and top[0][1] == top[1][1]:
        return default, True
    return top[0][0], False


def emotion_consensus(row: pd.Series, coder_count: int) -> tuple[List[str], bool]:
    votes: Dict[str, int] = {label: 0 for label in EMOTION_LABELS if label != "none"}
    any_valid = False
    for idx in range(1, coder_count + 1):
        labels = parse_emotions(row.get(f"coder_{idx}_emotions", ""))
        if labels:
            any_valid = True
        for label in labels:
            if label != "none":
                votes[label] += 1
    consensus = [label for label, count in votes.items() if count >= 2]
    if not consensus:
        consensus = ["none"]
    needs_adjudication = not any_valid
    return consensus, needs_adjudication


def build_report(input_path: Path, output_dir: Path, coder_count: int) -> dict:
    df = pd.read_csv(input_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    report = {"input_path": str(input_path), "coder_count": coder_count, "dimensions": {}}

    for dim, labels, default in [
        ("commitment", COMMITMENT_LABELS, "medium"),
        ("recommendation", RECOMMENDATION_LABELS, "neutral"),
    ]:
        cols = [f"coder_{idx}_{dim}" for idx in range(1, coder_count + 1)]
        matrix = df[cols].fillna("").astype(str).values.tolist()
        report["dimensions"][dim] = {
            "krippendorff_alpha_nominal": nominal_alpha(matrix),
            "percent_full_agreement": percent_agreement(matrix),
        }
        consensus_values = []
        adjudication = []
        for _, row in df.iterrows():
            value, needs_adjudication = majority([str(row.get(col, "")).strip() for col in cols], default)
            if value not in labels:
                value, needs_adjudication = default, True
            consensus_values.append(value)
            adjudication.append(needs_adjudication)
        df[f"consensus_{dim}"] = consensus_values
        df[f"{dim}_needs_adjudication"] = adjudication

    emotion_reports = {}
    for emotion in EMOTION_LABELS:
        binary_matrix = []
        for _, row in df.iterrows():
            binary_matrix.append([
                int(emotion in parse_emotions(row.get(f"coder_{idx}_emotions", "")))
                for idx in range(1, coder_count + 1)
            ])
        emotion_reports[emotion] = {
            "alpha": nominal_alpha(binary_matrix),
            "percent_agreement": percent_agreement(binary_matrix),
        }
    report["dimensions"]["emotions"] = emotion_reports
    consensus_emotions = []
    emotion_adjudication = []
    for _, row in df.iterrows():
        labels, needs_adjudication = emotion_consensus(row, coder_count)
        consensus_emotions.append(",".join(labels))
        emotion_adjudication.append(needs_adjudication)
    df["consensus_emotions"] = consensus_emotions
    df["emotions_needs_adjudication"] = emotion_adjudication
    df["needs_any_adjudication"] = df[
        ["commitment_needs_adjudication", "recommendation_needs_adjudication", "emotions_needs_adjudication"]
    ].any(axis=1)

    df.to_csv(output_dir / "holdout_human_consensus.csv", index=False)
    (output_dir / "human_reliability_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate reliability and consensus for human holdout labels.")
    parser.add_argument("--input", default=Path("data/labels/holdout_human_labeling_sheet.csv"), type=Path)
    parser.add_argument("--output-dir", default=Path("data/results"), type=Path)
    parser.add_argument("--coder-count", default=3, type=int)
    args = parser.parse_args()
    report = build_report(args.input, args.output_dir, args.coder_count)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

