# ML compiler eng, your job is NP-hard

_type: news-summary · created: 2026-11-25 · updated: 2026-11-27 · confidence: high_

`tldr-ai`

## Summary

Ian Barber uses a layout-selection hardness result to examine the gap between mathematical optimization and compiler performance. His account says that improving an inaccurate conversion-cost heuristic changed little across most tested kernels, while downstream instruction order and register allocation could dominate individual outcomes.

This is a practitioner experiment and reading of another paper, not an independently reproduced theorem or broad benchmark. A solver optimum is only optimal under its cost model, and an isolated reported 15–26x improvement is not an expected general speedup. The post's central point is that practical choice sets can be small even when the general problem is NP-hard; calibration to later compiler stages matters.

## Highlights

- Layout-search complexity is distinct from real execution cost
- Reported cost-model optimum can lose to heuristics
- Most tested kernels changed little
- Author reports eight slower, four faster and nine unchanged
- Rematerialization reduces the need for conversions
- Downstream register allocation can dominate
- Large isolated speedup is not a universal expectation
- No compiler code or benchmark was run

## Source

[Read the original story](https://ianbarber.blog/2026/11/24/ml-compiler-eng-your-job-is-np-hard/) · [TLDR AI issue](https://tldr.tech/ai/2026-11-25)

## Related pages

_No related entity or concept page yet._
