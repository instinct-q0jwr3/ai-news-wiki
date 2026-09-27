# "As a Language Model": Chat Template Switches LLM Self-Referential Voice

_type: news-summary · created: 2026-09-27 · updated: 2026-09-27 · confidence: high_

`hacker-news`

## Summary

Abstract: Large Language Models (LLMs) tend to add disclaimers like "I'm just an AI" when asked about something related to themselves.

In this work, we show that the chat template works like a switch - when present, it turns this disclaimer voice up and experiential voice like "I feel" down, across 8 popular open-source instruct models up to 9B parameters in size.

And conversely when the chat template is not present, it turns the disclaimer voice down and experiential voice up.

## Highlights

- The self-reports from such responses are used in debates about AI safety or self-knowledge of the models, yet what drives them is not well understood.
- Are the models telling us about themselves or rather how they are deployed?
- Inside the activations of 3 models, we find a direction that steers this behavior.
- Removing the direction in the model's activation space turns disclaimer voice down and adding it turns it up, while a random direction of the same size has little effect.
- We find that instruct models without chat template, when we add the disclaimer direction to them, disclaim like the template was there.
- Since the chat template controls the disclaimer voice of LLMs, then researchers studying self-reports or introspection of models might have a confound they need to control for.
- Our results show that there is a direction they can use to steer this voice.
- What they say doesn't come only from weights, but it is partially set by the chat template, and because of that a model's self-description shouldn't be treated literally. arXivLabs is a framework that allows collaborators to develop and…

## Source

[Read the original story](https://arxiv.org/abs/2609.25021)

## Related pages

_No related entity or concept page yet._
