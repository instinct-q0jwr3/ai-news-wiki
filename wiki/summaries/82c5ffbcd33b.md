# Show HN: A Claude Code skill to analyze your chess games

_type: news-summary · created: 2026-09-26 · updated: 2026-09-26 · confidence: high_

`hacker-news` `anthropic` `agentic-systems` `ai-coding-agents`

## Summary

Hello HN, It started as an experiment: can Claude play chess properly if it uses vision instead of PGN notation?

The next experiment was to see whether Claude + Stockfish could explain a game.

Claude Code skills that turn one of your chess games into a post-mortem you can actually read: plain-language explanations of your mistakes, checked against Stockfish, and a narrated video of the whole game.

## Highlights

- A few sessions later, I had a system that takes my live audio notes (or text, for that matter) and a vague instruction like "analyze my last lichess game", and gives me a commented video of the game.
- The result is not perfect and it takes time to deliver (an hour or so), but for me it is a much more pleasant and memorable experience than clicking around Stockfish branches.
- It burns tokens, so make sure you have enough quota.
- From the session logs, the last analyzed game would have cost around $15 at API prices.
- The fact that it reflects on my own thinking during the game makes it interesting from a teaching point of view, so I thought it was worth sharing.
- After the game I gave Claude two things: the lichess link and the mp3.
- Copy (or symlink) the skill folders into .claude/skills/ of your project, or into ~/.claude/skills/ for all projects: git clone https://github.com/brumar/chess-postmortem-skills cp -r chess-postmortem-skills/skills/ * ~ /.claude/skills/…
- For your own games, tell Claude your level once and make it stick, for example in your CLAUDE.md : My lichess handle is <handle>.

## Source

[Read the original story](https://github.com/brumar/chess-postmortem-skills)

## Related pages

[Anthropic](../entities/anthropic.md) · [Agentic systems](../concepts/agentic-systems.md) · [AI coding agents and the software pipeline](../concepts/ai-coding-agents.md)
