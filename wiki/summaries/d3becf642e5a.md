# Agents don't need memory, they need documentation

_type: news-summary · created: 2026-10-04 · updated: 2026-10-06 · confidence: high_

`hacker-news` `agentic-systems`

## Summary

An essay arguing that agent memory plugins solve the wrong problem. They split conversations into snippets, store them in a vector database and attach the closest few to each prompt, which the author calls a lottery that leaves the agent without real understanding of the project.

His alternative is documentation: agents do not need memory, they need written material on where features are, why they were built and what was agreed. He lists recurring failure modes of memory tools and says fancier layers, such as overnight 'dreamers', compression and rerankers, only add cost on a flawed design.

## Highlights

- Memory plugins retrieve snippets by similarity and often miss.
- Agents need project documentation, not recalled fragments.
- Extra layers add tokens without fixing the design.
- Opinion piece, no benchmarks.

## Source

[Read the original story](https://liao.gg/blog/agents-dont-need-memory)

## Related pages

[Agentic systems](../concepts/agentic-systems.md)
