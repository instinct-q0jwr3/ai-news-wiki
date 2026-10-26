# Anthropic details Scion, a git replacement for its monorepo, built by seven engineers with Claude in five months, as daily merges rose from 2.5K in May to 30K+

_type: news-summary · created: 2026-10-13 · updated: 2026-10-26 · confidence: high_

`techmeme` `anthropic` `google` `meta` `amazon` `agentic-systems` `ai-safety-incidents` `ai-coding-agents` `labor-displacement`

## Summary

Anthropic describes Scion, an in-house version control system that replaced git for its monorepo, built by seven engineers with Claude in five months. The reason: coding is no longer the bottleneck at Anthropic, human-scale infrastructure is. Merged changes rose from about 2,500 a day in May 2026 to over 30,000 a day by September, and Anthropic expects more because every bottleneck removed raises code output.

Git's decentralized design, where every clone holds full history, no longer fits: main-branch history is almost 100 GB, a compressed working copy over 25 GB, and CI does around 25 million checkouts a day, which fetched naively would be over 600 PB. Alongside Scion the team shipped a code review surface called Antique, code search, source-control IAM and new ways to land large volumes of reviewed code. Anthropic frames this as a case study of Claude both creating the load and building the fix.

## Highlights

- Merges grew from ~2,500 per day (May) to 30,000+ per day (September).
- Scion replaced git for the monorepo in five months with seven engineers and Claude.
- Monorepo main history is ~100 GB; ~25M CI checkouts a day.
- Also built: Antique review surface, code search, source-control IAM.
- Argues other firms will hit the same pressure as AI coding spreads.

## Source

[Read the original story](https://www.anthropic.com/engineering/redesigning-source-control)

## Related pages

[Anthropic](../entities/anthropic.md) · [Google](../entities/google.md) · [Meta](../entities/meta.md) · [Amazon](../entities/amazon.md) · [Agentic systems](../concepts/agentic-systems.md) · [AI safety incidents and controls](../concepts/ai-safety-incidents.md) · [AI coding agents and the software pipeline](../concepts/ai-coding-agents.md) · [AI, jobs and displacement](../concepts/labor-displacement.md)
