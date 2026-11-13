# Show HN: OmniDiff – Opensource, super fast, content aware Git difftool, in Rust

_type: news-summary · created: 2026-11-01 · updated: 2026-11-13 · confidence: high_

`hacker-news` `ai-coding-agents`

## Summary

OmniDiff is an open-source, content-aware diff tool written in Rust, built from research into what diffs actually look like across open-source repositories. Rather than comparing lines of text, it diffs by type: code in 25 languages via tree-sitter grammars, config files, images (still and animated), PDFs, archives, cursors, fonts, OpenDocument files and compiled translation catalogs - a PDF diagram with one renamed box or a web font with twenty redrawn icons comes out as a meaningful diff instead of binary noise. It ships as a 24-bit-color TUI with light and dark themes, plus a headless mode for scripts that prints plain-text diffs.

Distribution is unusually thorough: cargo install, prebuilt binaries for Linux, macOS and Windows on every GitHub release, a Homebrew tap, a signed apt repository for Debian and Ubuntu, Nix flakes, and PKGBUILD/ebuild recipes for Arch and Gentoo. The author is honest about the edges: speed numbers come from one ThinkPad T14s, PDF support has fewer than ten judged test cases, the browser-based code review companion is at v0.0.0, and the VS Code extension is blocked on an upstream API that is implemented but unreleased.

## Highlights

- OmniDiff: open-source, content-aware diff tool in Rust - diffs by file type, not text lines
- Handles code in 25 languages (tree-sitter), images, PDFs, archives, fonts, OpenDocument, translation catalogs
- TUI with 24-bit color and themes; headless mode prints plain-text diffs for scripts
- Built from research into real diffs across open-source repos
- Install via cargo, prebuilt binaries, brew, signed apt repo, Nix, PKGBUILD/ebuild
- Honest limits: one-machine benchmarks, thin PDF test coverage, codereview at v0.0.0, VS Code blocked on an unreleased API

## Source

[Read the original story](https://github.com/ivankovic/omnidiff)

## Related pages

[AI coding agents and the software pipeline](../concepts/ai-coding-agents.md)
