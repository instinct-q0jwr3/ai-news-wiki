# "As a Language Model": Chat Template Switches LLM Self-Referential Voice

_type: news-summary · created: 2026-09-27 · updated: 2026-09-28 · confidence: high_

`hacker-news`

## Summary

This arXiv paper shows that the chat template - the wrapper that formats prompts for instruct-tuned models - acts as a switch on how LLMs talk about themselves. With the template on, disclaimer voice ('I'm just an AI') goes up and experiential voice ('I feel') goes down; with it off, the pattern reverses. The result holds across 8 popular open-source instruct models up to 9B parameters.

The authors then find a direction in the activation space of 3 models that steers this behavior: adding it increases disclaimers, removing it suppresses them, while a random direction of equal size does little. Adding the direction to a base model without a template makes it disclaim as if the template were there. Their conclusion is a methodological warning: what a model says about itself is not a fact about its weights alone - it is partly set by deployment scaffolding - so self-reports and introspection studies have a confound they need to control for, and this direction gives them a way to do it.

## Highlights

- The chat template works like a switch on LLM self-reference: disclaimer voice up, experiential voice down - and reversed without it
- Holds across 8 open-source instruct models up to 9B parameters
- A steerable direction exists in activation space: add it, disclaimers rise; remove it, they fall
- A random direction of the same size has little effect - the direction is specific
- Base models with the direction added disclaim as if a chat template were present
- Implication: model self-reports confound weights with deployment scaffolding - don't treat self-descriptions literally
- The direction gives introspection and AI-safety researchers a control for the confound

## Source

[Read the original story](https://arxiv.org/abs/2609.25021)

## Related pages

_No related entity or concept page yet._
