# Anthropic redesigned source-control for AI agents

_type: news-summary · created: 2026-10-20 · updated: 2026-10-22 · confidence: high_

`hacker-news` `anthropic` `agentic-systems`

## Summary

Anthropic explains why it built Scion, an in-house version control system, migrating its monorepo off git in five months: coding is no longer the bottleneck, developer infrastructure built for human scale is. Merged changes went from about 2,500 per day in May 2026 to over 30,000 per day by September, and the company expects demand for merges to keep growing as each bottleneck is removed. Alongside Scion it shipped a code review surface (Antique), code search, source-control IAM, and new machinery for landing large volumes of reviewed code. Claude wrote much of the system, the same capability that created the load in the first place; Anthropic shares the work because it expects other heavy AI-coding shops to hit the same pressure points soon.

## Highlights

- Anthropic built Scion, its own VCS, and migrated the monorepo off git in five months
- Merges grew from ~2,500/day (May 2026) to 30,000+/day (September)
- Bottleneck shifted from writing code to human-scale dev infrastructure
- Also shipped Antique code review, code search, and source-control IAM
- Claude wrote the system that Claude's own output necessitated
- Git's decentralized design is the mismatch: every clone computes everything
- Anthropic expects other AI-heavy orgs to hit the same walls

## Source

[Read the original story](https://www.anthropic.com/research/redesigning-source-control)

## Related pages

[Anthropic](../entities/anthropic.md) · [Agentic systems](../concepts/agentic-systems.md)
