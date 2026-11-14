import json, glob, os, sys, re
from urllib.parse import urlsplit, parse_qsl, urlencode
def norm(u):
    if not u: return ''
    p = urlsplit(u)
    path = re.sub(r'/$','',p.path)
    host = p.netloc.lower().removeprefix('www.')
    keys = {'id'} if host == 'news.ycombinator.com' else {'v'} if host.endswith('youtube.com') else set()
    query = urlencode([(k,v) for k,v in parse_qsl(p.query) if k in keys])
    return host + path + ('?' + query if query else '')
os.chdir(sys.argv[1] if len(sys.argv)>1 else '.')
snaps = sorted(glob.glob('raw/snapshots/*.json'), key=os.path.getmtime)
latest = json.load(open(snaps[-1]))
seen, seen_url, seen_title = set(), {}, {}
for s in snaps[:-1]:
    for i in json.load(open(s))['items']:
        seen.add(i['id']); seen_url[norm(i.get('url'))] = i['id']
        seen_title[(i.get('title') or '').strip().lower()] = i['id']
digested = set()
for f in glob.glob('raw/llm/digest-*.json') + glob.glob('raw/llm/weekly-*.json'):
    try: d = json.load(open(f))
    except: continue
    for sec in d.get('sections') or []: digested.update(sec.get('stories', []))
redir = set()
try:
    for r in json.load(open('raw/redirects.json')): redir.add(r['from']); redir.add(r['to'])
except: pass
new = []
for i in latest['items']:
    iid = i['id']
    if iid in seen or iid in digested or iid in redir: continue
    if os.path.exists(f"raw/llm/{iid}.json"): continue
    dup = seen_url.get(norm(i.get('url'))) or seen_title.get((i.get('title') or '').strip().lower())
    if dup:
        print('SKIP-DUP', iid, '==', dup, '|', i['title'][:70]); continue
    new.append(i)
print(len(new), "new stories")
for i in new: print(i['id'], '|', i['source'], '|', i['title'][:110])
json.dump([i['id'] for i in new], open('/tmp/new_ids.json','w'))
