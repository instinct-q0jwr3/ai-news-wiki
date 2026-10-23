# Framefields

_type: news-summary · created: 2026-10-06 · updated: 2026-10-23 · confidence: high_

`tldr-ai`

## Summary

Framefields is a beta npm package that packs compositing, motion graphics and 3D scene work into a single code-first video library aimed squarely at AI coding agents. Instead of driving a headless browser or a multi-gigabyte creative suite, an agent writes a TypeScript composition, inspects frames, and renders an MP4 directly on the GPU through Dawn/WebGPU, Vulkan or Metal, in Node.js or modern browsers.

The pitch is that automated video generation has been constrained by browser architectures - DOM reflow, screenshot pipelines, process overhead - so Framefields treats video as pure software engineering. It ships shader-based image and video nodes, chart layers built on d3 geometry, text rendered with the Slug algorithm so it stays crisp under 3D camera moves, and one-line skill installs for Claude Code, Codex, Cursor and other agents. The project positions itself against Remotion and Hyperframes and requires Node.js 22 or newer.

## Highlights

- One npm package combining Photoshop-style compositing, After Effects-style motion graphics and Blender-style 3D scenes.
- Built for AI coding agents: the agent writes TypeScript compositions and renders MP4s.
- GPU-native rendering via Dawn/WebGPU, Vulkan or Metal - no headless browser or DOM pipeline.
- One-line plugin/skill installs for Claude Code and other agents (npx skills add gatewai-dev/framefields).
- Chart layers use d3 for scales and geometry; every element is an ordinary box, path or text node.
- Text uses the Slug algorithm so it stays sharp during 3D camera sweeps.
- Compared against Remotion (React/Chromium) and Hyperframes (Canvas2D/SVG).
- Beta software: APIs may change and some features are incomplete.

## Source

[Read the original story](https://github.com/gatewai-dev/framefields) · [TLDR AI issue](https://tldr.tech/ai/2026-10-06)

## Related pages

_No related entity or concept page yet._
