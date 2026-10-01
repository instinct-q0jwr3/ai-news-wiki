#!/usr/bin/env python3
"""Pre-publication reviewer. Runs after derive.py, before build_site.py (wired into run_pass.sh).
Fails (exit 1) if any generated content violates a standing rule:
  R1 Every daily/weekly digest page must come from an AUTHORED schema-3 digest
     (raw/llm/digest-<day>.json / raw/llm/weekly-<W>.json with >=1 sections).
     No page may fall back to the fixed CONCEPTS taxonomy.
  R2 No daily/weekly page may contain a fixed-taxonomy section header.
  R3 No summary page may render prose one character per line.
  R4 Every story id referenced by an authored digest must exist in the corpus.
"""
import json,re,sys,glob,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def J(p):
    with open(os.path.join(ROOT,p)) as f: return json.load(f)
FIXED=['Agentic systems','Compute and the data-center build-out','AI safety incidents and controls','AI policy, regulation and litigation','External AI evaluation','Small and specialist models','AI price war','Agentic commerce','Labor displacement','AI coding agents','Agent incidents']
fails=[]
# R1+R2: digests
dailies=sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(ROOT,'wiki/daily/*.md')))
weeklies=sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(ROOT,'wiki/weekly/*.md')))
for day in dailies:
    f=os.path.join(ROOT,'raw','llm',f'digest-{day}.json')
    ok=False
    if os.path.exists(f):
        try:
            d=J(f'raw/llm/digest-{day}.json'); ok=d.get('schema')==3 and len(d.get('sections') or [])>=1
        except Exception: ok=False
    if not ok: fails.append(f'R1 daily/{day}.md has no authored schema-3 digest (raw/llm/digest-{day}.json)')
    body=open(os.path.join(ROOT,'wiki','daily',day+'.md')).read()
    for label in FIXED:
        if f'## {label}' in body: fails.append(f'R2 daily/{day}.md uses fixed-taxonomy section "{label}"')
for w in weeklies:
    f=os.path.join(ROOT,'raw','llm',f'weekly-{w}.json')
    ok=False
    if os.path.exists(f):
        try:
            d=J(f'raw/llm/weekly-{w}.json'); ok=d.get('schema')==3 and len(d.get('sections') or [])>=1
        except Exception: ok=False
    if not ok: fails.append(f'R1 weekly/{w}.md has no authored schema-3 digest (raw/llm/weekly-{w}.json)')
    body=open(os.path.join(ROOT,'wiki','weekly',w+'.md')).read()
    for label in FIXED:
        if f'## {label}' in body: fails.append(f'R2 weekly/{w}.md uses fixed-taxonomy section "{label}"')
# R3: letter-spaced summaries
single=re.compile(r'^[A-Za-z]$')
for p in glob.glob(os.path.join(ROOT,'wiki/summaries/*.md')):
    n=sum(1 for line in open(p) if single.match(line.strip()))
    if n>=8: fails.append(f'R3 {os.path.relpath(p,ROOT)} renders prose one character per line ({n} single-char lines)')
# R4: digest story ids exist in corpus
ids=set()
for p in glob.glob(os.path.join(ROOT,'raw/snapshots/*.json')):
    for it in J(os.path.relpath(p,ROOT)).get('items',[]):
        if it.get('id'): ids.add(it['id'])
for f in sorted(glob.glob(os.path.join(ROOT,'raw/llm/digest-*.json')))+sorted(glob.glob(os.path.join(ROOT,'raw/llm/weekly-*.json'))):
    try: d=json.load(open(f))
    except Exception: continue
    for sec in d.get('sections') or []:
        for sid in sec.get('stories',[]):
            if sid not in ids: fails.append(f'R4 {os.path.basename(f)} section "{sec.get("title")}" references unknown story id {sid}')
# R5: entity pages need >=1 timeline event and must not be a feed/source name
try:
    _feeds={r['name'].lower() for r in json.load(open(os.path.join(ROOT,'wiki/feeds.json')))}
except Exception: _feeds=set()
for p in glob.glob(os.path.join(ROOT,'wiki/entities/*.md')):
    t=open(p).read(); nm=t.splitlines()[0][2:].strip().lower()
    if '\n- **' not in t: fails.append(f'R5 entity {os.path.basename(p)} has no timeline events')
    if nm in _feeds: fails.append(f'R5 entity {os.path.basename(p)} is a feed/source name')
# R6: completeness - every authored section/story that belongs to a day must be rendered
import re as _re
def _created(i):
    try: return _re.search(r'created: (\d{4}-\d{2}-\d{2})',open(os.path.join(ROOT,'wiki/summaries',i+'.md')).read()).group(1)
    except Exception: return None
for f in sorted(glob.glob(os.path.join(ROOT,'raw/llm/digest-*.json'))):
    try: d=json.load(open(f))
    except Exception: continue
    if d.get('schema')!=3: continue
    day=d.get('date') or os.path.basename(f)[7:-5]
    pg=os.path.join(ROOT,'wiki/daily',day+'.md')
    if not os.path.exists(pg): continue
    md=open(pg).read(); linked=set(_re.findall(r'summaries/([0-9a-f]{12})\.md',md)); heads={h.strip() for h in _re.findall(r'^## (.+)$',md,flags=_re.M)}
    for sec in d.get('sections') or []:
        mine=[i for i in sec.get('stories',[]) if _created(i)==day]
        if mine and sec.get('title','').strip() not in heads: fails.append(f'R6 daily/{day}.md is missing authored section "{sec.get("title")}"')
        for i in mine:
            if i not in linked: fails.append(f'R6 daily/{day}.md does not render authored story {i} (section "{sec.get("title")}")')
if fails:
    print('VERIFY CONTENT FAILED:')
    for x in fails: print(' -',x)
    sys.exit(1)
print(f'Verify OK: {len(dailies)} dailies, {len(weeklies)} weeklies, {len(glob.glob(os.path.join(ROOT,"wiki/summaries/*.md")))} summaries checked.')
