# SlopCodeBench 10/2026 – Opus 5.5, Astra wins overall, xhigh considered harmful

_type: news-summary · created: 2026-10-20 · updated: 2026-10-22 · confidence: high_

`hacker-news` `external-evaluation`

## Summary

Humanlayer's October 2026 SlopCodeBench writeup expands the benchmark to 36 problems and 196 checkpoints per setting. The headline metric is strict pass rate (every test case passed while keeping regression tests green): frontier models land in a 12.2-16.3% band, with gpt-6 astra highest at 16.3%, versus 14.8% for gpt-5.5 back in May; the looser core pass rate sits at 65.8-74.0%. A notable finding: medium effort beats XHigh on some newer models, and Opus 5.5 did better on medium than on XHigh, even though XHigh costs 2.11-4.22x as much; where Opus 5.5 Medium had more strict passes, the XHigh runs wrote roughly 5x cleaner code. A qualitative Part II on slop patterns is promised.

## Highlights

- SlopCodeBench expands to 36 problems, 196 checkpoints per setting
- Strict pass rates: 12.2-16.3% across frontier models; gpt-6 astra leads at 16.3%
- May baseline: gpt-5.5 at 14.8% strict
- Core pass rate is much higher: 65.8-74.0%
- XHigh effort costs 2.11-4.22x Medium but loses to it on some newer models
- Opus 5.5 Medium had more strict passes; XHigh wrote ~5x cleaner code
- Qualitative slop-pattern analysis coming in Part II

## Source

[Read the original story](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/benchmarking-new-models-on-slop-code-bench.md)

## Related pages

[External AI evaluation](../concepts/external-evaluation.md)
