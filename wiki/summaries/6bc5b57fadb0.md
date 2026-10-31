# Building an Inference Stack That Improves Itself

_type: news-summary · created: 2026-10-29 · updated: 2026-10-31 · confidence: high_

`tldr-ai`

## Summary

Decagon describes AutoResearch, an agent system that tunes its own inference stack in a continuous loop: measure the existing deployment, diagnose bottlenecks, propose changes, and run experiments on GPUs - then verify any improvement and continue searching from the new baseline. The search space covers serving parameters, GPU layouts, speculative decoding and patches to the inference engine itself. The loop runs on Devin Cloud, whose persistent sessions let the orchestrator coordinate long-running experiments while subagents investigate focused questions in parallel; Modal provides GPU execution for training, profiling and replay runs.

The methodological core is the replay harness: optimizations are evaluated by replaying production traffic under controlled load, reconstructed from production logs with PII and sensitive data redacted. Because redaction changes token lengths and shared prefixes, Decagon explicitly checks that the replayed traffic stays representative of production - the principle being that an inference improvement is only real if it survives contact with what the endpoint actually processes and when requests arrive.

## Highlights

- AutoResearch: agents measure, diagnose, modify and re-test the inference stack in a loop
- Search space: serving parameters, GPU layouts, speculative decoding, engine patches
- Verified improvements become the new baseline and search continues
- Runs on Devin Cloud with parallel subagents; Modal supplies GPU execution
- Evaluates changes by replaying PII-redacted production traffic under controlled load
- Redaction shifts token lengths, so replay representativeness is checked explicitly

## Source

[Read the original story](https://x.com/DecagonAI/status/2115511110120120437) · [TLDR AI issue](https://tldr.tech/ai/2026-10-29)

## Related pages

_No related entity or concept page yet._
