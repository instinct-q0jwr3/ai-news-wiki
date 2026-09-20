# Notion lets teams share the same instructions across AI agents

_type: news-summary · created: 2026-09-20 · updated: 2026-09-20 · confidence: high_

`tldr-ai` `agentic-systems`

## Summary

Notion is turning its workspace into a shared skills library for AI agents: teams can author, organize and govern agent skills as ordinary Notion pages and databases, then load them into any agent through a new Skills API. The bet is that skills are becoming a critical store of organizational knowledge that should be agent-neutral rather than locked into one vendor's assistant.

The API returns skills in spec-compliant file formats, enabling concrete flows: syncing Notion skills into GitHub for use in Claude, ChatGPT and Grok Bot (an open-source starter kit is provided), editing skills from agent apps via MCP tools, and one-line installs through Vercel's skills CLI (npx skills add <notion url>). Customer quotes from Pearmill, Candidly and Brainlabs emphasize the non-engineer ergonomics that Git-only workflows lack.

## Highlights

- New Skills API loads skills from Notion in spec-compliant formats, usable by any agent or tool.
- Design goals: usable by the whole team (not just engineers), agent-neutral, collaborative with permissions and version history, observable and governable for admins.
- GitHub sync: open-source starter kit keeps Notion as the editing home while agents consume skills from repos.
- MCP tools let agent apps upload and edit Notion skills, creating a continuous-improvement loop.
- Vercel's skills CLI now supports Notion: 'npx skills add <notion url>' or interactive plugin installs.
- Customers cited: Pearmill (marketing/design/ops sharing skills weekly), Candidly, Brainlabs.
- Skills are stored as Notion pages in databases, with folders of supporting files like assets and code.

## Source

[Read the original story](https://www.notion.com/blog/a-skills-library-for-every-agent) · [TLDR AI issue](https://tldr.tech/ai/2026-09-18)

## Related pages

[Agentic systems](../concepts/agentic-systems.md)
