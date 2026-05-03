from __future__ import annotations

import argparse
from pathlib import Path

from genai_benchmark import label_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Label train and test splits with the selected genAI strategy.")
    parser.add_argument("--supplier", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt", default=Path("config/prompt_template.md"), type=Path)
    parser.add_argument("--train-input", default=Path("data/processed/train_no_holdout_overlap.csv"), type=Path)
    parser.add_argument("--test-input", default=Path("data/processed/test_no_holdout_overlap.csv"), type=Path)
    parser.add_argument("--output-dir", default=Path("data/labels"), type=Path)
    parser.add_argument("--limit", default=None, type=int)
    args = parser.parse_args()
    train_out = args.output_dir / f"train_genai_{args.supplier}_{args.model}.csv".replace("/", "_")
    test_out = args.output_dir / f"test_genai_{args.supplier}_{args.model}.csv".replace("/", "_")
    label_file(args.train_input, args.prompt, train_out, args.supplier, args.model, args.limit)
    label_file(args.test_input, args.prompt, test_out, args.supplier, args.model, args.limit)


if __name__ == "__main__":
    main()
