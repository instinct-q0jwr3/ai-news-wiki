# Bonsai 2 27B: Near-Lossless Compression in a 9x Smaller Footprint

_type: news-summary · created: 2026-09-25 · updated: 2026-09-26 · confidence: high_

`simon-willison` `openai` `meta` `hugging-face` `ai-safety-incidents`

## Summary

Simon Willison's practical note on Bonsai 2 27B, a ternary-compressed model claiming near-lossless quality at 9x smaller footprint: trying the GGUFs requires Prism's own llama.cpp fork, not stock llama.cpp.

He posts working commands: download the Prism macOS runtime tarball, pull the ~5.95GB Ternary-Bonsai-2-27B GGUF from Hugging Face, and run llama-server on a chosen port. The useful detail for anyone testing small-footprint models: the runtime dependency is easy to miss.

## Highlights

- Bonsai 2 27B: near-lossless compression claims at 9x smaller footprint
- The GGUFs require Prism's llama.cpp fork, not stock llama.cpp
- Willison posts the full working command sequence
- Model size ~5.95GB (PTQ1_0 GGUF on Hugging Face)
- The runtime-fork dependency is the detail testers will trip on

## Source

[Read the original story](https://simonwillison.net/2026/Sep/17/hn-49747390/)

## Related pages

[OpenAI](../entities/openai.md) · [Meta](../entities/meta.md) · [Hugging Face](../entities/hugging-face.md) · [AI safety incidents and controls](../concepts/ai-safety-incidents.md)
