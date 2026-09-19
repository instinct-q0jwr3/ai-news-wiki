# Schema and maintenance contract

This repository follows the persistent-wiki pattern described in Karpathy's "LLM Wiki" gist.

## Layers

- `raw/snapshots/`: immutable timestamped source snapshots. Never edit an existing snapshot.
- `wiki/`: generated, cumulative Markdown knowledge. The maintainer may update these pages.
- `AGENTS.md`: this schema and operating contract.

## Ingest

1. Run `python3 src/update_feed.py`.
2. Preserve every raw snapshot.
3. Update the matching daily page and `wiki/index.md`.
4. Append one parseable `## [YYYY-MM-DD] ingest | ...` entry to `wiki/log.md`.
5. Keep source URLs attached to each claim. Do not invent summaries or links.

## Query and synthesis

Read `wiki/index.md` first, then open only relevant daily pages and raw snapshots. Useful analyses may be filed as new Markdown pages and linked from the index.

## Lint

Check for broken links, duplicated stories, stale daily pages, orphaned wiki pages, contradictions and missing source attribution. Raw snapshots are immutable.
