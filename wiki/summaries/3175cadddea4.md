# Today's PHP Security Release, and How We're Strengthening PHP Security

_type: news-summary · created: 2026-10-21 · updated: 2026-10-29 · confidence: high_

`simon-willison` `openai` `google` `gemini` `small-specialist-models` `ai-safety-incidents` `ai-policy-regulation`

## Summary

Simon Willison's linkblog relays the PHP Foundation's post-mortem of the botched coordinated disclosure behind today's security release. The CVE IDs began circulating 20 October around 15:00 UTC with a wrong release time and a wrong CVSS of 10.0 (actually 9.2); PHP pulled its pre-announcement forward to 19:30 UTC and moved the release up a day, to 21 October 14:00 UTC. Around 20:00 UTC, Calif, one of the reporting security firms, mistakenly published a video of its proof of concept working against several targets; copies spread and accelerated independent PoC development, so exploits have circulated since last night. The timeline: Wiz Research found the first vulnerability on 19 August using Wiz Atlas with Gemini 4 Argon and GPT-5.6 Sol, confirmed unauthenticated RCE against Drupal on the 20th and WordPress on the 21st, reported to PHP on 24 August, and PHP acknowledged on 21 September. If you run anything on PHP, upgrade: the whole PHP 8.x line is patched.

## Highlights

- PHP 8.x security release fixes two RCEs; upgrade now, exploits are circulating
- Leak timeline: CVE IDs with wrong CVSS 10.0 (real: 9.2) hit forums 20 Oct
- Calif mistakenly published a PoC video; copies spread, accelerating exploits
- Found 19 Aug by Wiz Atlas with Gemini 4 Argon and GPT-5.6 Sol
- RCE confirmed on Drupal and WordPress within days; reported to PHP 24 Aug
- PHP moved disclosure up a day after the leak

## Source

[Read the original story](https://simonwillison.net/2026/Oct/21/php-security-release/)

## Related pages

[OpenAI](../entities/openai.md) · [Google](../entities/google.md) · [Google Gemini](../entities/gemini.md) · [Small and specialist models](../concepts/small-specialist-models.md) · [AI safety incidents and controls](../concepts/ai-safety-incidents.md) · [AI policy, regulation and litigation](../concepts/ai-policy-regulation.md)
