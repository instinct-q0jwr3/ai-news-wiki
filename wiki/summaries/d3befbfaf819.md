# TML releases Inkling 2 Mini, an open-weights 26.4B-parameter transformer that loops middle layers three times per token for better reasoning with fewer tokens

_type: news-summary · created: 2026-11-20 · updated: 2026-11-22 · confidence: high_

`techmeme`

## Summary

Thinking Machines releases Inkling 2 Mini, an open-weight mixture-of-experts model that repeats its middle layers to spend more computation per token without storing a larger model. The announcement separates improved reasoning and tool use from factual recall, and notes weaknesses on multi-turn constraints.

Its accompanying variable-loop research model supports preliminary monitoring experiments, not a general safety guarantee. Readable shorter reasoning and weak control over reasoning text are different from evidence that every internal step is observable. Comparisons also depend on precision, hardware and task; the local Mac launch configuration requires at least 32 GB RAM despite the roughly 20 GB weight footprint.

## Highlights

- Middle layers repeat three times per token
- Total parameters differ from active computation
- Looping helps some reasoning tasks more than recall
- Variable-loop model is a separate research artifact
- Monitoring findings are preliminary and scale-limited
- Energy comparisons use differing precisions
- Memory footprint is not the minimum system RAM

## Source

[Read the original story](https://thinkingmachines.ai/news/inkling-2-mini/)

## Related pages

_No related entity or concept page yet._
