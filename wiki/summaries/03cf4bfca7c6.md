# A new era for software testing

_type: news-summary · created: 2026-09-26 · updated: 2026-09-28 · confidence: high_

`antirez` `agentic-systems` `ai-policy-regulation`

## Summary

Salvatore Sanfilippo (antirez) argues that AI coding trades quality for speed when writing new software - in his experience the output rarely reaches the structural quality of the best hand-written code, even if it beats decently written human code. But QA and testing, he says, are a domain where LLMs open strictly more powerful automation with no quality compromise at all.

His method: a markdown file that instructs an agent to work as a QA engineer on a new release. The agent first inspects what changed since the released version, then specializes its pass on what those commits could have broken. For his DwarfStar inference engine the file lists checks like distributed inference across two MacBooks over SSH and speed regressions - with no fixed baseline, since the target moves with each optimization. For Redis Arrays he had an agent build a real array-based application, run it for days under simulated load with replication and persistence, and report oddities. He also points to a psychological layer of quality - surprising, undocumented or sloppy features - that manual QA usually skipped entirely.

## Highlights

- AI-written code: big speed gains, some quality tradeoff; QA is a no-compromise win
- Core recipe: a markdown file telling an agent to act as a QA engineer
- The agent reads the new commits first and aims its testing at likely regressions
- DwarfStar example: distributed inference across two Macs, SSH endpoints and keys in the file
- Speed regression checks need no baseline - the agent finds the moving target itself
- Redis Arrays example: agent built and stress-ran a full production-like app for days
- Agents can review UX-level sloppiness and undocumented surprises humans skip

## Source

[Read the original story](http://antirez.com/news/168)

## Related pages

[Agentic systems](../concepts/agentic-systems.md) · [AI policy, regulation and litigation](../concepts/ai-policy-regulation.md)
