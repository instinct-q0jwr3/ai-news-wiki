#!/usr/bin/env python3
"""Pre-publication reviewer. Runs after derive.py, before build_site.py (wired into run_pass.sh).
Fails (exit 1) if any generated content violates a standing rule:
  R1 Every daily/weekly digest page must come from an AUTHORED schema-3 digest
     (raw/llm/digest-<day>.json / raw/llm/weekly-<W>.json with >=1 sections).
     No page may fall back to the fixed CONCEPTS taxonomy.
  R2 No daily/weekly page may contain a fixed-taxonomy section header.
  R3 No summary page may render prose one character per line.
  R4 Every story id referenced by an authored digest must exist in the corpus.
  R8 Stories on the disputed-claims registry must keep their dispute marker and must not
     regress to a categorical claim while the dispute is open.
"""
import json,re,sys,glob,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def J(p):
    with open(os.path.join(ROOT,p)) as f: return json.load(f)
FIXED=['Agentic systems','Compute and the data-center build-out','AI safety incidents and controls','AI policy, regulation and litigation','External AI evaluation','Small and specialist models','AI price war','Agentic commerce','Labor displacement','AI coding agents','Agent incidents']
fails=[]
# Authored digest leads are paragraphs, never a bare string iterated as characters.
for path in glob.glob(os.path.join(ROOT,'raw/llm/digest-*.json')) + glob.glob(os.path.join(ROOT,'raw/llm/weekly-*.json')):
    data=json.load(open(path))
    if data.get('schema')==3 and 'lead' in data:
        lead=data['lead']
        if not isinstance(lead,list) or not all(isinstance(p,str) for p in lead):
            fails.append(f'R3 {os.path.basename(path)} lead must be a list of paragraphs')
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
# R7: Signal - 5 picks per day, none paywalled/thin/unreadable, ids resolve
try: _sig=json.load(open(os.path.join(ROOT,'wiki/signal_data.json')))
except Exception: _sig={}
for day,r in _sig.items():
    if len(r['picks'])!=5: fails.append(f'R7 signal/{day} has {len(r["picks"])} picks, need 5')
    for p in r['picks']:
        if p['cat']!='ok': fails.append(f'R7 signal/{day} pick {p["id"]} is {p["cat"]}, must be ok')
        if not os.path.exists(os.path.join(ROOT,'wiki/summaries',p['id']+'.md')): fails.append(f'R7 signal/{day} pick {p["id"]} does not resolve')
    if len({p['id'] for p in r['picks']})!=5: fails.append(f'R7 signal/{day} has duplicate picks')
if _sig and not os.path.exists(os.path.join(ROOT,'docs/signal/index.html')): fails.append('R7 docs/signal/index.html missing')
# R9: paywall labels - the lock marker is reserved for verified subscription/paywall sources.
# cat=='paywall' may only come from a domain in derive.py's PAYWALL_DOMAINS registry; a fetcher
# 'paywall' marker (paywall markers in page) or any technical/JS block on another domain must
# render as thin/unreadable, never as a paywall.
import re as _re9
_dm=_re9.search(r"PAYWALL_DOMAINS=\{([^}]*)\}", open(os.path.join(ROOT,'scripts/derive.py')).read())
_PAY9={d.strip().strip("'") for d in _dm.group(1).split(',') if d.strip()}
try: _ss9=json.load(open(os.path.join(ROOT,'wiki/source_status.json')))
except Exception: _ss9={}
for _i,_c in _ss9.items():
    if _c!='paywall': continue
    try:
        _cc=json.load(open(os.path.join(ROOT,'raw/cache/sources',_i+'.json')))
        _dom=_re9.sub(r'^www\.','',_re9.search(r'https?://([^/]+)',_cc.get('url','') or '').group(1)) if _cc.get('url') else ''
    except Exception: _dom=''
    if _dom not in _PAY9: fails.append(f'R9 {_i} labeled paywall but domain "{_dom}" is not in the verified PAYWALL_DOMAINS registry')
# R8: disputed-claims registry - while a claim's scope is disputed, the settled wording must not regress
# to a categorical assertion. Each entry fails the build if a forbidden categorical phrasing reappears
# OR if the dispute marker disappears (a resolved dispute requires a conscious edit of the registry).
DISPUTED=[
 {'id':'22215744d33a',
  'forbidden':[r'are all clean', r'are NOT affected', r'NOT malicious\b',
               r'NPM,? OpenVSX,? and (the )?(Microsoft |official )?VS ?Code (marketplace |extension)?builds? (are|were) unaffected'],
  'required':[r'scope outside Cursor.{0,40}(not settled|disputed|unconfirmed)'],
  'note':'Claude Code 2.1.313 incident (Oct 2026): Cursor confirmed only its own marketplace; cleanliness of NPM/OpenVSX/VSCode is asserted by one writeup but disputed by other researchers. No categorical exclusion while disputed.'},
 {'id':'d19636d7fe25',
  'forbidden':[r'are all clean', r'are NOT affected', r'NOT malicious\\b',
               r'NPM,? OpenVSX,? and (the )?(Microsoft |official )?VS ?Code (marketplace |extension)?builds? (are|were) unaffected'],
  'required':[r'beyond Cursor.{0,40}(contested|disputed|unconfirmed|not settled)'],
  'note':'Claude Code 2.1.313 incident (Oct 2026): same disputed-scope guard as 22215744d33a.'},
 {'id':'834b8a6bd154',
  'forbidden':[r'are all clean', r'are NOT affected', r'NOT malicious\\b',
               r'NPM,? OpenVSX,? and (the )?(Microsoft |official )?VS ?Code (marketplace |extension)?builds? (are|were) unaffected'],
  'required':[r'competing accounts'],
  'note':'Claude Code 2.1.313 incident (Oct 2026): same disputed-scope guard as 22215744d33a.'},
 {'id':'6c79ccb73a57',
  'forbidden':[r'are all clean', r'are NOT affected', r'NOT malicious\\b',
               r'NPM,? OpenVSX,? and (the )?(Microsoft |official )?VS ?Code (marketplace |extension)?builds? (are|were) unaffected'],
  'required':[r'Open VSX reports remain'],
  'note':'Claude Code 2.1.313 incident (Oct 2026): same disputed-scope guard as 22215744d33a.'},
]
for e in DISPUTED:
    texts=[]
    lj=os.path.join(ROOT,'raw','llm',e['id']+'.json')
    if os.path.exists(lj):
        d=json.load(open(lj))
        pr=d.get('prose'); pr=' '.join(pr) if isinstance(pr,list) else (pr or '')
        texts.append(('raw/llm/'+e['id']+'.json', pr+' '+' '.join(d.get('highlights') or [])))
    md=os.path.join(ROOT,'wiki','summaries',e['id']+'.md')
    if os.path.exists(md): texts.append(('wiki/summaries/'+e['id']+'.md', open(md).read()))
    if not texts:
        fails.append(f'R8 disputed-claim guard for {e["id"]} found no files; remove the entry consciously if the story is gone')
        continue
    for where,body in texts:
        for pat in e['forbidden']:
            if re.search(pat,body): fails.append(f'R8 {where} reintroduces categorical claim /{pat}/ on disputed story {e["id"]} ({e["note"]})')
        for pat in e['required']:
            if not re.search(pat,body): fails.append(f'R8 {where} lost the dispute marker /{pat}/ on {e["id"]} ({e["note"]})')
if fails:
    print('VERIFY CONTENT FAILED:')
    for x in fails: print(' -',x)
    sys.exit(1)
print(f'Verify OK: {len(dailies)} dailies, {len(weeklies)} weeklies, {len(glob.glob(os.path.join(ROOT,"wiki/summaries/*.md")))} summaries checked.')
