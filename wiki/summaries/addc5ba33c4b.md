# Your Model Is a Dependency

_type: news-summary · created: 2026-11-27 · updated: 2026-11-28 · confidence: high_

`tldr-ai`

## Summary

César Soto-Valero argues that a deployed model should be managed as a software dependency, together with prompts, tools, retrieval, serving behavior and an exit path. The article proposes pinning versions, repeated paired regression tests, inventories, minimal dependencies, provenance checks and rehearsed fallbacks.

These are engineering recommendations, not an audit showing a particular system compliant or safe. A model identifier does not pin every serving computation, hashes do not prove trustworthy provenance, and an average gain can hide regressions. Provider retirement dates and legal interpretations in the article were not independently checked for operational reliance. Code samples, lockfile checks and tool-removal suggestions were read only; no account, dependency or policy changed.

## Highlights

- Behavior depends on more than model weights
- Temperature zero is not a reproducibility guarantee
- Paired tests expose regressions hidden by averages
- Inventories and exit plans address concentration risk
- Hashes do not establish a source is trustworthy
- Legal and retirement details need independent current checks
- No code or configuration was applied

## Source

[Read the original story](https://www.cesarsotovalero.net/blog/your-model-is-a-dependency.html) · [TLDR AI issue](https://tldr.tech/ai/2026-11-27)

## Related pages

_No related entity or concept page yet._
