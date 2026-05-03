# Benchmarking and Evaluation Plan

## Holdout Discipline

The 1,000-review holdout is locked before genAI prompt tuning and specialist model training. It is used for:

- Human reliability measurement.
- Final genAI model comparison.
- Final specialist model evaluation.
- Final genAI-versus-specialist recommendation.

Do not repeatedly tune prompts or hyperparameters on the holdout. Use a small pilot set from training data for prompt debugging.

## Human Labels

Each holdout item receives three independent human labels:

- Emotions: multi-label set.
- Commitment: one of low, medium, high.
- Recommendation: one of would_not, neutral, would_recommend.

Report:

- Krippendorff's alpha per dimension.
- Percent agreement per dimension.
- Label prevalence.
- Common disagreement patterns.
- Consensus procedure.

## GenAI Benchmark

Benchmark at least six models from at least three suppliers. The final roster in `config/genai_models.yaml` uses OpenAI, Anthropic, DeepSeek, and xAI.

Controls:

- Same codebook.
- Same prompt structure.
- Temperature 0 where supported.
- JSON-only response.
- Same review order or logged random seed.
- Retry and parse-failure policy documented.

Metrics:

- Macro F1.
- Per-class F1.
- MCC.
- AUC when class probabilities or confidence scores are available.
- Krippendorff's alpha against human labels.
- Runtime.
- Estimated cost.
- Parse failure rate.

For emotions, evaluate both:

- Multi-label exact match and sample-level F1.
- Binary one-vs-rest metrics per emotion.

## Specialist Model

Fine-tune at least one pretrained transformer such as RoBERTa. Because this is a multi-task construct, use one of two defensible approaches:

1. Train separate classifiers: one multi-label emotion model plus one commitment model plus one recommendation model.
2. Train one shared encoder with separate task heads.

The first approach is simpler and more reproducible for a capstone.

Minimum experiment grid:

| Experiment | Model | Learning Rate | Epochs | Notes |
|---|---:|---:|---:|---|
| E1 | distilroberta-base | 2e-5 | 3 | fast baseline |
| E2 | roberta-base | 2e-5 | 3 | main baseline |
| E3 | roberta-base | 1e-5 | 4 | lower learning rate |
| E4 | roberta-base | 3e-5 | 3 | higher learning rate |

Optional A-level additions:

- TF-IDF + logistic regression baseline.
- Dictionary baseline using codebook cues.
- Class weighting or focal loss for rare labels.
- Threshold tuning for emotion labels using validation data only.
- Error analysis by rating, length, genre, and rare emotion.

## Final Recommendation Criteria

The recommendation should answer:

- Which strategy performs best on the locked holdout?
- Which strategy is cheapest per 10,000 reviews?
- Which is fastest at realistic batch size?
- Which is most reproducible?
- Which failure modes are acceptable for the business decision?
- What monitoring and human review should remain in production?
