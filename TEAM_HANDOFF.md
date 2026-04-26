# Team Handoff

## Current Status

The repo is ready for teammates to continue from the current Goodreads spoiler-review dataset split.

Important source note: the current parsed file was `/Users/pod/Desktop/goodreads_reviews_spoiler.json`, the UCSD Goodreads spoiler-review subset. This is acceptable for the assignment if we describe it as a Goodreads review source. Do not call it the Young Adult subset unless we later rerun the pipeline with `goodreads_reviews_young_adult.json.gz` or filter by genre metadata.

## What Is Already Done

- Business concept brief drafted.
- Label schema and detailed codebook drafted.
- Data source plan drafted.
- Dataset parsed into exact required split:
  - `data/processed/train.csv`: 12,000 rows
  - `data/processed/test.csv`: 3,000 rows
  - `data/processed/holdout_locked.csv`: 1,000 rows
- Labeling workbook created:
  - `data/labels/holdout_labeling_workbook.xlsx`
- Dictionary baseline created:
  - `data/results/dictionary_baseline_predictions.csv`
- Reproducible scripts and notebooks created.

## Highest-Priority Next Step

Human labeling is now the bottleneck.

1. Open `data/labels/holdout_labeling_workbook.xlsx`.
2. Have all 3 coders label the `Pilot` sheet first.
3. Meet once to resolve confusion.
4. Then have all 3 coders independently label the full `Holdout` sheet.
5. Save/export completed labels back to `data/labels/holdout_human_labeling_sheet.csv`.

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
export GOOGLE_API_KEY="..."
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
  --model gpt-4o-mini
```

Change supplier/model to the selected strategy.

## Fine-Tuning

Use:

`notebooks/04_train_specialist.ipynb`

Run at least four configurations for the A-level target.

## Final Deliverables To Finish

- Fill final metrics into `docs/executive_memo_draft.md`.
- Fill benchmark and fine-tuning tables into `docs/technical_appendix_outline.md`.
- Build the final 20-slide IGNITE deck from `docs/ignite_storyboard.md`.
- Include cost/time/reproducibility comparison.
- Add error analysis and mitigation.

## Recommended Manual-Work Minimization

- Do not manually label train/test. Use the best genAI strategy after benchmarking.
- Human-label only the 1,000 holdout reviews, because the assignment requires it.
- Use the 60-row pilot to reduce disagreement before the full holdout.
- Use the dictionary baseline as a quick additional baseline for the A-level rubric.

