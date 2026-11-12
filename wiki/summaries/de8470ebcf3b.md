# Show HN: LLM weight editing tool made by a 15-year-old

_type: news-summary · created: 2026-11-08 · updated: 2026-11-12 · confidence: high_

`hacker-news`

## Summary

Laplace's Scissors is a Rust, Triton and CUDA/HIP tool that edits an LLM's output matrix by rotation so that chosen answers are repaired while protected correct answers stay intact. Its commands fetch and inspect a model, probe directions with weak output discrimination, diagnose failures from expected answer strings, generate, export an edited checkpoint, and analyze scaling across model sizes.

Each edit is validated against actual GPU outputs before it is accepted. The project needs a Rust toolchain, Python with Triton 3.8, and a CUDA or HIP driver, and caches models and kernels under a configurable directory. The Show HN title says it was made by a 15-year-old; the README itself does not say.

## Highlights

- Edits an LLM's output matrix by readout rotation.
- Aims to fix failed answers while protecting successful ones.
- Edits are checked against real GPU outputs.
- Commands: fetch, inspect, probe, diagnose, generate, export, scale.
- Requires Rust, Triton 3.8 and CUDA or HIP.

## Source

[Read the original story](https://github.com/Miyamoto-Renya/LaplacesScissors)

## Related pages

_No related entity or concept page yet._
