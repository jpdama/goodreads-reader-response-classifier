from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

from common import extract_review_text, length_bucket, normalize_text, quality_issue, read_jsonl_gz, word_count, write_csv


def stable_id(row: Dict[str, Any]) -> str:
    raw = row.get("review_id") or f"{row.get('user_id','')}:{row.get('book_id','')}:{row.get('review_text','')[:80]}"
    return hashlib.sha1(str(raw).encode("utf-8")).hexdigest()[:16]


def reservoir_add(bucket: List[Dict[str, Any]], row: Dict[str, Any], limit: int, seen: int, rng: random.Random) -> None:
    if len(bucket) < limit:
        bucket.append(row)
        return
    idx = rng.randint(0, seen - 1)
    if idx < limit:
        bucket[idx] = row


def collect(input_path: Path, output_path: Path, sample_size: int, seed: int, per_stratum_cap: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    buckets: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    seen_by_bucket: Dict[str, int] = defaultdict(int)
    total_seen = 0
    total_usable = 0

    for raw in read_jsonl_gz(input_path):
        total_seen += 1
        text = normalize_text(extract_review_text(raw))
        if quality_issue(text):
            continue
        rating = raw.get("rating", "")
        wc = word_count(text)
        stratum = f"rating_{rating or 'missing'}__{length_bucket(wc)}"
        total_usable += 1
        row = {
            "review_uid": stable_id(raw),
            "source_file": input_path.name,
            "book_id": raw.get("book_id", ""),
            "user_id_hash": hashlib.sha1(str(raw.get("user_id", "")).encode("utf-8")).hexdigest()[:16],
            "rating": rating,
            "review_text": text,
            "word_count": wc,
            "length_bucket": length_bucket(wc),
            "date_added": raw.get("date_added", ""),
            "timestamp": raw.get("timestamp", ""),
            "has_spoiler": raw.get("has_spoiler", ""),
            "n_votes": raw.get("n_votes", ""),
            "n_comments": raw.get("n_comments", ""),
        }
        seen_by_bucket[stratum] += 1
        reservoir_add(buckets[stratum], row, per_stratum_cap, seen_by_bucket[stratum], rng)

    strata = sorted(buckets)
    base_quota = max(1, sample_size // max(1, len(strata)))
    selected: List[Dict[str, Any]] = []

    for stratum in strata:
        candidates = buckets[stratum]
        rng.shuffle(candidates)
        selected.extend(candidates[:base_quota])

    if len(selected) < sample_size:
        leftovers = []
        selected_ids = {row["review_uid"] for row in selected}
        for rows in buckets.values():
            leftovers.extend([row for row in rows if row["review_uid"] not in selected_ids])
        rng.shuffle(leftovers)
        selected.extend(leftovers[: sample_size - len(selected)])

    rng.shuffle(selected)
    selected = selected[:sample_size]

    fieldnames = [
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
    write_csv(output_path, selected, fieldnames)
    stats = {
        "input_path": str(input_path),
        "output_path": str(output_path),
        "seed": seed,
        "sample_size_requested": sample_size,
        "sample_size_written": len(selected),
        "total_records_seen": total_seen,
        "total_usable_records": total_usable,
        "strata": {key: {"seen": seen_by_bucket[key], "reservoir": len(buckets[key])} for key in strata},
    }
    output_path.with_suffix(".stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Sample UCSD Goodreads reviews into a 16k project dataset.")
    parser.add_argument("--input", required=True, type=Path, help="Path to a UCSD Goodreads reviews .json.gz file.")
    parser.add_argument("--output", default=Path("data/interim/goodreads_sample_16000.csv"), type=Path)
    parser.add_argument("--sample-size", default=16000, type=int)
    parser.add_argument("--seed", default=20260426, type=int)
    parser.add_argument("--per-stratum-cap", default=2500, type=int)
    args = parser.parse_args()
    stats = collect(args.input, args.output, args.sample_size, args.seed, args.per_stratum_cap)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
