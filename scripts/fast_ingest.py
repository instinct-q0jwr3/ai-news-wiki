#!/usr/bin/env python3
"""Parallel-feed version of src/update_feed.py main(): identical outputs,
fetches all RSS feeds concurrently (16 workers). Run from repo root."""
import sys, json, datetime as dt
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'src')
import update_feed as uf

def main():
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    stamp, day = now.strftime("%Y%m%dT%H%M%SZ"), now.date().isoformat()
    terms = uf.load_terms()
    collected, errors = [], []
    def one(src_url):
        source, url = src_url
        try: return uf.parse_feed(source, url), None
        except Exception as exc: return [], f"{source}: {exc}"
    with ThreadPoolExecutor(16) as ex:
        for items, err in ex.map(one, uf.SOURCES.items()):
            collected.extend(items)
            if err: errors.append(err)
    try: collected.extend(uf.fetch_tldr_ai())
    except Exception as exc: errors.append(f"TLDR AI: {exc}")
    try: collected.extend(uf.fetch_hn(100))
    except Exception as exc: errors.append(f"Hacker News: {exc}")
    filtered = []
    for item in uf.dedupe(collected):
        matches = ["tldr ai"] if item.get("source") == "TLDR AI" else uf.ai_matches(item, terms)
        if matches:
            item["ai_matches"] = matches
            filtered.append(item)
    filtered.sort(key=lambda x: (x["source"], -x.get("score", 0), x["title"].lower()))
    uf.RAW_DIR.mkdir(parents=True, exist_ok=True)
    uf.DAILY_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = {"generated_at": now.isoformat(), "errors": errors, "items": filtered}
    (uf.RAW_DIR / f"{stamp}.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
    (uf.DAILY_DIR / f"{day}.md").write_text(uf.render_daily(day, filtered, now.isoformat()))
    uf.rebuild_index()
    with uf.LOG.open("a") as log:
        log.write(f"## [{day}] ingest | {len(filtered)} AI stories | snapshot {stamp}\n")
        if errors: log.write("- Partial errors: " + "; ".join(errors) + "\n")
    print(f"{len(filtered)} AI stories written to wiki/daily/{day}.md snapshot {stamp}")
    return 0 if filtered else 1

if __name__ == "__main__":
    raise SystemExit(main())
