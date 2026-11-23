# GhostScript CVE 2026-125396: "Upload2Shell"

_type: news-summary · created: 2026-11-22 · updated: 2026-11-23 · confidence: high_

`lobsters`

## Summary

pwn.ai's research article by Paulos Yibelo details Upload2Shell, now CVE-2026-125396, a use-after-free in Ghostscript's Type 1 font loader that the authors say gave a write-what-where primitive and let a crafted document alter the state enforcing -dSAFER to run commands as the rendering process. The article explains how ordinary features such as preview generation or cropping handed files with trusted extensions to Ghostscript through ImageMagick delegates or pixel-decoding calls, describes a WordPress-shaped proof reaching Ghostscript through Imagick's readImage with PostScript bytes named as a PDF, and lists decoder tests in which PHP GD, OpenCV, prebuilt Sharp, Jimp, Java ImageIO and Go's standard decoders did not invoke Ghostscript. Its timeline says WordPress shipped its mitigation on 12 August, Artifex authored the fix on 2 September and released 10.08.0 on 8 September, a Debian network CUPS proof was completed on 17 September, and the CVE was published on 9 November, with a Debian 13 CUPS case study promised as the first full write-up.

This is the research article behind the Upload2Shell disclosure index covered yesterday, not a separate vulnerability. The version matrix describes tested libraries rather than every product built on them, and reaching the renderer remains distinct from proven execution in any specific deployment, a distinction the authors themselves draw. The exploit chains, fix timeline and forthcoming case studies are the researchers' account; no proof of concept was reproduced or independently audited here.

## Highlights

- Full research article behind the Upload2Shell disclosure index already indexed
- CVE-2026-125396: use-after-free in Ghostscript's Type 1 font loader
- ImageMagick delegates and pixel-loading calls exposed Ghostscript indirectly
- Several common decoders did not reach Ghostscript in the authors' tests
- Fix timeline runs from WordPress's August mitigation to Ghostscript 10.08.0
- Tested library calls are not proof of exploitability in every product

## Source

[Read the original story](https://pwn.ai/upload2shell/research.html)

## Related pages

_No related entity or concept page yet._
