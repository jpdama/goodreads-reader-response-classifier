# Dataset Run Report

## Current Parsed Source

Source file parsed:

`/Users/pod/Desktop/goodreads_reviews_spoiler.json`

This file is the UCSD Goodreads spoiler-review JSONL file. It stores each record as one JSON object per line with review text split across `review_sentences`. The parser now flattens those sentence lists into one full-review text per record.

Important caveat: this file is **not the dedicated Young Adult genre subset** by itself. If the final project must explicitly be Young Adult, use `goodreads_reviews_young_adult.json.gz` or join these review `book_id` values to Goodreads book/genre metadata and filter to YA. The current files are still valid Goodreads review-text artifacts for the pipeline, but the write-up should not call them Young Adult unless that genre filtering is completed.

## Parse Summary

Parsed on: 2026-04-26  
Sampling seed: `20260426`

Raw records scanned: `1,378,033`  
Usable records before sampling: `1,373,010`  
Sample requested: `16,200`  
Sample written: `16,200`

The sample was stratified by rating and review length bucket. The extra 200 rows were collected so that exact target sizes remained possible after duplicate removal.

## Cleaning and Split Summary

Rows after quality filter: `16,200`  
Duplicate reviews removed: `83`  
Rows available after dedupe: `16,117`

Final locked files:

- `data/processed/train.csv`: `12,000` rows
- `data/processed/test.csv`: `3,000` rows
- `data/processed/holdout_locked.csv`: `1,000` rows

This satisfies the assignment target of 15,000 train/test texts plus a 1,000-text locked holdout.

## Rating Distribution After Cleaning

| Rating | Count |
|---:|---:|
| 0 / missing | 2,685 |
| 1 | 2,695 |
| 2 | 2,687 |
| 3 | 2,683 |
| 4 | 2,676 |
| 5 | 2,691 |

## Length Distribution After Cleaning

| Length Bucket | Count |
|---|---:|
| short | 5,321 |
| medium | 5,398 |
| long | 5,398 |

## Word Count Summary

| Statistic | Value |
|---|---:|
| Mean | 162.2 |
| Std. dev. | 221.6 |
| Min | 3 |
| 25th percentile | 22 |
| Median | 74 |
| 75th percentile | 214 |
| Max | 2,503 |

## Manual Work Minimization

Created artifacts:

- `data/labels/holdout_labeling_workbook.xlsx`: Excel workbook with instructions, pilot sheet, holdout sheet, coder columns, dropdowns, frozen panes, and wrapped review text.
- `data/labels/holdout_human_labeling_sheet.csv`: script-friendly labeling CSV.
- `data/results/dictionary_baseline_predictions.csv`: automatic dictionary baseline for comparison, not a replacement for human holdout labels.

Recommended human workflow:

1. Three coders label only the 60-row `Pilot` sheet first.
2. Meet once to resolve codebook confusion.
3. Then all three coders independently label the `Holdout` sheet.
4. Export/save the completed workbook as CSV if needed, then run `scripts/reliability_report.py`.

