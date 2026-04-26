# Labeling Codebook

## Project

**Construct:** reader response in book reviews.  
**Unit of analysis:** entire review.  
**Source domain:** Goodreads-style book reviews.  
**Coding mode:** one review receives emotion labels, one commitment label, and one recommendation label.

## Label Overview

| Dimension | Label Type | Labels |
|---|---:|---|
| Emotions | Multi-label | joy, love, surprise, contentment, interest, anger, frustration, disappointment, sadness, fear, disgust, boredom, none |
| Commitment | Single-label ordinal | low, medium, high |
| Recommendation | Single-label ordinal | would_not, neutral, would_recommend |

## General Rules

1. Code the reviewer's expressed response, not the objective content of the plot.
2. Use the entire review as context.
3. Text overrides rating when both are available.
4. Emotion labels are multi-label. Select every emotion clearly expressed by the reviewer.
5. `none` is exclusive. If any other emotion is present, do not select `none`.
6. Commitment and recommendation are single-label. Select exactly one label for each.
7. When commitment is unclear or absent, use `medium`.
8. When recommendation is unclear or absent, use `neutral`.
9. If a review is empty, spam, unintelligible, or not a review, use emotions `none`, commitment `medium`, recommendation `neutral`, and flag a quality issue.
10. Do not infer emotions solely from genre or plot events. A horror book is not `fear` unless the reviewer says they felt scared, creeped out, anxious, or similar.

## Emotion Labels

### Joy

Reviewer expresses happiness, delight, amusement, excitement, or being uplifted.

Use when:

- The review says the book made the reader happy, laugh, smile, or feel delighted.
- The reviewer describes the reading experience as fun or exciting.

Do not use when:

- The reviewer merely gives a positive rating without emotion.
- The reviewer says the book is "good" but not emotionally joyful.

Examples:

- "This book made me grin the entire afternoon."
- "Such a fun read; I had a great time with it."
- "The ending left me genuinely happy."

### Love

Reviewer expresses strong affection, devotion, adoration, or favorite-level attachment.

Use when:

- The reviewer says they loved the book, author, characters, writing, or series.
- The reviewer calls it a favorite or says they are obsessed.

Do not use when:

- The reviewer only says they liked or enjoyed it mildly.

Examples:

- "I absolutely loved this book and already miss the characters."
- "This is one of my favorite reads of the year."
- "I adore the author's voice."

### Surprise

Reviewer describes shock, unexpectedness, twists, revelations, or being caught off guard.

Use when:

- The reviewer says they did not see something coming.
- The review emphasizes twists or unexpected developments.

Do not use when:

- The reviewer summarizes a plot twist without saying it surprised them.

Examples:

- "I did not see that ending coming."
- "The twist halfway through completely shocked me."
- "This went in a direction I never expected."

### Contentment

Reviewer expresses satisfaction, comfort, calm enjoyment, or that expectations were met.

Use when:

- The reviewer describes the book as satisfying, pleasant, comforting, cozy, or exactly what they wanted.
- The tone is positive but calmer than joy or love.

Do not use when:

- The review expresses intense affection better coded as love, unless satisfaction is also explicit.

Examples:

- "A quiet, satisfying read."
- "This was exactly the comfort book I wanted."
- "I enjoyed the ending and felt at peace with it."

### Interest

Reviewer expresses curiosity, engagement, intrigue, or intellectual fascination.

Use when:

- The reviewer says the premise, world, argument, mystery, or character arc was interesting or intriguing.
- The review says the book kept them engaged.

Do not use when:

- "Interesting" is clearly sarcastic.
- The reviewer mentions a topic without saying it engaged them.

Examples:

- "The premise was intriguing from page one."
- "The history behind the setting kept me interested."
- "I wanted to understand how the mystery would unfold."

### Anger

Reviewer expresses anger, outrage, moral indignation, or being mad.

Use when:

- The reviewer uses words like angry, furious, rage, outraged, or blood boiling.
- The reviewer expresses moral outrage at the book's content, message, or execution.

Do not use when:

- The reviewer is merely annoyed or confused. Use frustration instead.

Examples:

- "The ending made me furious."
- "I was angry at how carelessly the author handled that topic."
- "This book made my blood boil."

### Frustration

Reviewer expresses annoyance, irritation, impatience, confusion with the book, or feeling blocked by flaws.

Use when:

- The reviewer says the pacing, structure, writing, or character decisions annoyed them.
- The reviewer felt stuck, confused, or irritated.

Do not use when:

- The review is negative but unemotional.

Examples:

- "The pacing was so frustrating."
- "I kept getting annoyed by the narrator's choices."
- "The timeline was confusing in a way that made the book hard to enjoy."

### Disappointment

Reviewer says the book fell short of expectations or potential.

Use when:

- The reviewer expected more from the author, series, premise, or hype.
- The review frames the reaction as a letdown.

Do not use when:

- The reviewer disliked the book but does not express an expectation gap.

Examples:

- "I wanted to love this, but it was a letdown."
- "After the first book, this sequel disappointed me."
- "The premise had so much potential, but the execution fell flat."

### Sadness

Reviewer expresses sadness, grief, heartbreak, melancholy, guilt, or being emotionally hurt.

Use when:

- The reviewer says they cried or felt sad, devastated, heartbroken, or emotionally wrecked.
- The review describes guilt or sorrow as the reader's response.

Do not use when:

- The plot includes sad events but the reviewer does not describe feeling sad.

Examples:

- "I cried through the last chapter."
- "This book left me heartbroken."
- "The story made me feel a deep sadness."

### Fear

Reviewer expresses fear, dread, anxiety, creepiness, or being scared.

Use when:

- The reviewer says the book scared, unsettled, or creeped them out.
- The reviewer describes suspense as fear or dread.

Do not use when:

- The book is labeled horror but the reviewer does not report fear.

Examples:

- "This genuinely scared me."
- "I felt dread every time the house appeared."
- "The atmosphere was creepy enough that I had to stop reading at night."

### Disgust

Reviewer expresses repulsion, revulsion, or distaste toward content, style, character behavior, or reading experience.

Use when:

- The reviewer uses terms like disgusting, gross, revolting, repulsive, or made me sick.
- The reviewer expresses moral or physical revulsion.

Do not use when:

- The reviewer simply says something was bad.

Examples:

- "The violence was so graphic it made me feel sick."
- "I found the main character's behavior repulsive."
- "Some scenes were just gross, not meaningful."

### Boredom

Reviewer expresses boredom, dullness, lack of engagement, tediousness, or indifference.

Use when:

- The reviewer says the book was boring, slow, dull, tedious, or dragged.
- The reviewer says they could not stay interested.

Do not use when:

- The review is short but not emotionally bored.

Examples:

- "I was bored by chapter three."
- "The middle dragged for nearly two hundred pages."
- "Nothing held my attention."

### None

No codable emotion is expressed, or the review is empty, unintelligible, purely factual, or only contains metadata.

Use when:

- The review contains no emotional reaction.
- The text is spam, broken, or not a review.

Do not use when:

- Any other emotion label applies.

Examples:

- "Paperback edition, 320 pages."
- "Read for book club."
- "asdf qwer 123"

## Commitment Labels

Commitment measures whether the reviewer is likely to continue with this author, series, universe, or closely related books.

### Low

Reviewer explicitly rejects continuing, says they will not finish/read more, or shows strong evidence of abandonment.

Examples:

- "I will not read another book by this author."
- "This convinced me to quit the series."
- "I could not finish it and have no interest in trying the sequel."

### Medium

Continuation is unclear, mixed, conditional, or not mentioned. This is the default.

Examples:

- "I might try the sequel if reviews are better."
- "I liked parts of it, but I am not sure I need more."
- "A decent standalone read."

### High

Reviewer explicitly intends to read more, continue the series, seek the sequel, or read more by the author.

Examples:

- "I cannot wait for the next book."
- "I am reading everything this author writes."
- "This made me want to continue the series immediately."

## Recommendation Labels

Recommendation measures whether the reviewer would recommend the book to another reader.

### Would Not

Reviewer discourages reading, warns others away, or says the book is not worth the time.

Examples:

- "Do not waste your time on this."
- "I would not recommend this to anyone."
- "Skip it and read something else."

### Neutral

Recommendation is unclear, mixed, conditional, audience-specific, or not mentioned. This is the default.

Examples:

- "Fans of slow literary fiction may like this."
- "I am not sure who I would recommend this to."
- "It has strengths and weaknesses."

### Would Recommend

Reviewer explicitly recommends the book, urges others to read it, or says it is worth reading.

Examples:

- "I highly recommend this."
- "Everyone should read this book."
- "If you like mysteries, put this on your list."

## Borderline Rules

### Mixed Reviews

Code all explicit emotions. A review can be both `love` and `disappointment` if the reviewer loved the characters but was disappointed by the ending.

### Sarcasm

Code sarcasm only when the implied meaning is clear. "Great, another pointless love triangle" should be coded as frustration or disappointment, not joy.

### Plot Versus Feeling

"A character dies" is not sadness. "A character dies and I cried" is sadness.

### Rating Conflicts

If a 5-star review says "I loved the first half but hated the ending," code the textual emotions. Do not force all labels positive because of the rating.

### Conditional Recommendation

If the reviewer recommends the book only to a narrow audience, use `neutral` unless the recommendation is clearly positive for a broad or relevant audience.

### Abandonment

Did-not-finish reviews usually imply `commitment low` only when the reviewer connects that abandonment to the author, series, sequel, or future reading.

## Human Labeling Procedure

Each holdout review should receive three independent human annotations. Coders should not see model labels. Recommended workflow:

1. Train coders on 30 pilot examples.
2. Discuss disagreements and update the codebook before labeling the locked holdout.
3. Label the 1,000-item holdout independently.
4. Calculate agreement by dimension using Krippendorff's alpha and percent agreement.
5. Create a consensus label for final evaluation through majority vote, with adjudication for three-way splits.

