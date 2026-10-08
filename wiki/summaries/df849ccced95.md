# DoGBench: The first user-facing docs generation benchmark. No model scores >50%

_type: news-summary · created: 2026-10-02 · updated: 2026-10-08 · confidence: high_

`hacker-news` `external-evaluation`

## Summary

DoGBench is a new benchmark for agents that write and maintain user-facing software documentation. It has 292 tasks drawn from real open-source projects such as Helm, PostHog, Mautic and Doc Detective. In 205 of them the docs must change; in 87 the right move is to leave them alone, so agents are tested on judgment as well as writing.

The headline result is that no model scores above 50%. Agents write polished text but miss what readers need to finish a task, and they err both ways: documenting internal refactors that need no guidance, or overlooking a needed update because no existing page covers it. The authors publish 735 agent trajectories and caveat that cloud agents were told not to use the internet, which they could verify only for their own product.

## Highlights

- 292 tasks from real open-source repos; 205 need a docs change, 87 need none.
- No evaluated model scores above 50%.
- Agents fail in both directions: needless docs for refactors and missed updates.
- Scored with rubrics validated with project maintainers.
- 735 agent trajectories from seven non-cloud agents are published.
- Run by Promptless, whose own agent is among those tested, so treat comparisons with that in mind.

## Source

[Read the original story](https://dogbench.ai/)

## Related pages

[External AI evaluation](../concepts/external-evaluation.md)
