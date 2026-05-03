# Goodreads Reader Response Classifier

Capstone project package for classifying reader response in book reviews at scale.

## Construct

The classifier identifies three decision-relevant signals in an entire Goodreads-style book review:

1. **Reader emotions**: multi-label affective response to the book.
2. **Continuation commitment**: whether the reader is likely to keep reading the author or series.
3. **Recommendation intent**: whether the reader would recommend the book to another reader.

The business use case is an analytics workflow for a book recommendation, publishing, or reader insights team that needs to convert high-volume review text into structured signals for merchandising, personalization, author/series strategy, and reputation monitoring.

## Project Layout

- `docs/`: concept brief, codebook, data source plan, executive memo draft, appendix outline.
- `config/`: label schema, benchmark model roster, prompt template.
- `scripts/`: reproducible collection, preprocessing, labeling, reliability, benchmarking, and training utilities.
- `data/raw/`: downloaded source files. Do not commit large/raw datasets.
- `data/interim/`: cleaned samples before final split.
- `data/processed/`: locked train/test/holdout splits.
- `data/labels/`: human and genAI label outputs.
- `data/results/`: descriptive stats, benchmark metrics, training summaries.
- `models/`: local model checkpoints. Do not commit large model files.
- `reports/`: generated PDFs and final presentation artifacts.

## Current Dataset State

The current repo includes a parsed working split from `/Users/pod/Desktop/goodreads_reviews_spoiler.json`, the UCSD Goodreads spoiler-review subset. It is a valid Goodreads review-text source for this construct, but it is not the dedicated Young Adult genre subset unless later filtered or rerun with `goodreads_reviews_young_adult.json.gz`.

Current included files:

- `data/processed/train_no_holdout_overlap.csv`: 12,000 reviews, regenerated to avoid overlap with the human-labeled holdout
- `data/processed/test_no_holdout_overlap.csv`: 3,000 reviews, regenerated to avoid overlap with the human-labeled holdout
- `data/processed/holdout_locked.csv`: original 1,000-review holdout
- `data/labels/holdout_labeling_workbook.xlsx`: human labeling workbook
- `data/results/dictionary_baseline_predictions.csv`: automatic baseline predictions
- `data/results/no_holdout_overlap_split_report.json`: verification that regenerated train/test do not overlap the holdout
- `reports/specialist_model.docx`: RoBERTa specialist model results
- `notebooks/03_genai_benchmark_best.ipynb`: sanitized GPT-4.1-mini benchmark and labeling notebook
- `notebooks/04_train_specialist.ipynb`: Colab/local specialist training and holdout evaluation notebook
- `scripts/predict_specialist.py`: inference script for saved RoBERTa task models

Raw source data and model checkpoints are intentionally excluded.

## Final Modeling Recommendation

Use GPT-4o-mini as the best overall genAI labeling strategy because it is inexpensive, reliable, and had no parsing failures. Use RoBERTa as the deployed specialist classifier because it outperformed GPT-4o-mini on the locked holdout for emotions, commitment, and recommendation.

| Task | GPT-4o-mini Macro F1 | RoBERTa Macro F1 |
|---|---:|---:|
| Emotions | 0.394 | 0.406 |
| Commitment | 0.516 | 0.622 |
| Recommendation | 0.563 | 0.700 |

The recommended production design is a hybrid workflow: GPT-4o-mini labels new batches or ambiguous reviews, while RoBERTa handles routine high-volume classification.

## Recommended Execution Order

1. Review `docs/concept_brief.md` and `docs/labeling_codebook.md`.
2. Download one UCSD Goodreads review subset into `data/raw/`.
3. Use `data/processed/train_no_holdout_overlap.csv`, `data/processed/test_no_holdout_overlap.csv`, and `data/processed/holdout_locked.csv` for final modeling.
4. Run `scripts/reliability_report.py` if human labels change.
5. Use `scripts/genai_benchmark.py` to reproduce the genAI benchmark.
6. Use `scripts/genai_label_train_test.py` with GPT-4o-mini for scalable train/test labeling.
7. Use `scripts/train_transformer.py` to reproduce RoBERTa specialist model fine-tuning.
8. Use `scripts/predict_specialist.py` to run saved specialist models on the locked holdout or new review files.
9. Complete the final memo, appendix, and IGNITE deck with the resulting metrics.

## Data Governance Note

The UCSD Goodreads dataset is described by the maintainers as academic-use data and should not be redistributed. Keep raw files, labeled text, and model checkpoints out of public repositories unless your instructor explicitly approves the sharing mechanism.
