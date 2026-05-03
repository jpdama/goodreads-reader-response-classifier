from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import pandas as pd
import torch


def load_transformers():
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    return AutoModelForSequenceClassification, AutoTokenizer


def predict_multilabel(model_path: Path, texts: List[str], threshold: float, batch_size: int, max_length: int, device: str) -> List[str]:
    AutoModelForSequenceClassification, AutoTokenizer = load_transformers()
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)
    model.eval()

    id2label = {int(k): v for k, v in model.config.id2label.items()}
    predictions: List[str] = []

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        inputs = tokenizer(
            batch,
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors="pt",
        ).to(device)

        with torch.no_grad():
            logits = model(**inputs).logits
            probs = torch.sigmoid(logits).cpu().numpy()

        for row in probs:
            labels = [id2label[i] for i, prob in enumerate(row) if prob >= threshold]
            predictions.append(",".join(labels or ["none"]))

    return predictions


def predict_singlelabel(model_path: Path, texts: List[str], batch_size: int, max_length: int, device: str) -> List[str]:
    AutoModelForSequenceClassification, AutoTokenizer = load_transformers()
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)
    model.eval()

    id2label = {int(k): v for k, v in model.config.id2label.items()}
    predictions: List[str] = []

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        inputs = tokenizer(
            batch,
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors="pt",
        ).to(device)

        with torch.no_grad():
            logits = model(**inputs).logits
            pred_ids = torch.argmax(logits, dim=1).cpu().numpy()

        predictions.extend([id2label[int(i)] for i in pred_ids])

    return predictions


def main() -> None:
    parser = argparse.ArgumentParser(description="Run saved specialist RoBERTa classifiers on a review CSV.")
    parser.add_argument("--input", default=Path("data/processed/holdout_locked.csv"), type=Path)
    parser.add_argument("--output", default=Path("data/results/holdout_roberta_config3_predictions.csv"), type=Path)
    parser.add_argument("--emotion-model", required=True, type=Path)
    parser.add_argument("--commitment-model", required=True, type=Path)
    parser.add_argument("--recommendation-model", required=True, type=Path)
    parser.add_argument("--text-column", default="review_text")
    parser.add_argument("--id-column", default="review_uid")
    parser.add_argument("--threshold", default=0.4, type=float)
    parser.add_argument("--batch-size", default=16, type=int)
    parser.add_argument("--max-length", default=512, type=int)
    parser.add_argument("--device", default=None)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    if args.text_column not in df.columns:
        raise ValueError(f"Missing text column: {args.text_column}")
    if args.id_column not in df.columns:
        raise ValueError(f"Missing id column: {args.id_column}")

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    texts = df[args.text_column].astype(str).tolist()

    predictions = pd.DataFrame(
        {
            args.id_column: df[args.id_column],
            "emotions": predict_multilabel(args.emotion_model, texts, args.threshold, args.batch_size, args.max_length, device),
            "commitment": predict_singlelabel(args.commitment_model, texts, args.batch_size, args.max_length, device),
            "recommendation": predict_singlelabel(args.recommendation_model, texts, args.batch_size, args.max_length, device),
        }
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(args.output, index=False)
    print(f"Wrote {len(predictions)} predictions to {args.output}")


if __name__ == "__main__":
    main()
