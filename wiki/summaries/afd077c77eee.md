# The data black hole at the center of AI

_type: news-summary · created: 2026-09-25 · updated: 2026-09-28 · confidence: high_

`dwarkesh-podcast`

## Summary

Dwarkesh Patel's essay argues that the real engine of AI progress is data, not sample efficiency. If intelligence is how little data you need to become fluent in a domain, then models have barely improved - they are simply fed vastly more and better data. RL is best understood as synthetic data generation: burn compute against a verifier to find good trajectories, then train on them. That in turn demands 'mind-stretching' volumes of bespoke human expert work - hundreds of specialists per skill writing example completions, rubrics and chains of thought - which is why the data industry behind it earns billions and heads for deca-billions.

This framing explains why open models sit only about four months behind the frontier: data can be distilled from public APIs, while architectures and training tricks cannot - if those drove progress, catch-up would be slower. The scale gap is stark: a human sees perhaps 200 million tokens by adulthood; frontier models train on tens to hundreds of trillions, a million-fold difference. A teenager drives after 20 hours of practice; Waymo and Tesla needed orders of magnitude more. To the objection that evolution is our pre-training, he answers that the 3GB genome can't store the parameters - evolution found the hyperparameters and loss functions, not the weights. The image he leaves: a galaxy of capabilities held together by an invisible black hole of data at its center.

## Highlights

- One definition of intelligence is sample efficiency - and on that measure, models have barely progressed
- Progress comes from more and better data; RL is synthetic data generation against verifiers
- RL still needs the model to assign some prior probability to the correct solution, so expert human trajectories are indispensable
- Data vendors hire hundreds of specialists per skill - Word polishers, M&A diligence writers, consultants - to author completions and rubrics
- Models grind thousands of rollouts per task where a human student practices once or twice
- Open models lag the frontier by ~4 months because data distills through public APIs while training tricks don't transfer
- Scale gap: ~200M tokens in a human lifetime vs tens to hundreds of trillions for a frontier model - a million-fold difference
- Robotics and driving as evidence: humans teleoperate a robot arm in hours or drive after 20 hours of practice
- Rebuttal to 'evolution is pre-training': the 3GB genome is too small to hold the weights - it encodes the learning algorithm, not the knowledge

## Source

[Read the original story](https://www.dwarkesh.com/p/the-sample-efficiency-black-hole)

## Related pages

_No related entity or concept page yet._
