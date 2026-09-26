# Can modern LLMs actually count the number of b's in "blueberry"?

_type: news-summary · created: 2026-09-25 · updated: 2026-09-26 · confidence: high_

`max-woolf`

## Summary

Max Woolf tests whether modern LLMs can count the b's in 'blueberry' - a descendant of the classic 'strawberry r's' failure. The root cause is tokenization: models see numerical token representations, not letters, so they may know 'straw'+'berry' but not the letter sequence of 'strawberry'.

The fun is in the failures: models confidently walk through letter-by-letter breakdowns and still land on wrong counts - one reply asserts three b's, 'checks carefully', misses one, then re-derives three again with contradictory step-by-step 'proofs', each stamped with a checkmark.

## Highlights

- Tokenization explains letter-counting failures: models see tokens, not characters
- Woolf's test: count the b's in 'blueberry' (correct answer: 2)
- Models produce confident, contradictory letter-by-letter 'proofs' of wrong counts
- One model asserts 3 b's, 'verifies' with a breakdown that actually shows 2, and still concludes 3
- The piece continues his series of probing LLM failure modes with humor

## Source

[Read the original story](https://minimaxir.com/2025/08/llm-blueberry/)

## Related pages

_No related entity or concept page yet._
