# Show HN: A Claude Code skill to analyze your chess games

_type: news-summary · created: 2026-09-26 · updated: 2026-09-29 · confidence: high_

`hacker-news` `anthropic` `agentic-systems` `ai-coding-agents`

## Summary

Show HN: a Claude Code skill that turns one of your chess games into a readable post-mortem - plain-language explanations of your mistakes, checked against Stockfish, plus a narrated video of the game. The author's own twist: during a 15+10 rapid game on lichess he recorded himself thinking aloud in French, then gave Claude the lichess link and the mp3. Claude transcribed the audio locally with whisper.cpp and used the PGN clock times to match each spoken thought to the move being decided.

The result is a video where the commentary answers your own questions ('at move eight you asked yourself whether the bishop belongs on c4 or e2') with engine verification - a personal coach built from your own voice. The post hit the HN front page; the author regrets demoing with a game containing a massive blunder of his own.

## Highlights

- Claude Code skill generates chess post-mortems in plain language.
- Mistakes verified against Stockfish; narrated video output.
- Syncs think-aloud audio to moves via PGN clock times.
- Local transcription with whisper.cpp.
- Commentary answers the player's own in-game questions.
- Made the HN front page.

## Source

[Read the original story](https://github.com/brumar/chess-postmortem-skills)

## Related pages

[Anthropic](../entities/anthropic.md) · [Agentic systems](../concepts/agentic-systems.md) · [AI coding agents and the software pipeline](../concepts/ai-coding-agents.md)
