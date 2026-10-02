# OpenAI has a LOT of work to do if they think Luna can compete with Jev

_type: news-summary · created: 2026-10-02 · updated: 2026-10-02 · confidence: high_

`hacker-news` `openai` `typesafe`

## Summary

Anth.us tests OpenAI's new Decisions API, announced at DevDay on September 29 in limited preview. It picks one answer from a list you define so software can branch on it, and runs on a version of GPT-6 Luna at about 150 ms a decision. The authors could not test the API itself, so they ran Luna on their Hard-Decisions benchmark as a stand-in, next to Jev, Kev and Laya.

The finding is about confidence. When Luna said it was 99% sure or more, it was right only 68% of the time, which breaks the common rule of letting an agent act alone above 99% and sending the rest to a person. OpenAI models' token probabilities look certain about almost everything, so the authors build and calibrate their own confidence score before routing on it.

## Highlights

- Decisions API: limited preview since Sept 29, picks one option from a fixed list, ~150 ms per decision.
- At 99%+ stated confidence Luna was correct 68% of the time.
- Test used a Luna model on Hard-Decisions, not the API itself; no docs exist yet to test against.
- Log-probabilities from OpenAI models look near-certain, and newer reasoning models often hide them.
- Authors recommend extracting, checking and calibrating confidence before routing on it.
- Written by a vendor that sells confidence-based call review, so the framing has a stake.

## Source

[Read the original story](https://anth.us/blog/openai-decisions-api-preview/)

## Related pages

[OpenAI](../entities/openai.md) · [TypeSafe](../entities/typesafe.md)
