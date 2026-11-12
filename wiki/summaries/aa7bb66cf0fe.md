# AI Can Write More of the Code. We Still Have to Engineer the System

_type: news-summary · created: 2026-11-02 · updated: 2026-11-12 · confidence: high_

`hacker-news`

## Summary

An engineer's answer to 'AI has transformed software development' is to ask which part, exactly, got transformed. Producing an implementation, exploring a design, and deciding whether a system solves the right problem are connected but distinct - and automating one settles none of the others. The piece's claim: agents can absorb more implementation work and assist with analysis, design and testing, while engineers remain responsible for deciding what to build and what evidence is sufficient to accept it. The author resists the 'replacing the typist' framing - it understates agents and turns task automation into a jobs claim that requires evidence beyond a good demo.

The practical core is about memory and accountability. A chat is convenient for exploring options and a fragile place to keep the only record of a decision: context is bounded, sessions get summarized and compacted, and a summary can preserve the conclusion while losing the condition that made it reasonable ('use a local cache' is not 'use a local cache because this screen must work offline'). The recommendation: give durable decisions a small, reviewable home - a PROJECT_GUIDE.md wired into the tool's project instructions - supply each increment with the relevant files, and ask the agent to paraphrase intent, constraints and acceptance cases before implementing. Markdown guarantees neither retrieval nor obedience, and any claim of savings needs measurement of the complete task, not the prompt.

## Highlights

- Which part of development did AI transform? Implementation, design exploration and problem selection are different questions
- Agents take more implementation; engineers keep deciding what to build and what evidence accepts it
- Against the 'replacing the typist' frame: understates agents, and job claims need evidence
- Chat is a fragile record: compaction preserves conclusions and drops the conditions behind them
- Fix: a small reviewable PROJECT_GUIDE.md, wired into project instructions, with paraphrase checks per increment
- Markdown alone guarantees neither retrieval nor obedience - measure the whole task before claiming savings

## Source

[Read the original story](https://picon.dev/en/publications/ai-assisted-engineering/)

## Related pages

_No related entity or concept page yet._
