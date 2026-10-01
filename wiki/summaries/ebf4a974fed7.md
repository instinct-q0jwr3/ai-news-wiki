# Show HN: TurboGPT: train 22KiB transformer in 13s

_type: news-summary · created: 2026-09-30 · updated: 2026-10-01 · confidence: high_

`hacker-news`

## Summary

TurboGPT is a Show HN project that trains a tiny 22KiB byte-level GPT in about 13 seconds, written in CUDA C++ and released under the MIT license. It supports Linux/NixOS and Windows builds, stores full training checkpoints (model, optimizer, scheduler and trainer state) for resumable runs, and emits TensorBoard-compatible logs capped at 8Mi reports.

## Highlights

- Byte-level GPT training in CUDA C++, MIT licensed
- Trains a 22KiB transformer in about 13 seconds
- Checkpoints bundle model, optimizer, scheduler and trainer state; resumable with --load
- TensorBoard-compatible logging, one report per batch, capped at 8Mi reports
- Builds via nix-build on Linux/NixOS or PowerShell on Windows with CUDA 13.4

## Source

[Read the original story](https://github.com/lostmsu/TurboGPT)

## Related pages

_No related entity or concept page yet._
