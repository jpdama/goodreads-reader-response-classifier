from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def make_sheet(input_path: Path, output_path: Path, coder_count: int) -> None:
    df = pd.read_csv(input_path)
    sheet = df[["review_uid", "rating", "review_text", "word_count", "length_bucket"]].copy()
    for coder_idx in range(1, coder_count + 1):
        sheet[f"coder_{coder_idx}_emotions"] = ""
        sheet[f"coder_{coder_idx}_commitment"] = ""
        sheet[f"coder_{coder_idx}_recommendation"] = ""
        sheet[f"coder_{coder_idx}_quality_issue"] = ""
        sheet[f"coder_{coder_idx}_notes"] = ""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.to_csv(output_path, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a holdout labeling sheet for independent human coders.")
    parser.add_argument("--input", default=Path("data/processed/holdout_locked.csv"), type=Path)
    parser.add_argument("--output", default=Path("data/labels/holdout_human_labeling_sheet.csv"), type=Path)
    parser.add_argument("--coder-count", default=3, type=int)
    args = parser.parse_args()
    make_sheet(args.input, args.output, args.coder_count)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

