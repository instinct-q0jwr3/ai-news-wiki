# The architecture of open-weight LLMs: MoE, hybrid layers, ternary weights

_type: news-summary · created: 2026-11-05 · updated: 2026-11-08 · confidence: high_

`hacker-news`

## Summary

Silas Liu's study examines the architectures of twelve open-weight models, 1.7B to 35B parameters, that run on an 8 GB GPU. Each architecture is framed by the cost it cuts: attention variants shrink the KV cache, mixture of experts reduces compute per token, recurrent layers and short convolutions replace most attention, and quantization and ternary weights shrink every weight. It then follows a request through the server, from the startup KV-cache reservation through prefill and decode, showing what each step reads from VRAM and RAM and what limits speed. Motivation: the model variety is far greater than a year ago.

## Highlights

- Twelve open-weight models, 1.7B-35B, fit an 8 GB GPU
- Each design trick maps to a cost: KV cache, compute, weight size
- Traces a request through prefill and decode and the VRAM/RAM limits
- Useful explainer rather than new research

## Source

[Read the original story](https://www.silasdata.com/llm-playground-inside-architectures/)

## Related pages

_No related entity or concept page yet._
