# LayerStream: faster MoE fine-tuning on fewer or cheaper GPUs

_type: news-summary · created: 2026-11-27 · updated: 2026-11-28 · confidence: high_

`tldr-ai` `compute-buildout`

## Summary

Nebius describes LayerStream, a managed MoE training engine that moves optimizer state and saved activations into host memory and streams layer working state through GPUs. Its vendor tests report a Qwen pass over 25.8 million tokens falling from 22.4 to 7.1 minutes on the same sixteen H200 GPUs.

The main GLM cost and throughput comparison uses different data and an RL-loss baseline; separate matched-data loss checks cover only eighteen steps and do not prove equal downstream quality. Updates happen before full-model gradient norms are available, so exact global gradient clipping is unsupported. GPU-only cost extrapolations use dated vendor prices, not full bills or measured billion-token runs. No job, API or cloud spend was started.

## Highlights

- Mechanism trades GPU residency for host streaming
- Same-hardware Qwen comparison is vendor-reported
- Main GLM baseline differs in data and loss
- Separate matched loss test spans one short epoch
- Exact global gradient clipping is unsupported
- Costs exclude non-GPU service overhead
- No training or purchase was initiated

## Source

[Read the original story](https://nebius.com/blog/posts/layerstream-moe-fine-tuning) · [TLDR AI issue](https://tldr.tech/ai/2026-11-27)

## Related pages

[Compute and the data-center build-out](../concepts/compute-buildout.md)
