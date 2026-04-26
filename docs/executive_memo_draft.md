# Executive Memo Draft

To: Underbrush Leadership Team  
From: Capstone Analytics Team  
Subject: Deploying a Reader Response Classifier for Book Review Intelligence  
Date: April 2026

## Recommendation Preview

Underbrush should build a reader response classifier that converts book review text into three operational signals: reader emotions, continuation commitment, and recommendation intent. The project should use human labels on a locked holdout as the evaluation anchor, benchmark genAI labelers as scalable annotators, and fine-tune a specialist transformer for lower-cost recurring deployment.

## Why It Matters

Ratings show whether a book was evaluated positively or negatively, but they do not explain the reaction. Review text shows whether readers were delighted, bored, frustrated, surprised, likely to recommend the book, or likely to continue with the author or series. These signals can improve recommendations, marketing, series investment, and reader retention monitoring.

## Data and Governance

The project uses the UCSD Goodreads Book Graph review data. This source contains naturally occurring reader language and is appropriate for model development. Because the dataset is described as academic-use data and includes anonymized user/review identifiers, raw records should be stored securely, not redistributed publicly, and used only in ways consistent with course and source rules.

## Label Schema

The schema has three parts:

- Emotions: multi-label set of 13 classes including `none`.
- Commitment: low, medium, high.
- Recommendation: would_not, neutral, would_recommend.

The codebook emphasizes conservative labeling, explicit default categories, and clear borderline rules to improve human reliability.

## Evaluation Design

The project locks a 1,000-review holdout before tuning. Each holdout item receives three independent human annotations. GenAI models are benchmarked against the human consensus and reliability statistics. The best genAI strategy labels the 15,000-review train/test set. A specialist transformer is then fine-tuned and evaluated once on the locked holdout.

## Results Placeholder

Final results will be filled after benchmarking and fine-tuning:

| Strategy | Macro F1 | MCC | Alpha vs Human | Cost / 10k | Runtime / 10k | Notes |
|---|---:|---:|---:|---:|---:|---|
| Best genAI single model | TBD | TBD | TBD | TBD | TBD | TBD |
| GenAI ensemble | TBD | TBD | TBD | TBD | TBD | TBD |
| Specialist transformer | TBD | TBD | TBD | TBD | TBD | TBD |
| TF-IDF baseline | TBD | TBD | TBD | TBD | TBD | optional baseline |

## Decision Logic

If a genAI model is substantially more accurate on rare labels and the business use is low-volume, genAI labeling may be preferable. If the specialist model is close in performance and much cheaper at scale, Underbrush should deploy the specialist model with periodic human audits and genAI escalation for uncertain cases.

## Production Controls

Recommended controls:

- Monitor class prevalence drift by month and genre.
- Route low-confidence and rare-label cases to human review.
- Re-benchmark genAI labelers quarterly or when models change.
- Maintain a locked evaluation set for reproducibility.
- Keep raw review data and model outputs governed as academic/private artifacts.

