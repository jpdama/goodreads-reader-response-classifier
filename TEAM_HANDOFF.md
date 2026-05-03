# Team Handoff

## Current Status

The repo is ready for final submission review from the current Goodreads spoiler-review dataset split.

Important source note: the current parsed file was `/Users/pod/Desktop/goodreads_reviews_spoiler.json`, the UCSD Goodreads spoiler-review subset. This is acceptable for the assignment if we describe it as a Goodreads review source. Do not call it the Young Adult subset unless we later rerun the pipeline with `goodreads_reviews_young_adult.json.gz` or filter by genre metadata.

## What Is Already Done

- Business concept brief completed.
- Label schema and detailed codebook completed.
- Data source plan completed.
- Dataset parsed into exact required split:
  - `data/processed/train_no_holdout_overlap.csv`: 12,000 rows
  - `data/processed/test_no_holdout_overlap.csv`: 3,000 rows
  - `data/processed/holdout_locked.csv`: original 1,000-row holdout
- The holdout has already been human labeled outside this repo as `/Users/pod/Desktop/holdout_real_reviews.csv`; do not replace it.
- The original `train.csv` and `test.csv` had small overlaps with the labeled holdout. Use the `*_no_holdout_overlap.csv` files for all remaining genAI labeling and specialist-model training.
- Labeling workbook created:
  - `data/labels/holdout_labeling_workbook.xlsx`
- Dictionary baseline created:
  - `data/results/dictionary_baseline_predictions.csv`
- Human reliability results created:
  - `data/results/human_reliability_report.json`
  - `data/results/holdout_human_consensus.csv`
- GenAI benchmark and RoBERTa results are summarized in `docs/technical_appendix_outline.md`.
- Reproducible scripts and notebooks created.

## Highest-Priority Next Step

Do a final team read-through of the memo, appendix, and IGNITE deck. The remaining work is presentation polish, not pipeline setup.

## After Human Labels Are Done

Run:

```bash
python scripts/reliability_report.py \
  --input data/labels/holdout_human_labeling_sheet.csv \
  --output-dir data/results \
  --coder-count 3
```

This creates:

- `data/results/holdout_human_consensus.csv`
- `data/results/human_reliability_report.json`

## GenAI Benchmark

Set API keys:

```bash
export OPENAI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
export DEEPSEEK_API_KEY="..."
export XAI_API_KEY="..."
```

Then run the benchmark notebook:

`notebooks/03_genai_benchmark.ipynb`

Minimum required roster is in:

`config/genai_models.yaml`

## Train/Test Labeling

After selecting the best genAI model:

```bash
python scripts/genai_label_train_test.py \
  --supplier OpenAI \
  --model gpt-4o-mini \
  --train-input data/processed/train_no_holdout_overlap.csv \
  --test-input data/processed/test_no_holdout_overlap.csv
```

Change supplier/model to the selected strategy.

## Fine-Tuning

Use:

`notebooks/04_train_specialist.ipynb`

Run at least four configurations for the A-level target.

## Final Deliverables To Finish

- Check `docs/executive_memo_draft.md` for team voice and formatting.
- Check `docs/technical_appendix_outline.md` against the professor's submission checklist.
- Build or finalize the 20-slide IGNITE deck from `docs/ignite_storyboard.md`.
- Confirm the Google Doc appendix charts are visible before submission.

## Recommended Manual-Work Minimization

- Do not manually label train/test. Use the best genAI strategy after benchmarking.
- Human-label only the 1,000 holdout reviews, because the assignment requires it.
- Use the 60-row pilot to reduce disagreement before the full holdout.
- Use the dictionary baseline as a quick additional baseline for the A-level rubric.
