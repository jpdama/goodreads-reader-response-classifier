# Data Source Plan and Sampling Approach

## Source

The source is the **UCSD Goodreads Book Graph** dataset maintained by the McAuley Lab. The dataset page describes large-scale Goodreads book metadata, user-book interactions, and detailed review text. The review data is appropriate because it contains the free-text language needed to detect emotion, recommendation intent, and continuation commitment.

Primary source pages:

- UCSD Goodreads dataset page: https://cseweb.ucsd.edu/~jmcauley/datasets/goodreads.html
- UCSD Book Graph mirror: https://mcauleylab.ucsd.edu/public_datasets/gdrive/goodreads/UCSD%20Book%20Graph.html
- Reviews page: https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/reviews

The dataset maintainers state that the data was collected from public Goodreads shelves, that user/review identifiers are anonymized, and that the dataset is for academic use. That matters for governance: raw data should not be redistributed publicly, and any deliverable should avoid exposing unnecessary user identifiers.

## Why This Source Fits

The construct requires naturally occurring reader language. Goodreads reviews include:

- Emotional evaluations: "I loved this," "the ending made me cry," "this was boring."
- Recommendation cues: "everyone should read this," "skip it," "not for me but maybe for fans."
- Continuation cues: "I cannot wait for the sequel," "I will not read this author again."
- Metadata useful for sampling, such as rating, book ID, user ID, votes, comments, and dates.

This source is better than synthetic text because the classifier must handle real review messiness: short reviews, sarcasm, mixed emotions, spelling variation, genre-specific language, and sparse explicit recommendation signals.

## Business Use Pattern

Underbrush would use the dataset in two stages:

1. **Development and benchmarking**: use the UCSD Goodreads corpus to sample, label, benchmark genAI labelers, and train a specialist classifier.
2. **Operational monitoring**: apply the trained classifier to newly collected or licensed review streams on a weekly basis for new releases and monthly/quarterly for catalog reporting.

Example operating cadence:

- Weekly: classify new reviews for monitored authors, series, and high-growth categories.
- Monthly: refresh product dashboards and investigate negative emotion spikes.
- Quarterly: retrain or recalibrate the model if label drift, genre mix changes, or performance monitoring flags degradation.

## Access Plan

The preferred access path is to download the dataset files made available by UCSD instead of scraping Goodreads directly. This respects the source's published access pathway and avoids violating platform rules.

For resource control, start with one genre subset rather than the complete 15M review file. Recommended first subset: **young adult**, **romance**, or **mystery/thriller/crime**, because these genres often contain explicit emotion, series continuation, and recommendation language. If file size is a concern, begin with the smaller **poetry** subset for pipeline testing, then rerun the same scripts on the final chosen genre.

## Sampling Requirements

The project requires:

- 15,000 texts total for train/test.
- 1,000 texts for a locked human-labeled holdout.
- 16,000 total sampled reviews before labeling and splitting.

The holdout must be locked early and not used for prompt tuning, model selection beyond final evaluation, or hyperparameter iteration.

## Sampling Strategy

Use stratified sampling so the dataset is not dominated by short positive reviews. The sampling frame should balance:

- **Rating**: 1, 2, 3, 4, 5, and missing/zero if present.
- **Review length**: short, medium, and long buckets based on token count.
- **Genre/source subset**: if multiple files are used, preserve a source indicator.
- **Potential signal density**: optionally oversample reviews containing weak lexical cues for rare emotions or continuation language, then report the oversampling.

Recommended operational split:

- `holdout.csv`: 1,000 reviews, locked immediately.
- `train.csv`: 12,000 reviews.
- `test.csv`: 3,000 reviews.

The train/test labels may be generated after benchmarking the genAI strategy. The holdout labels must come from humans.

## Data Cleaning

Minimum preprocessing:

- Remove exact duplicate review texts.
- Remove empty, whitespace-only, and very short non-review strings.
- Normalize whitespace.
- Preserve the original raw review text in a separate field.
- Strip HTML artifacts if present.
- Keep a quality flag rather than silently deleting every messy case.

Do not aggressively remove punctuation, capitalization, or emotive markers because they may carry label signal.

## Documentation Outputs

The dataset documentation should report:

- Source file name and download date.
- Sampling seed.
- Number of records read and sampled.
- Duplicate count removed.
- Empty/spam/quality issue count.
- Rating distribution.
- Review length summary.
- Final split counts.
- Any oversampling rules used.

