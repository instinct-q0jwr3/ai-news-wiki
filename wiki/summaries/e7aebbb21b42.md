# Git as Shared Memory for AI Research Agents

_type: news-summary · created: 2026-09-20 · updated: 2026-09-24 · confidence: high_

`tldr-ai` `agentic-systems`

## Summary

Agora, an NVIDIA research project, uses Git as shared memory for AI research agents: instead of sharing a conversation or workspace, agents publish experiments, failures, hypotheses and reproductions as immutable commits in a shared contribution graph, linked to the work they build on. Searchable views surface leading results, neglected branches and verification status, and recommendations help agents choose between refining a result or exploring elsewhere.

In a weight-transfer benchmark, 13 language-model workers ran for nearly 12 days with no central planner and published 1,703 contributions. The best method initialized a frozen 119.6M-parameter attention-SSM hybrid to 1.899 bits per byte versus 3.3923 for random initialization, closing 62% of the gap to a trained GPT-2 124M, without any training data or gradient updates on the target. The result suggests a shared, inspectable record may be enough to coordinate multi-agent research at meaningful scale.

## Highlights

- 13 language-model workers ran ~12 days with a two-page brief, no assigned tasks and no central planner, publishing 1,703 contributions.
- Task: transfer knowledge from 141 open-weight donor models (534 GB, 32 architecture families) into a frozen 14-layer hybrid that matches none of them.
- Best result: 1.899 bits per byte vs 3.3923 random init, closing 62% of the gap to a trained GPT-2 124M (~1.0 bpb).
- The winning method's ancestry spans 145 commits across 15 accounts; 18 first-day contributions drove ~98% of the total improvement.
- Best method: build a context-averaged bigram table from donor next-token predictions, factorize it by SVD, then re-enable sublayers with sparse deterministic edits.
- Reliability: workers posted 165 reproductions across 95 targets with no reported failures.
- Final graph: 1,703 nodes, 1,894 edges, 149 multi-parent nodes; one component holds 98.9% of nodes.
- Paper: arXiv 2609.18094, 'Agora: Git as Shared Memory for Collective AutoResearch' (Zhang et al., NVIDIA).

## Source

[Read the original story](https://github.com/yifanzhang-pro/Agora) · [TLDR AI issue](https://tldr.tech/ai/2026-09-18)

## Related pages

[Agentic systems](../concepts/agentic-systems.md)
