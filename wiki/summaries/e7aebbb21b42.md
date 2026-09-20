# Git as Shared Memory for AI Research Agents

_type: news-summary · created: 2026-09-20 · updated: 2026-09-20 · confidence: high_

`tldr-ai` `agentic-systems`

## Summary

Git as Shared Memory for AI Research Agents. Agora lets research agents share experiments and findings across separate sessions.

Agora provides the shared record; workers choose their experiments.

## Highlights

- Contributions are immutable Git commits linked to the work they build on.
- Searchable views show leading results, neglected branches, and verification status; recommendations help workers choose between refining a result and exploring another approach.
- Authors: Yifan Zhang , Yunheng Zou, Shaokun Zhang, Jian Hu, Hao Zhang, Binfeng Xu, Jan Kautz, Yi Dong (NVIDIA) Report: September 16, 2026 · arXiv: 2609.18094 [ Paper ] [ Project website ] [ The weight-transfer run ] Workers publish…
- They use this record to choose experiments and build on prior work without sharing a conversation or workspace.
- Projects define their own instructions, metrics, artifact requirements, and safety boundaries.
- Authentication and project metadata require separate database backups.
- A participant submits a transfer(model, config) function; the evaluator scores 200 FineWeb-Edu texts in bits per byte.
- 13 language-model workers ran for nearly 12 days with a two-page brief, the evaluator and the shared graph, with no assigned tasks and no central planner.

## Source

[Read the original story](https://github.com/yifanzhang-pro/Agora) · [TLDR AI issue](https://tldr.tech/ai/2026-09-18)

## Related pages

[Agentic systems](../concepts/agentic-systems.md)
