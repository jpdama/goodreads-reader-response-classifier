You are labeling Goodreads-style book reviews for a reader response classification project.

Unit of analysis: the entire review.

Return valid JSON only with this schema:

```json
{
  "emotions": ["joy"],
  "commitment": "medium",
  "recommendation": "neutral",
  "quality_issue": false,
  "rationale": "Short reason using only evidence from the review."
}
```

Allowed emotion labels: joy, love, surprise, contentment, interest, anger, frustration, disappointment, sadness, fear, disgust, boredom, none.

Rules:
- Choose every emotion explicitly expressed by the reviewer toward the book, reading experience, author, characters, plot, or series.
- If no emotion is expressed, use only `none`.
- `none` must never be combined with another emotion label.
- Choose exactly one commitment label: low, medium, high.
- Commitment means likely continuation with the author, series, universe, or closely related books.
- Use `medium` when continuation is unclear, mixed, conditional, or not mentioned.
- Choose exactly one recommendation label: would_not, neutral, would_recommend.
- Use `neutral` when recommendation is unclear, mixed, audience-specific, conditional, or not mentioned.
- If the text is empty, spam, unintelligible, or not a review, set quality_issue true, emotions ["none"], commitment "medium", and recommendation "neutral".
- Code the reviewer's response, not objective plot content.
- Text overrides star rating if both are provided.

Review:
{{review_text}}

