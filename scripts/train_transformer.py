from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, matthews_corrcoef
from sklearn.preprocessing import MultiLabelBinarizer

from common import COMMITMENT_LABELS, EMOTION_LABELS, RECOMMENDATION_LABELS, parse_emotions


def load_transformers():
    from datasets import Dataset
    from transformers import (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        DataCollatorWithPadding,
        Trainer,
        TrainingArguments,
    )

    return Dataset, AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding, Trainer, TrainingArguments


def prepare_dataframe(text_path: Path, label_path: Path) -> pd.DataFrame:
    text_df = pd.read_csv(text_path)
    label_df = pd.read_csv(label_path)
    df = text_df.merge(label_df, on="review_uid", suffixes=("", "_label"))
    if df.empty:
        raise ValueError(f"No matching review_uid values for {text_path} and {label_path}")
    return df


def labels_for_task(df: pd.DataFrame, task: str):
    if task == "emotions":
        labels = [label for label in EMOTION_LABELS if label != "none"]
        mlb = MultiLabelBinarizer(classes=labels)
        y = mlb.fit_transform([[label for label in parse_emotions(value) if label != "none"] for value in df["emotions"].fillna("")])
        return y.astype(float), labels, "multi_label_classification"
    if task == "commitment":
        label2id = {label: idx for idx, label in enumerate(COMMITMENT_LABELS)}
        return df["commitment"].fillna("medium").map(label2id).astype(int).values, COMMITMENT_LABELS, "single_label_classification"
    if task == "recommendation":
        label2id = {label: idx for idx, label in enumerate(RECOMMENDATION_LABELS)}
        return df["recommendation"].fillna("neutral").map(label2id).astype(int).values, RECOMMENDATION_LABELS, "single_label_classification"
    raise ValueError(f"Unsupported task: {task}")


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def train(args: argparse.Namespace) -> Dict[str, object]:
    Dataset, AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding, Trainer, TrainingArguments = load_transformers()

    train_df = prepare_dataframe(args.train_texts, args.train_labels)
    eval_df = prepare_dataframe(args.eval_texts, args.eval_labels)
    y_train, labels, problem_type = labels_for_task(train_df, args.task)
    y_eval, _, _ = labels_for_task(eval_df, args.task)

    train_dataset = Dataset.from_dict({"text": train_df["review_text"].astype(str).tolist(), "labels": list(y_train)})
    eval_dataset = Dataset.from_dict({"text": eval_df["review_text"].astype(str).tolist(), "labels": list(y_eval)})

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, max_length=args.max_length)

    train_dataset = train_dataset.map(tokenize, batched=True)
    eval_dataset = eval_dataset.map(tokenize, batched=True)

    id2label = {idx: label for idx, label in enumerate(labels)}
    label2id = {label: idx for idx, label in enumerate(labels)}
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name,
        num_labels=len(labels),
        id2label=id2label,
        label2id=label2id,
        problem_type=problem_type,
    )

    def compute_metrics(eval_pred):
        logits, y_true = eval_pred
        if args.task == "emotions":
            y_pred = (sigmoid(logits) >= args.threshold).astype(int)
            return {
                "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
                "micro_f1": f1_score(y_true, y_pred, average="micro", zero_division=0),
                "sample_f1": f1_score(y_true, y_pred, average="samples", zero_division=0),
            }
        y_pred = np.argmax(logits, axis=1)
        return {
            "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
            "mcc": matthews_corrcoef(y_true, y_pred),
        }

    output_dir = args.output_dir / f"{args.task}_{args.model_name.replace('/', '_')}_lr{args.learning_rate}_ep{args.epochs}"
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        weight_decay=args.weight_decay,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        seed=args.seed,
        report_to=[],
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
        compute_metrics=compute_metrics,
    )
    trainer.train()
    metrics = trainer.evaluate()
    trainer.save_model(str(output_dir / "best_model"))
    tokenizer.save_pretrained(str(output_dir / "best_model"))
    summary = {
        "task": args.task,
        "model_name": args.model_name,
        "learning_rate": args.learning_rate,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "output_dir": str(output_dir),
        "metrics": metrics,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune a transformer classifier for one project task.")
    parser.add_argument("--task", choices=["emotions", "commitment", "recommendation"], required=True)
    parser.add_argument("--model-name", default="roberta-base")
    parser.add_argument("--train-texts", default=Path("data/processed/train.csv"), type=Path)
    parser.add_argument("--eval-texts", default=Path("data/processed/test.csv"), type=Path)
    parser.add_argument("--train-labels", required=True, type=Path)
    parser.add_argument("--eval-labels", required=True, type=Path)
    parser.add_argument("--output-dir", default=Path("models"), type=Path)
    parser.add_argument("--learning-rate", default=2e-5, type=float)
    parser.add_argument("--epochs", default=3, type=float)
    parser.add_argument("--batch-size", default=8, type=int)
    parser.add_argument("--weight-decay", default=0.01, type=float)
    parser.add_argument("--max-length", default=256, type=int)
    parser.add_argument("--threshold", default=0.5, type=float)
    parser.add_argument("--seed", default=20260426, type=int)
    args = parser.parse_args()
    print(json.dumps(train(args), indent=2))


if __name__ == "__main__":
    main()
