#!/usr/bin/env python3
"""Parallel cache warmer replicating scripts/derive.py enrich_sources per-item logic.
Uncached stories first (8 workers), then stale error caches past TTL (24 workers).
Run from repo root after ingest, before derive, so derive finds all caches warm."""
import sys, json, glob, os, time, datetime as dt
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'scripts')
import derive as D

def corpus():
    seen, xs = set(), []
    for s in sorted(glob.glob('raw/snapshots/*.json'), key=os.path.getmtime):
        for i in json.load(open(s))['items']:
            if i['id'] not in seen:
                seen.add(i['id']); xs.append(i)
    return xs

def stale_error(x):
    f = D.CACHE / f"{x['id']}.json"
    if not f.exists(): return False
    try: c = json.loads(f.read_text())
    except Exception: return True
    if not (c.get('url') == x.get('url') or c.get('feed_url') == x.get('url')): return True
    if c.get('status') in ('ok', 'thin'): return False
    try: age = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(c.get('fetched_at',''))).total_seconds()
    except Exception: age = 1e9
    ttl = 604800 if c.get('block') in ('bot-block','paywall') else 3600
    return c.get('status') == 'error' and age >= ttl

def fetch_one(x):
    url = x.get('url', '')
    if not url.startswith('http'): return ('error', 'no-url')
    body, err, kind = None, None, None
    for attempt in (1, 2):
        try: body, err, kind = D.fetch_url(url)
        except Exception as e: body, err, kind = None, str(e)[:160], 'error'
        if body: break
        time.sleep(0.2)
    if not body:
        D.save_entry(x, 'error', '', err or 'fetch failed', kind)
        return ('error', kind)
    text = D.html_to_text(body)
    if text:
        probe = text[:2000]
        bad = sum(1 for ch in probe if (ord(ch) < 32 and ch not in '\n\t') or ord(ch) == 0xfffd)
        if bad / max(len(probe), 1) > 0.05:
            D.save_entry(x, 'error', '', 'non-text or compressed response body')
            return ('error', 'non-text')
    if len(text) < 400:
        kind2 = D.classify_block(body, None)
        if kind2 == 'paywall':
            D.save_entry(x, 'thin', text, 'paywall markers in page', 'paywall')
        else:
            D.save_entry(x, 'thin', text, 'extracted text under 400 chars')
        return ('thin', kind2)
    D.save_entry(x, 'ok', text, '')
    return ('ok', None)

def main():
    xs = corpus()
    uncached = [x for x in xs if not (D.CACHE / f"{x['id']}.json").exists()]
    print(f"uncached new={len(uncached)}", flush=True)
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(fetch_one, uncached))
    stale = [x for x in xs if stale_error(x)]
    print(f"stale errors={len(stale)}", flush=True)
    from collections import Counter
    res = Counter()
    with ThreadPoolExecutor(24) as ex:
        for r, k in ex.map(fetch_one, stale): res[r] += 1
    print('done', dict(res), flush=True)
    left = [x for x in xs if not (D.CACHE / f"{x['id']}.json").exists()]
    print('remaining uncached:', len(left))

if __name__ == '__main__':
    main()
