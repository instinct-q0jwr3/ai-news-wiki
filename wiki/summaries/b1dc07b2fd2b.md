# What Is RLCD? The Secret Behind Jev

_type: news-summary · created: 2026-09-24 · updated: 2026-09-24 · confidence: high_

`hacker-news` `typesafe`

## Summary

This blog post argues that Jev looks mysterious as an alternative to a language model but becomes simple when seen as the next step in reward modeling. The core idea is RLCD, a schema-conditioned Plackett-Luce objective that moves from pairwise reward modeling to calibrated, multiway decisions; Jev turns that objective into a product by adding typed outputs and parallel inference. 'The reward model is no longer hidden behind a generator. The reward model becomes the model.'

The motivation: conventional reward models map a context and candidate answer to a scalar score, but that number is not actually absolute - a reward of 0.8 has no stable meaning across problems, candidate pools, checkpoints, or model families, and is mainly useful for comparing candidates generated under similar conditions.

## Highlights

- Frames Jev as the next step in reward modeling, not an alternative LM.
- RLCD is a schema-conditioned Plackett-Luce objective: calibrated multiway decisions.
- Jev productizes it with typed outputs and parallel inference.
- 'The reward model becomes the model.'
- Conventional scalar rewards are not absolute: they shift across problems, pools, checkpoints and model families.
- Outcome reward models score final answers; process reward models score individual steps.

## Source

[Read the original story](https://di-zhang-llm.github.io/blog/what-is-rlcd-the-secret-behind-jev/)

## Related pages

[TypeSafe](../entities/typesafe.md)
