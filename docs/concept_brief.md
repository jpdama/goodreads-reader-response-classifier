# Concept Brief: Reader Response Classification for Book Reviews

## Construct Choice

This project classifies **reader response** in book reviews: the emotions a reader expresses, whether the reader is likely to continue with the author or series, and whether the reader would recommend the book. The unit of analysis is the entire review.

The construct is valuable because book reviews are high-volume, unstructured evidence of product-market fit for books. Star ratings alone compress the reader's experience into a single number. Review text reveals why a book worked or failed: whether readers loved the characters, felt bored by the pacing, were surprised by the ending, felt disappointed by a sequel, or planned to continue the series.

## Stakeholder

The primary stakeholder is a **reader insights and recommendation product lead** at a book discovery platform, publisher, or subscription reading service. Secondary stakeholders include:

- **Editorial and acquisition teams** deciding which authors, genres, or series deserve investment.
- **Marketing teams** identifying books with strong word-of-mouth potential.
- **Recommendation product managers** improving personalization beyond ratings and genre tags.
- **Author relations or customer experience teams** tracking recurring complaints and reader attachment.
- **Investor relations or executive teams** monitoring leading indicators of audience engagement.

For this project, the firm can be framed as **Underbrush**, a book discovery and recommendation platform that uses review intelligence to improve personalization and publisher-facing analytics.

## Decision Enabled

Classification turns text reviews into structured signals that can support repeatable decisions:

- **Recommendation ranking**: promote books with high recommendation intent and strong positive emotions for similar readers.
- **Series investment**: detect books with high continuation commitment, even when ratings are mixed.
- **Retention risk**: identify books, authors, or categories that trigger boredom, frustration, or disappointment.
- **Marketing copy**: surface dominant reader reactions for campaigns, such as "surprising ending" or "comfort read."
- **Quarterly reporting**: track shifts in reader response by genre, author, release cohort, or campaign.

The key managerial question is not simply "Did readers rate the book highly?" It is "What response did the book create, and what action should the firm take because of it?"

## Why Classification at Scale

Human reading is too slow for large-scale review streams. The UCSD Goodreads data contains millions of review records, and even a narrow genre subset can contain hundreds of thousands of detailed reviews. A firm cannot manually inspect enough reviews to monitor reader response weekly or quarterly. A classifier enables:

- Faster monitoring of new releases and backlist titles.
- Consistent comparison across authors, genres, and time periods.
- Lower marginal cost once a specialist model is trained.
- Detection of rare but important signals such as disgust, fear, or abandonment intent.

## Error Costs

False positives and false negatives have different business consequences.

### Emotions

A **false positive** emotion label can misrepresent what readers value. For example, labeling a merely factual review as "love" could inflate perceived attachment and cause the platform to over-promote a title. Labeling plot content as reader fear when the reviewer was not personally scared could distort genre insights.

A **false negative** misses an actual reader response. Missing boredom or frustration hides a retention risk. Missing love or surprise weakens marketing and personalization signals.

### Commitment

A **false positive high commitment** label can make a weak series look like it has sequel demand. This could misallocate marketing or acquisition spend.

A **false negative high commitment** label misses future demand. A book with moderate ratings but strong continuation language may be more commercially valuable than ratings imply.

### Recommendation

A **false positive would-recommend** label can overstate word-of-mouth potential. A **false negative would-recommend** label can suppress books that readers actively advocate for. In deployment, false positives are more costly for promotional decisions, while false negatives are more costly for discovery and long-tail catalog value.

## Why Now

Several conditions make this construct timely:

- **Volume**: review platforms generate more text than teams can manually read.
- **Speed**: new books and social buzz move quickly; quarterly or monthly manual reviews are too slow.
- **Competitive need**: recommendation platforms compete on relevance, not just catalog size.
- **GenAI benchmarking**: modern language models can label nuanced constructs, but they are expensive and inconsistent unless benchmarked.
- **Specialist model opportunity**: a fine-tuned transformer can potentially match genAI quality at lower cost and higher reproducibility.

## Recommended Project Positioning

The capstone should position the classifier as a **decision system**, not just a text classification exercise. The business value comes from comparing three labeling strategies:

1. Human labels for the locked holdout as the evaluation anchor.
2. GenAI models as scalable but costly labelers.
3. A fine-tuned specialist model as a cheaper, repeatable production classifier.

The final recommendation should identify which strategy Underbrush should deploy, under what governance controls, and for which business decisions.

