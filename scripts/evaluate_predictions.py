from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import pandas as pd
from sklearn.metrics import f1_score, matthews_corrcoef, precision_recall_fscore_support
from sklearn.preprocessing import MultiLabelBinarizer

from common import COMMITMENT_LABELS, EMOTION_LABELS, RECOMMENDATION_LABELS, parse_emotions


def single_label_metrics(y_true: List[str], y_pred: List[str], labels: List[str]) -> Dict[str, object]:
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=labels,
        zero_division=0,
    )
    return {
        "macro_f1": f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "per_class": {
            label: {
                "precision": float(precision[idx]),
                "recall": float(recall[idx]),
                "f1": float(f1[idx]),
                "support": int(support[idx]),
            }
            for idx, label in enumerate(labels)
        },
    }


def emotion_metrics(y_true_raw: List[str], y_pred_raw: List[str]) -> Dict[str, object]:
    labels = [label for label in EMOTION_LABELS if label != "none"]
    mlb = MultiLabelBinarizer(classes=labels)
    y_true = mlb.fit_transform([[label for label in parse_emotions(value) if label != "none"] for value in y_true_raw])
    y_pred = mlb.transform([[label for label in parse_emotions(value) if label != "none"] for value in y_pred_raw])
    per_label = {}
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true,
        y_pred,
        average=None,
        zero_division=0,
    )
    for idx, label in enumerate(labels):
        per_label[label] = {
            "precision": float(precision[idx]),
            "recall": float(recall[idx]),
            "f1": float(f1[idx]),
            "support": int(support[idx]),
        }
    return {
        "sample_f1": f1_score(y_true, y_pred, average="samples", zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "micro_f1": f1_score(y_true, y_pred, average="micro", zero_division=0),
        "exact_match": float((y_true == y_pred).all(axis=1).mean()),
        "per_class": per_label,
    }


def evaluate(gold_path: Path, pred_path: Path, output_path: Path) -> dict:
    gold = pd.read_csv(gold_path)
    pred = pd.read_csv(pred_path)
    df = gold.merge(pred, on="review_uid", suffixes=("_gold", "_pred"))
    if df.empty:
        raise ValueError("No overlapping review_uid values between gold and prediction files.")

    results = {
        "gold_path": str(gold_path),
        "prediction_path": str(pred_path),
        "n_matched": int(len(df)),
        "emotions": emotion_metrics(df["consensus_emotions"].fillna("").tolist(), df["emotions"].fillna("").tolist()),
        "commitment": single_label_metrics(
            df["consensus_commitment"].fillna("medium").tolist(),
            df["commitment"].fillna("medium").tolist(),
            COMMITMENT_LABELS,
        ),
        "recommendation": single_label_metrics(
            df["consensus_recommendation"].fillna("neutral").tolist(),
            df["recommendation"].fillna("neutral").tolist(),
            RECOMMENDATION_LABELS,
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate model predictions against human consensus labels.")
    parser.add_argument("--gold", default=Path("data/results/holdout_human_consensus.csv"), type=Path)
    parser.add_argument("--pred", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(evaluate(args.gold, args.pred, args.output), indent=2))


if __name__ == "__main__":
    main()

