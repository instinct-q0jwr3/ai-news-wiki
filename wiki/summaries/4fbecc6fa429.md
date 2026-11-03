# Agents Prompt People: Using Agents for Long-Horizon Financial Work

_type: news-summary · created: 2026-10-31 · updated: 2026-11-03 · confidence: high_

`latent.space` `agentic-systems`

## Summary

Latent Space sits down with Aman Singh, lead AI engineer at Arca, an AI-native wealth-management firm that recently raised $48.5 million led by General Catalyst, and gets a rare concrete account of what agents at work actually means in a regulated business. Arca's line: agents do most of the background work, humans make the final calls - Singh's formulation is that agents prompt people more than people prompt agents. The work is long-horizon but stop-start, with tasks running up to ten days across many actors and handoffs, so the firm built an internal memory system that persists per-client state: what has happened, what is due in days, what is tracked long-term, and who owns each action.

The safety architecture is equally deliberate. Agents analyze and propose; trading and any money movement stay with human advisors. All safety restrictions are fully deterministic and take decisions out of the agent's hands, and Arca runs verification checks against known attack classes such as prompt injection. On infrastructure, Arca built its own harness that picks the best model per task against internal benchmarks - Claude is the primary provider - keeping the freedom to switch vendors, a quiet hedge that says as much about the model market as the tooling.

## Highlights

- Arca (AI-native wealth management, $48.5M raise) runs agents for long-horizon client work - tasks up to ten days
- Singh: 'agents prompt people more than people prompt agents'
- Agents analyze and propose; trading and money movement stay with human advisors
- Safety restrictions are fully deterministic, not model judgment
- Internal memory system tracks per-client state, next actions and owners across handoffs
- Own harness selects models per task against internal benchmarks; Claude is primary but swappable
- Runs verification checks against prompt injection and known AI attack classes
- A concrete reference architecture for agents in a regulated industry

## Source

[Read the original story](https://latent.space/p/arca/)

## Related pages

[Agentic systems](../concepts/agentic-systems.md)
