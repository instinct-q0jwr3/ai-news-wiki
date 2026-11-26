# Show HN: TrnRT – An open-source LLM inference engine for AWS Trainium

_type: news-summary · created: 2026-11-17 · updated: 2026-11-26 · confidence: high_

`hacker-news` `amazon` `deepseek` `agentic-systems` `external-evaluation` `ai-coding-agents` `ai-price-war`

## Summary

TrnRT presents an open inference engine for AWS Trainium, initially supporting GLM-5.3-Flash on a single Trainium2 instance. Its repository describes compiled kernels, host and device prefix caching and an OpenAI-compatible serving API.

Reported agent-session costs depend on hardware pricing, batch configuration and a specified earlier build. They count input, cached input and output together, so they cannot be read as an equivalent public API output-token price. Model coverage and known issues remain important deployment limits.

## Highlights

- Initial model support is narrow
- Compilation is a separate preparation stage
- Prefix cache spans host and device memory
- Benchmark costs depend on instance pricing
- Earlier-build results are not universal current guarantees

## Source

[Read the original story](https://github.com/RunanywhereAI/trnrt)

## Related pages

[Amazon](../entities/amazon.md) · [DeepSeek](../entities/deepseek.md) · [Agentic systems](../concepts/agentic-systems.md) · [External AI evaluation](../concepts/external-evaluation.md) · [AI coding agents and the software pipeline](../concepts/ai-coding-agents.md) · [The frontier model price war](../concepts/ai-price-war.md)
