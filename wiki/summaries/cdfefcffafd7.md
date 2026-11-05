# WiCi: Connecting GPUs over WiFi

_type: news-summary · created: 2026-11-03 · updated: 2026-11-05 · confidence: high_

`hacker-news` `compute-buildout`

## Summary

WiCi is a systems research lab betting on the opposite of the datacenter: wireless GPU computing for local AI. Its pitch - a dedicated inference device for homes, studios and workplaces called WiCi One, from US$2,599 - rests on three pieces of systems research: a runtime that makes GPU-over-Wi-Fi practical by caching, reusing data and executing asynchronously (GPU software issues thousands of small calls that are ruinous over Wi-Fi); InferSSD, an open-source engine that keeps model weights on SSD and streams the working set to the GPU, so oversized models run on personal hardware; and scheduling work that lets multiple applications share one GPU without duplicating weights.

There's also a voice-interaction thread - forming candidate answers while speech is still arriving, with a learned policy deciding when to respond - aimed at making local assistants feel immediate rather than batch.

The ideological framing is explicit ('local compute, direct control'), and the press quotes lean into the anti-oligarch angle. But the technical agenda is the interesting part: if a Wi-Fi-7-linked box can serve high-end GPU inference to every device in a home, the 'local AI' argument stops depending on each device having its own expensive silicon. That is a real alternative architecture to the cloud subscription - at exactly the moment the week's other stories are about $895B compute commitments.

## Highlights

- WiCi One (from $2,599): a home/studio wireless-GPU inference box serving multiple devices over Wi-Fi 7
- Three research threads: a runtime hiding Wi-Fi latency from GPU call patterns, InferSSD streaming weights from SSD, and cross-app weight sharing/scheduling
- Voice research: speculative answers formed during speech input, learned response timing
- The contrarian architecture: local shared GPU vs cloud subscription - landing amid $895B compute-commitment news

## Source

[Read the original story](https://wici.ai)

## Related pages

[Compute and the data-center build-out](../concepts/compute-buildout.md)
