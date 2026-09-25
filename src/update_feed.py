#!/usr/bin/env python3
"""Build a persistent AI-news wiki from public AI and technology news sources."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "raw" / "snapshots"
DAILY_DIR = ROOT / "wiki" / "daily"
INDEX = ROOT / "wiki" / "index.md"
LOG = ROOT / "wiki" / "log.md"
USER_AGENT = "ai-news-wiki/0.1 (+https://github.com/instinct-q0jwr3/ai-news-wiki)"

SOURCES = {
    "Techmeme": "https://www.techmeme.com/feed.xml",
    "Lobsters": "https://lobste.rs/rss",
    "Latent.Space": "https://www.latent.space/feed",
    "Stratechery": "https://stratechery.com/feed/",
    # Oscar's personal blog roll (OPML import 2026-09-26), batch 1: AI-dense feeds.
    "Simon Willison": "https://simonwillison.net/atom/everything/",
    "Marcus on AI": "https://garymarcus.substack.com/feed",
    "Ed Zitron": "https://www.wheresyoured.at/rss/",
    "Gwern": "https://gwern.substack.com/feed",
    "Dwarkesh Podcast": "https://www.dwarkesh.com/feed",
    "geohot": "https://geohot.github.io/blog/feed.xml",
    "Max Woolf": "https://minimaxir.com/index.xml",
    "Works on My Machine": "https://worksonmymachine.substack.com/feed",
    "lcamtuf": "https://lcamtuf.substack.com/feed",
    "Westenberg": "https://www.joanwestenberg.com/feed",
    "Geoffrey Litt": "https://www.geoffreylitt.com/feed.xml",
    "Experimental History": "https://www.experimental-history.com/feed",
}
HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
TLDR_AI_LATEST = "https://tldr.tech/api/latest/ai"

# Deliberately inspectable. Tune these in config/ai_terms.txt without an API key.
DEFAULT_TERMS = {
    "ai", "artificial intelligence", "machine learning", "deep learning", "llm",
    "large language model", "language model", "generative ai", "genai", "agentic",
    "ai agent", "agents", "chatgpt", "openai", "anthropic", "claude", "gemini",
    "deepmind", "mistral", "hugging face", "transformer", "diffusion model",
    "neural network", "inference", "fine-tuning", "finetuning", "embedding",
    "computer vision", "robotics", "copilot", "gpt-", "foundation model",
}


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def clean(text: str | None) -> str:
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def techmeme_original(raw_description: str) -> str | None:
    """Techmeme permalinks 403 our fetcher; the item description links the original article."""
    for match in re.finditer(r'(?i)<a\s+href="([^"]+)"', raw_description or ""):
        href = html.unescape(match.group(1))
        if "techmeme.com" not in href:
            return href
    return None


def parse_feed(source: str, url: str) -> list[dict]:
    root = ET.fromstring(fetch_text(url))
    items = []
    for node in root.findall(".//item"):
        title = clean(node.findtext("title"))
        link = clean(node.findtext("link"))
        raw_description = node.findtext("description") or ""
        description = clean(raw_description)
        if source == "Techmeme":
            link = techmeme_original(raw_description) or link
        if title and link:
            items.append({"source": source, "title": title, "url": link, "summary": description})
    if items:
        return items
    # Atom feeds (many personal blogs publish Atom only).
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for entry in root.findall(".//a:entry", ns):
        title = clean(entry.findtext("a:title", default="", namespaces=ns))
        link = ""
        for ln in entry.findall("a:link", ns):
            if ln.get("href") and ln.get("rel", "alternate") in ("alternate", ""):
                link = ln.get("href")
                break
        if not link:
            for ln in entry.findall("a:link", ns):
                if ln.get("href"):
                    link = ln.get("href")
                    break
        raw_description = (entry.findtext("a:summary", default="", namespaces=ns)
                           or entry.findtext("a:content", default="", namespaces=ns) or "")
        description = clean(raw_description)
        if title and link:
            items.append({"source": source, "title": title, "url": link, "summary": description})
    return items


def fetch_hn(limit: int) -> list[dict]:
    ids = fetch_json(HN_TOP)[:limit]
    items = []
    for item_id in ids:
        try:
            item = fetch_json(HN_ITEM.format(item_id=item_id))
        except (urllib.error.URLError, TimeoutError):
            continue
        if not item or item.get("type") != "story" or not item.get("title"):
            continue
        items.append({
            "source": "Hacker News",
            "title": clean(item["title"]),
            "url": item.get("url") or f"https://news.ycombinator.com/item?id={item_id}",
            "summary": clean(item.get("text")),
            "score": item.get("score", 0),
            "comments": item.get("descendants", 0),
        })
    return items



class _TldrLinkParser(HTMLParser):
    """Extract editorial links from TLDR AI's latest public issue page."""
    def __init__(self):
        super().__init__()
        self.current = None
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href", "")
            if href.startswith("http"):
                self.current = {"href": html.unescape(href), "text": []}

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            self.links.append((clean(" ".join(self.current["text"])), self.current["href"]))
            self.current = None


def _strip_tracking(url: str) -> str:
    parts = urlsplit(url)
    keep = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if not k.lower().startswith(("utm_", "sp"))]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(keep), parts.fragment))


def fetch_tldr_ai() -> list[dict]:
    """Fetch only TLDR AI, using its public latest-issue endpoint."""
    issue_url = TLDR_AI_LATEST
    req = urllib.request.Request(issue_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")
        issue_url = response.geturl()
    parser = _TldrLinkParser()
    parser.feed(page)
    items = []
    seen = set()
    editorial_marker = re.compile(r"\((?:\d+ minute read|github repo)\)\s*$", re.I)
    for label, url in parser.links:
        if not editorial_marker.search(label) or "sponsor" in label.lower():
            continue
        title = editorial_marker.sub("", label).strip()
        url = _strip_tracking(url)
        if not title or url in seen:
            continue
        seen.add(url)
        items.append({
            "source": "TLDR AI",
            "title": title,
            "url": url,
            "summary": f"TLDR AI selected this story in its latest issue: {title}.",
            "newsletter_url": issue_url,
        })
    return items


def load_terms() -> set[str]:
    path = ROOT / "config" / "ai_terms.txt"
    if not path.exists():
        return DEFAULT_TERMS
    custom = {line.strip().lower() for line in path.read_text().splitlines()
              if line.strip() and not line.lstrip().startswith("#")}
    return custom or DEFAULT_TERMS


def ai_matches(item: dict, terms: set[str]) -> list[str]:
    haystack = f"{item.get('title', '')} {item.get('summary', '')} {item.get('url', '')}".lower()
    return sorted(term for term in terms if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", haystack))


def dedupe(items: Iterable[dict]) -> list[dict]:
    seen, result = set(), []
    for item in items:
        normalized = re.sub(r"\W+", " ", item["title"].lower()).strip()
        key = hashlib.sha1(normalized.encode()).hexdigest()[:12]
        if key not in seen:
            seen.add(key)
            item["id"] = key
            result.append(item)
    return result


def trim_blurb(text, cap=300):
    text = re.sub(r"\s+", " ", text or "").strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    picked = " ".join(sentences[:2]).strip()
    if len(picked) > cap:
        picked = picked[: cap - 1].rsplit(" ", 1)[0] + "\u2026"
    return picked


def strip_headline_repeat(desc, title):
    def norm(t): return re.sub(r"[^a-z0-9 ]", " ", (t or "").lower())
    parts = re.split(r"\s+\u2014\s+", desc, maxsplit=1)
    if len(parts) == 2:
        a = set(norm(parts[0]).split()); b = set(norm(title).split())
        if len(a) >= 4 and b and len(a & b) / len(a) >= 0.6: return parts[1]
    return desc


def blurb_for(item):
    desc = re.sub(r"\s+", " ", item.get("summary") or "").strip()
    desc = re.sub(r"^TLDR AI selected this story in its latest issue:\s*", "", desc)
    desc = re.sub(r"^[A-Z][^.:]{1,50} :\s+", "", desc)
    title = item["title"]
    basetitle = re.sub(r"\s*\([^()]{1,60}\)\s*$", "", title)
    for t in (title, basetitle):
        if t and desc.lower().startswith(t.lower()):
            desc = desc[len(t):].lstrip(" \u2014\u2013-:|"); break
    desc = strip_headline_repeat(desc, title)
    if desc and desc.lower() != title.lower() and len(desc) > 35:
        return trim_blurb(desc)
    return f"{item['title']}."


def render_daily(day: str, items: list[dict], generated: str) -> str:
    all_sources = list(SOURCES.keys()) + ["Hacker News", "TLDR AI"]
    lines = [f"# AI in the news - {day}", "", f"Updated: `{generated}`", "",
             "Sources: " + ", ".join(all_sources) + ".", ""]
    for source in all_sources:
        source_items = [item for item in items if item["source"] == source]
        lines.extend([f"## {source}", ""])
        if not source_items:
            lines.extend(["_No stories passed the AI filter._", ""])
            continue
        for item in source_items:
            lines.extend([f"### [{item['title']}](../summaries/{item['id']}.md)", "",
                          blurb_for(item), ""])
            meta = []
            if source == "Hacker News" and (item.get("score") or item.get("comments")):
                meta.append(f"{item.get('score', 0)} points, {item.get('comments', 0)} comments")
            meta.append(f"[Original source]({item['url']})")
            lines.extend(["_" + " \u00b7 ".join(meta) + "_", ""])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def rebuild_index() -> None:
    entries = sorted(DAILY_DIR.glob("*.md"), reverse=True)
    lines = ["# AI News Wiki", "", "Cumulative AI news wiki.", "", "## Daily digests", ""]
    lines += [f"- [{p.stem}](daily/{p.name})" for p in entries]
    extra = ""
    if INDEX.exists():
        # Preserve agent-maintained sections that live after the daily digest block.
        sections = re.split(r"(?m)^## ", INDEX.read_text())
        kept = [s for s in sections[1:] if not s.startswith("Daily digests")]
        if kept:
            extra = "\n\n" + "\n\n".join("## " + s.strip() for s in kept)
    INDEX.write_text("\n".join(lines).rstrip() + extra + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hn-limit", type=int, default=100, help="HN top stories to inspect")
    args = parser.parse_args()
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    stamp, day = now.strftime("%Y%m%dT%H%M%SZ"), now.date().isoformat()
    terms = load_terms()
    collected, errors = [], []
    for source, url in SOURCES.items():
        try:
            collected.extend(parse_feed(source, url))
        except Exception as exc:
            errors.append(f"{source}: {exc}")
    try:
        collected.extend(fetch_tldr_ai())
    except Exception as exc:
        errors.append(f"TLDR AI: {exc}")
    try:
        collected.extend(fetch_hn(args.hn_limit))
    except Exception as exc:
        errors.append(f"Hacker News: {exc}")
    filtered = []
    for item in dedupe(collected):
        matches = ["tldr ai"] if item.get("source") == "TLDR AI" else ai_matches(item, terms)
        if matches:
            item["ai_matches"] = matches
            filtered.append(item)
    filtered.sort(key=lambda x: (x["source"], -x.get("score", 0), x["title"].lower()))
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = {"generated_at": now.isoformat(), "errors": errors, "items": filtered}
    (RAW_DIR / f"{stamp}.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
    (DAILY_DIR / f"{day}.md").write_text(render_daily(day, filtered, now.isoformat()))
    rebuild_index()
    with LOG.open("a") as log:
        log.write(f"## [{day}] ingest | {len(filtered)} AI stories | snapshot {stamp}\n")
        if errors:
            log.write("- Partial errors: " + "; ".join(errors) + "\n")
    print(f"{len(filtered)} AI stories written to wiki/daily/{day}.md")
    if errors:
        print("Partial errors: " + "; ".join(errors), file=sys.stderr)
    return 0 if filtered else 1


if __name__ == "__main__":
    raise SystemExit(main())
