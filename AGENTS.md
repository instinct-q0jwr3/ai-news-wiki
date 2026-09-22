# Schema and maintenance contract

This repository follows the persistent-wiki pattern described in Karpathy's "LLM Wiki" gist.

## Layers

- `raw/snapshots/`: immutable timestamped source snapshots. Never edit an existing snapshot.
- `wiki/`: generated, cumulative Markdown knowledge. The maintainer may update these pages.
- `docs/`: static GitHub Pages build generated from `wiki/`; never hand-edit it.
- `AGENTS.md`: this schema and operating contract.

## Ingest

1. Run `python3 src/update_feed.py`.
2. Preserve every raw snapshot.
3. Update the matching daily page and `wiki/index.md`.
4. Append one parseable `## [YYYY-MM-DD] ingest | ...` entry to `wiki/log.md`.
5. Run `python3 scripts/derive.py` to refresh evidence blocks, weekly synthesis, comparisons, concepts and hubs.
6. Run `python3 scripts/build_site.py` to rebuild `docs/`.
7. Keep source URLs attached to each claim. Do not invent summaries or links.

The supported pass entrypoint is `scripts/run_pass.sh`. Derived pages may contain a curated interpretation outside auto markers; the pipeline only replaces marked evidence blocks. The external 6-hour runner should run the entrypoint and commit `raw wiki docs`.

## Query and synthesis

Read `wiki/index.md` first, then open only relevant daily pages and raw snapshots. Useful analyses may be filed as new Markdown pages and linked from the index.

## Lint

Check for broken links, duplicated stories, stale daily pages, orphaned wiki pages, contradictions and missing source attribution. Raw snapshots are immutable.

## Daily digest artifact (raw/llm/digest-YYYY-MM-DD.json, schema 2)

The external runner may author one curated artifact per day: `{"id":"digest-YYYY-MM-DD","date":"YYYY-MM-DD","schema":2,"model":"agent-pass","lead":["<one tight editorial paragraph framing the day, with inline [links](../summaries/<id>.md)>"]}`. The pipeline renders the lead directly under the daily header; the thematic sections below it are generated automatically from the corpus in the same style as the weekly synthesis. Do not author per-section prose for the daily page. Daily and weekly titles are static: `AI in the news - YYYY-MM-DD` and `Week YYYY-Www` (no descriptive headlines).
