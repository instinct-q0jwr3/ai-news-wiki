#!/usr/bin/env python3
"""Build a persistent AI-news wiki from Techmeme, Hacker News and Lobsters."""
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
}
HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"

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


def parse_feed(source: str, url: str) -> list[dict]:
    root = ET.fromstring(fetch_text(url))
    items = []
    for node in root.findall(".//item"):
        title = clean(node.findtext("title"))
        link = clean(node.findtext("link"))
        description = clean(node.findtext("description"))
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


def render_daily(day: str, items: list[dict], generated: str) -> str:
    lines = [f"# IA en las noticias - {day}", "", f"Actualizado: `{generated}`", "",
             "Fuentes: Techmeme, Hacker News, Lobsters, Latent.Space y Stratechery.", ""]
    for source in ("Techmeme", "Hacker News", "Lobsters", "Latent.Space", "Stratechery"):
        source_items = [item for item in items if item["source"] == source]
        lines.extend([f"## {source}", ""])
        if not source_items:
            lines.extend(["_No se encontraron noticias que superasen el filtro._", ""])
            continue
        for item in source_items:
            signals = ", ".join(f"`{term}`" for term in item["ai_matches"][:5])
            meta = ""
            if source == "Hacker News":
                meta = f" - {item.get('score', 0)} puntos, {item.get('comments', 0)} comentarios"
            lines.extend([f"- [{item['title']}]({item['url']}){meta}", f"  - Señales IA: {signals}"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def rebuild_index() -> None:
    entries = sorted(DAILY_DIR.glob("*.md"), reverse=True)
    lines = ["# AI News Wiki", "", "Wiki acumulativa de noticias de IA.", "", "## Informes diarios", ""]
    lines += [f"- [{p.stem}](daily/{p.name})" for p in entries]
    extra = ""
    if INDEX.exists():
        # Preserve agent-maintained sections (Temas, Entidades, Tendencias, ...)
        # that live after the "Informes diarios" block.
        sections = re.split(r"(?m)^## ", INDEX.read_text())
        kept = [s for s in sections[1:] if not s.startswith("Informes diarios")]
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
        collected.extend(fetch_hn(args.hn_limit))
    except Exception as exc:
        errors.append(f"Hacker News: {exc}")
    filtered = []
    for item in dedupe(collected):
        matches = ai_matches(item, terms)
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
        log.write(f"## [{day}] ingest | {len(filtered)} noticias IA | snapshot {stamp}\n")
        if errors:
            log.write("- Errores parciales: " + "; ".join(errors) + "\n")
    print(f"{len(filtered)} AI stories written to wiki/daily/{day}.md")
    if errors:
        print("Partial errors: " + "; ".join(errors), file=sys.stderr)
    return 0 if filtered else 1


if __name__ == "__main__":
    raise SystemExit(main())
