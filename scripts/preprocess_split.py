from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from common import length_bucket, normalize_text, quality_issue, word_count


def stratified_take(df: pd.DataFrame, n: int, stratum_col: str, seed: int) -> pd.DataFrame:
    if n >= len(df):
        return df.copy()
    rng_seed = seed
    counts = df[stratum_col].value_counts()
    exact = counts / counts.sum() * n
    quotas = exact.astype(int)
    remainder = n - int(quotas.sum())
    if remainder > 0:
        for key in (exact - quotas).sort_values(ascending=False).index[:remainder]:
            quotas[key] += 1
    sampled_parts = []
    for key, quota in quotas.items():
        if quota <= 0:
            continue
        part = df[df[stratum_col] == key]
        sampled_parts.append(part.sample(n=min(int(quota), len(part)), random_state=rng_seed))
        rng_seed += 1
    sampled = pd.concat(sampled_parts, ignore_index=False)
    if len(sampled) < n:
        remaining = df.drop(index=sampled.index)
        sampled = pd.concat([sampled, remaining.sample(n=n - len(sampled), random_state=seed + 999)], ignore_index=False)
    elif len(sampled) > n:
        sampled = sampled.sample(n=n, random_state=seed + 1000)
    return sampled.sample(frac=1, random_state=seed + 2000)


def split_dataset(input_path: Path, output_dir: Path, seed: int, holdout_size: int, test_size: int, train_size: int) -> dict:
    df = pd.read_csv(input_path)
    df["raw_review_text"] = df["review_text"].fillna("")
    df["review_text"] = df["raw_review_text"].map(normalize_text)
    df["quality_issue"] = df["review_text"].map(quality_issue)
    df = df[~df["quality_issue"]].copy()
    before_dedupe = len(df)
    df = df.drop_duplicates(subset=["review_text"]).copy()
    df["word_count"] = df["review_text"].map(word_count)
    df["length_bucket"] = df["word_count"].map(length_bucket)
    df["rating_str"] = df.get("rating", "").fillna("missing").astype(str)
    df["stratum"] = df["rating_str"] + "__" + df["length_bucket"]

    required = holdout_size + test_size + train_size
    if len(df) < required:
        raise ValueError(f"Need at least {required} clean rows after dedupe; found {len(df)}")

    holdout_df = stratified_take(df, holdout_size, "stratum", seed)
    train_test_df = df.drop(index=holdout_df.index)
    test_df = stratified_take(train_test_df, test_size, "stratum", seed + 1)
    train_pool = train_test_df.drop(index=test_df.index)
    train_df = stratified_take(train_pool, train_size, "stratum", seed + 2)

    output_dir.mkdir(parents=True, exist_ok=True)
    keep_cols = [
        "review_uid",
        "source_file",
        "book_id",
        "user_id_hash",
        "rating",
        "review_text",
        "word_count",
        "length_bucket",
        "date_added",
        "timestamp",
        "has_spoiler",
        "n_votes",
        "n_comments",
    ]
    keep_cols = [col for col in keep_cols if col in df.columns]
    train_df[keep_cols].to_csv(output_dir / "train.csv", index=False)
    test_df[keep_cols].to_csv(output_dir / "test.csv", index=False)
    holdout_df[keep_cols].to_csv(output_dir / "holdout_locked.csv", index=False)

    stats = {
        "input_path": str(input_path),
        "output_dir": str(output_dir),
        "seed": seed,
        "rows_after_quality_filter": int(before_dedupe),
        "duplicates_removed": int(before_dedupe - len(df)),
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "holdout_rows": int(len(holdout_df)),
        "rating_distribution": df["rating_str"].value_counts(dropna=False).to_dict(),
        "length_distribution": df["length_bucket"].value_counts(dropna=False).to_dict(),
        "word_count_summary": df["word_count"].describe().to_dict(),
    }
    (output_dir / "split_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean, deduplicate, and split sampled Goodreads reviews.")
    parser.add_argument("--input", default=Path("data/interim/goodreads_sample_16000.csv"), type=Path)
    parser.add_argument("--output-dir", default=Path("data/processed"), type=Path)
    parser.add_argument("--seed", default=20260426, type=int)
    parser.add_argument("--holdout-size", default=1000, type=int)
    parser.add_argument("--test-size", default=3000, type=int)
    parser.add_argument("--train-size", default=12000, type=int)
    args = parser.parse_args()
    stats = split_dataset(args.input, args.output_dir, args.seed, args.holdout_size, args.test_size, args.train_size)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
