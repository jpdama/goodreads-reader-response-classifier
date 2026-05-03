# Executive Memo

To: Underbrush Leadership Team  
From: Team 9 Capstone Analytics Team  
Subject: Deploying an Emotion-Based Reader Response Classifier  
Date: May 2026

## Recommendation

Underbrush should use a hybrid labeling and deployment strategy. GPT-4o-mini is the best overall genAI labeling choice because it is inexpensive, reliable, and had no parsing failures in our benchmark. RoBERTa should be the main deployed classifier after training because it performed better than GPT-4o-mini on the locked human-labeled holdout across emotions, commitment, and recommendation.

In practice, Underbrush should use GPT-4o-mini to label large review batches and support periodic relabeling, then use the RoBERTa specialist model for repeated high-volume classification. Human review should be reserved for rare emotions, low-confidence cases, and business-critical reviews.

## Why It Matters

Ratings show whether a book was evaluated positively or negatively, but they do not explain the emotional experience behind the rating. Two readers can give a book four stars for very different reasons. One reader may find it comforting and enjoyable, while another may find it sad, intense, or emotionally difficult but still meaningful.

Emotion-based reader response gives Underbrush a more specific recommendation signal than ratings alone. Instead of only knowing that a reader liked a book, Underbrush can understand whether the reader found it comforting, exciting, heartbreaking, frustrating, surprising, or meaningful.

## Data and Governance

The project uses the UCSD Book Graph / Goodreads review dataset. The final modeling data includes 12,000 training reviews, 3,000 test reviews, and a locked 1,000-review holdout set. After the holdout was human labeled, train and test were regenerated to remove overlapping review IDs and duplicate normalized review text. The final modeling files are `train_no_holdout_overlap.csv`, `test_no_holdout_overlap.csv`, and `holdout_locked.csv`.

Because the dataset is academic-use review data with anonymized identifiers, raw records should not be redistributed publicly. The classifier should be used to understand aggregate reader response rather than to profile individual users.

## Label Schema

The schema includes multi-label emotions, commitment, and recommendation. Emotion labels include joy, love, surprise, contentment, interest, anger, frustration, disappointment, sadness, fear, disgust, boredom, and none. Commitment is labeled as low, medium, or high. Recommendation is labeled as would_not, neutral, or would_recommend. The project also tracks book quality issues separately from data quality problems.

## Human Labeling

The 1,000-review holdout set was labeled by three human coders and used as the evaluation anchor. Human agreement was measured using Krippendorff’s alpha and percent full agreement. Agreement was low to moderate, with Krippendorff’s alpha of 0.194 for commitment and 0.313 for recommendation. For emotions, agreement varied by label.

This result is important context for the model results. The reviews themselves are difficult to align. People’s emotions about books are complex, and labeling the shifting sands of how humans describe their emotions about complex abstract concepts is difficult to align on. The lower agreement scores show that the construct is valuable but inherently nuanced.

## GenAI Benchmark

We benchmarked six genAI models from four suppliers: OpenAI GPT-4o-mini, OpenAI GPT-4.1-mini, Anthropic Claude Sonnet 4.6, DeepSeek Chat, Grok 3 Fast, and Grok 4.1 Fast. The same prompt and label schema were used across models.

GPT-4o-mini was selected as the best overall genAI strategy because it gave usable performance at the lowest cost and had no parsing failures. It had an emotion macro F1 of 0.394, commitment macro F1 of 0.516, and recommendation macro F1 of 0.563. Its estimated cost was about $0.138 per 1,000 reviews, or about $1.38 per 10,000 reviews.

## Specialist Model

We fine-tuned RoBERTa as the specialist model. We tested four configurations and selected configuration 3 as the best specialist model because it offered strong F1 scores without the longer training time and overfitting risk of the 10-epoch configuration. Configuration 3 used RoBERTa-base with a learning rate of 2e-5, 5 epochs, batch size 16, max length 512, and a 0.4 threshold for emotions.

On the development evaluation, configuration 3 reached emotion macro F1 of 0.713, commitment macro F1 of 0.839, and recommendation macro F1 of 0.840. On the locked holdout set, it reached emotion macro F1 of 0.406, commitment macro F1 of 0.622, and recommendation macro F1 of 0.700.

These holdout results support using RoBERTa as the production classifier. RoBERTa outperformed GPT-4o-mini on all three major holdout evaluations while being a smaller task-specific model.

## Error Analysis

The main error pattern was rare emotions and overlapping emotional categories. GPT-4o-mini performed reasonably well on common labels like love, but struggled with rare labels such as disgust, fear, and anger. Disgust had an F1 score of 0.000, fear had an F1 score of 0.200, and anger had an F1 score of 0.231.

The model also over-applied joy, with very high recall but low precision. This means it often labeled reviews as joyful even when the human consensus did not. This matches the human agreement issue because emotional categories like joy, love, interest, and contentment often blur together in real reviews.

## Deployment Controls

Underbrush should use RoBERTa for routine high-volume classification and GPT-4o-mini for new labeling rounds, ambiguous reviews, and low-confidence cases. Rare emotions such as disgust, fear, and anger should be routed to human review when the prediction matters. Underbrush should also monitor class prevalence by month, review length, rating, and genre, and re-benchmark genAI labelers when provider models change.

