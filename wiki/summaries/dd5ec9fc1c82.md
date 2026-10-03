# Show HN: Reladraw – A diagram language where you decide where to place things

_type: news-summary · created: 2026-09-26 · updated: 2026-10-03 · confidence: high_

`hacker-news` `anthropic` `agentic-systems`

## Summary

Reladraw is a text language for diagrams where the author, not an algorithm, decides placement - but in relative statements ('below app.ui', 'right of app', 'between cluster.desktop1 and cluster.laptop1'), never coordinates. It aims at the gap between auto-layout languages like Mermaid, Graphviz and D2 (which can't express 'I want this module over here') and absolute-positioning tools like draw.io or Figma (where every edit to a complex diagram is slow hand-work). Nothing is nested, so no line depends on another line's position or indentation, and gaps are minimum distances: insert an element between two others and they push apart, delete it and they close back up.

The pitch is unusually agent-aware. Reading a pixel-positioned file, an agent must reconstruct the picture from coordinates before it can edit; with auto-layout there is nothing to read at all. With stated placement, editing the picture means editing the sentence that says where a thing goes - and the agent can re-read its own file to confirm intent (though not visual outcomes like overlaps, which need the renderer's diagnostics). Since no model has reladraw in its training data, the repo ships an installable agent skill (npx skills add reladraw/reladraw) for Claude Code, Codex, Cursor and others. v0.4.0 is a TypeScript parser, resolver and SVG renderer with zero runtime dependencies, CLI included; the language is explicitly unstable.

## Highlights

- Reladraw: a diagram text language where placement is stated in relative sentences, never coordinates
- Middle ground: Mermaid/Graphviz auto-layout can't express intended arrangement; draw.io/Figma make every edit manual
- Example: 44 statements reproduce a hand-drawn architecture diagram with no coordinates anywhere
- Flat structure: nothing nested, so lines never depend on each other's indentation or order
- Gaps are minimum distances - inserting a node pushes neighbors apart, deleting it closes them back up
- Agent angle: editing = changing the sentence that says where a thing goes; intent is re-readable from the file
- Honest limit: an agent can confirm stated intent but not rendered outcomes (overlaps, overflows) without diagnostics
- Ships an agent skill (npx skills add reladraw/reladraw) since the language is too new for any training data
- v0.4.0: TypeScript parser/resolver/SVG renderer, no runtime dependencies; syntax explicitly unstable

## Source

[Read the original story](https://github.com/reladraw/reladraw)

## Related pages

[Anthropic](../entities/anthropic.md) · [Agentic systems](../concepts/agentic-systems.md)
