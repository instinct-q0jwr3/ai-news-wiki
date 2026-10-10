# Show HN: Jevman – AI decision models play Pac-Man

_type: news-summary · created: 2026-10-09 · updated: 2026-10-10 · confidence: high_

`hacker-news` `openai` `typesafe` `external-evaluation`

## Summary

Opper AI's Jevman benchmark tests AI decision models by having them play Pac-Man. At each junction the game sends the maze as JSON and the model returns a probability per direction, with a 2-second limit per answer before a simple backup rule takes over.

Each model plays 100 games against the classic scripted ghosts until it loses three lives, with games capped at five minutes; none lasted past 2 minutes 24 seconds. Anyone can submit a model by pull request and results are marked self-reported. It was motivated by OpenAI's new decisions endpoint and similar models.

## Highlights

- Pac-Man benchmark for fast decision models
- Model returns direction probabilities at each junction
- 2 second deadline, backup rule on timeout
- 100 games per model, three lives each
- Submissions by pull request, self-reported

## Source

[Read the original story](https://opper.ai/jevman-benchmark/)

## Related pages

[OpenAI](../entities/openai.md) · [TypeSafe](../entities/typesafe.md) · [External AI evaluation](../concepts/external-evaluation.md)
