# Redis on the Raspberry Pi: adventures in unaligned lands

_type: news-summary · created: 2026-09-26 · updated: 2026-09-26 · confidence: high_

`antirez` `agentic-systems` `external-evaluation` `small-specialist-models` `ai-safety-incidents` `ai-policy-regulation`

## Summary

A classic antirez post from the Raspberry Pi era (3,319 days old): with 10 million Pis sold, the device had become programmers' preferred embedded experimentation platform - and he wanted Redis to be a first-class citizen on it. The catch: unaligned memory access. The Pi's default C compiler could emit code the default Linux kernel couldn't handle ('Alignment trap: not handling instruction...').

So he set a harder target: Redis must run even with the kernel's unaligned-access fixing disabled, which means ARM should only see word-sized unaligned accesses it can handle transparently. Redis superficially worked anyway, but the test suite exposed crashes in bit operations and hash functions. The post walks through finding and fixing them.

## Highlights

- Goal: Redis running cleanly on Raspberry Pi's ARM with alignment-fixing disabled
- The Pi's compiler could emit code the kernel's alignment trap couldn't handle
- Redis 'worked' until the test suite crashed in bit ops and hash functions
- The fix: only word-sized unaligned accesses, which ARM handles transparently
- A 10-year-old deep-dive from the Redis-on-embedded era

## Source

[Read the original story](http://antirez.com/news/111)

## Related pages

[Agentic systems](../concepts/agentic-systems.md) · [External AI evaluation](../concepts/external-evaluation.md) · [Small and specialist models](../concepts/small-specialist-models.md) · [AI safety incidents and controls](../concepts/ai-safety-incidents.md) · [AI policy, regulation and litigation](../concepts/ai-policy-regulation.md)
