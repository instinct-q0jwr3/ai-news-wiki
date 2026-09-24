# Security auditing in the age of (good enough) AI

_type: news-summary · created: 2026-09-24 · updated: 2026-09-24 · confidence: high_

`hacker-news` `ai-safety-incidents`

## Summary

A security firm's writeup argues the interesting AI shift in security reviews is not agentic code review but the tooling agents now let them build before review starts. Preparing to review the Miden VM - a new zero-knowledge VM with a custom assembly language and almost no developer tooling - they spent six months having agents build an LSP server, a decompiler, a static analysis engine, and a Lean model of the VM executor from scratch.

The tooling found real issues, including an unvalidated prover-supplied input that would have let a malicious prover forge Falcon signatures and steal funds from Miden account holders. The Lean work also produced 95 machine-checked correctness proofs covering a large component of the Miden core library - a depth of formal assurance that would have been impractical to hand-build for a pre-launch review.

## Highlights

- Agents used to build custom security tooling: LSP server, decompiler, static analyzer, Lean model of the Miden VM executor.
- Six months of agent-built tooling before the review itself began.
- Found a critical bug: unvalidated prover input enabling forged Falcon signatures and fund theft.
- 95 machine-checked correctness proofs produced for the Miden core library.
- Argues custom tooling, not just agentic code review, is the real AI gain for security audits.

## Source

[Read the original story](https://blog.trailofbits.com/2026/09/18/auditing-in-the-age-of-good-enough-ai/)

## Related pages

[AI safety incidents and controls](../concepts/ai-safety-incidents.md)
