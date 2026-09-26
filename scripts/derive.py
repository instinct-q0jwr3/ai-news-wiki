#!/usr/bin/env python3
"""Regenerate story summaries and contextual, cross-linked wiki pages."""
from __future__ import annotations
import datetime as dt, json, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; WIKI=ROOT/'wiki'; RAW=ROOT/'raw'/'snapshots'

ENTITY_DEFS={
 'openai':('OpenAI','organization',['openai','chatgpt','gpt-','codex','sora'],'OpenAI develops frontier AI models and products, including the GPT, ChatGPT and Codex families. This page follows its model releases, agent products, partnerships, business moves, evaluations and safety record.'),
 'anthropic':('Anthropic','organization',['anthropic','claude'],'Anthropic develops the Claude model family and related coding and agent products. This page tracks its research, releases, enterprise strategy, evaluations and safety work.'),
 'google':('Google','organization',['google','gemini','deepmind'],'Google builds AI across Google DeepMind, Gemini and its consumer and cloud products. This page connects model research, product launches, infrastructure and policy developments.'),
 'microsoft':('Microsoft','organization',['microsoft','copilot','azure'],'Microsoft develops and distributes AI through Azure, Copilot, research and major model partnerships. This page follows product, infrastructure, investment and governance developments.'),
 'meta':('Meta','organization',['meta','llama'],'Meta develops open-weight Llama models and deploys AI across its social products. This page follows releases, infrastructure, research, business strategy and governance.'),
 'apple':('Apple','organization',['apple','siri'],'Apple integrates AI into devices and services, with an emphasis on on-device processing and privacy. This page follows model work, product changes, partnerships and deployment constraints.'),
 'alibaba':('Alibaba','organization',['alibaba','qwen'],'Alibaba develops the Qwen model family and AI cloud services. This page follows model releases, agent capabilities, open-weight strategy and commercial deployment.'),
 'hugging-face':('Hugging Face','organization',['hugging face','huggingface'],'Hugging Face operates a major platform for models, datasets and open AI tooling. This page follows releases, research, community infrastructure and open-source policy.'),
}
CONCEPTS={
 'agentic-systems':('Agentic systems',['agent','agentic','tool call','computer use','claude code','agents.md'],'Systems that plan or act through tools. This page tracks architecture, control, observability and adoption.'),
 'external-evaluation':('External AI evaluation',['evaluat','metr','redwood','apollo','aef-1','benchmark'],'Methods used by third parties, standards groups and labs to measure model capability, reliability and risk.'),
 'small-specialist-models':('Small and specialist models',['small model','local-llm','local llm','needle','system one','cua-s1','edge','on-device'],'Narrow or compact models trade breadth for lower cost, latency, privacy or local control.'),
 'ai-safety-incidents':('AI safety incidents and controls',['safety','security','hack','misalign','kill-switch','hallucin','collusion','guardrail'],'A connected record of reported failures, attacks and control proposals. A reported incident does not by itself establish a general risk.'),
}
COMPARISONS={
 'openai-vs-anthropic':('OpenAI vs Anthropic',['openai','gpt-','chatgpt','codex'],['anthropic','claude'],'A running comparison of launches, pricing, business, evaluation and safety. It preserves evidence from both sides rather than declaring a winner.'),
 'generalist-vs-specialist-models':('Generalist vs specialist models',['gpt','claude','gemini','foundation model'],['needle','cua-s1','small model','specialist','local-llm'],'Generalist models maximize breadth and reasoning; specialists optimize cost, latency or a narrow and verifiable action surface.'),
 'open-agents-vs-closed-platforms':('Open agents vs closed platforms',['open source','github','local','agents.md'],['openai','anthropic','salesforce','meta'],'This comparison connects the control and auditability of open agents with the integration and capability of hosted platforms.'),
}


def _load_overlay(name):
    f=ROOT/'raw'/'llm'/name
    if f.exists():
        try: return json.loads(f.read_text())
        except Exception: return {}
    return {}

# Curated overlays (LLM-authored each pass): raw/llm/entities.json, concepts.json, hubs.json.
# Hardcoded definitions win on slug conflicts.
for _slug,_d in _load_overlay('entities.json').items():
    if _slug not in ENTITY_DEFS:
        ENTITY_DEFS[_slug]=(_d['name'],_d.get('kind','organization'),_d['terms'],_d['overview'])
for _slug,_d in _load_overlay('concepts.json').items():
    if _slug not in CONCEPTS:
        CONCEPTS[_slug]=(_d['name'],_d['terms'],_d['overview'])

import html as _html, time, urllib.request

CACHE=ROOT/'raw'/'cache'/'sources'
FETCH_BUDGET_S=420; FETCH_DELAY_S=0.8; MAX_FETCHES=150; MAX_TEXT=60000
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.9'}
PAYWALL_DOMAINS={'wsj.com','ft.com','bloomberg.com','nytimes.com','theinformation.com','science.org','sfchronicle.com','theathletic.com','washingtonpost.com','economist.com','newyorker.com','thetimes.co.uk','latimes.com','hbr.org','foreignaffairs.com','theatlantic.com','technologyreview.com','statnews.com','barrons.com','afr.com','theaustralian.com.au','bizjournals.com','seekingalpha.com'}
WALL_MARKERS=re.compile(r'subscribe to (continue|keep reading|read)|subscription (is )?required|sign in to continue|already a subscriber|this (article|story|content) is for (our )?(subscribers|members)|premium (article|content)|create a free account|to keep reading,? (please )?(sign in|subscribe|register)|unlock this article|behind a paywall|support (our|independent) journalism',re.I)
BOTBLOCK_MARKERS=re.compile(r'cf-chl|just a moment|verify you are a human|checking your browser|are you a robot|attention required|access denied|px-captcha|perimeterx|datadome|request blocked',re.I)
def classify_block(body,http_code=None):
    seg=(body or '')[:60000]
    if WALL_MARKERS.search(seg): return 'paywall'
    if http_code in (401,402,403) or BOTBLOCK_MARKERS.search(seg): return 'bot-block'
    return 'error'
SOURCES={}; RICH={}; NEW_IDS=set(); NEW_STORIES=[]; LATEST_DAY=''; MERGED={}

STOPWORDS=set('a an the and or but if then else when at by for with about into through during before after above below to from up down in out on off over under again further once here there all any both each few more most other some such no nor not only own same so than too very can will just should now is are was were be been being have has had having do does did doing would could ought i you he she it we they them his her its our their this that these those am of as'.split())
JUNK=re.compile(r'cookie|subscribe|sign[ -]?up|newsletter|all rights reserved|advertisement|terms of service|privacy policy|follow us|share this|enable javascript|verify you are|listen to this post|watch on youtube|listen to podcast|views\s+\d+\s+replies|\d+\s+reposts?\b.{0,12}\blikes\b',re.I)

class _RedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_308(self,req,fp,code,msg,headers):
        return self.http_error_301(req,fp,301,msg,headers)
_opener=urllib.request.build_opener(_RedirectHandler)

def fetch_url(url):
    req=urllib.request.Request(url,headers=UA)
    try:
        with _opener.open(req,timeout=10) as r:
            ct=r.headers.get('content-type','')
            if 'html' not in ct: return None,f'unsupported content-type: {ct}','error'
            raw=r.read(1500000)
        return raw.decode('utf-8','replace'),None,None
    except urllib.error.HTTPError as e:
        try: seg=e.read(60000).decode('utf-8','replace')
        except Exception: seg=''
        return None,f'HTTP {e.code}',classify_block(seg,e.code)
    except Exception as e:
        return None,str(e)[:160],'error'

def html_to_text(h):
    h=re.sub(r'(?is)<(script|style|noscript|svg|form|nav|footer|header|aside|iframe)[^>]*>.*?</\1>',' ',h)
    m=re.search(r'(?is)<article[^>]*>(.*?)</article>',h)
    seg=m.group(1) if m else h
    ps=re.findall(r'(?is)<p[^>]*>(.*?)</p>',seg)
    bq=re.findall(r'(?is)<blockquote[^>]*>(.*?)</blockquote>',seg)
    if bq: ps=bq+ps
    txt='\n\n'.join(ps) if len(ps)>=3 else seg
    txt=_html.unescape(re.sub(r'(?s)<[^>]+>',' ',txt))
    return re.sub(r'\s+',' ',txt).strip()

def cache_entry(x):
    CACHE.mkdir(parents=True,exist_ok=True)
    f=CACHE/f"{x['id']}.json"
    if f.exists():
        try: c=json.loads(f.read_text())
        except Exception: c=None
        if c and (c.get('url')==x.get('url') or c.get('feed_url')==x.get('url')):
            if c.get('status') in ('ok','thin'): return c,True
            try: age=(dt.datetime.now(dt.timezone.utc)-dt.datetime.fromisoformat(c.get('fetched_at',''))).total_seconds()
            except Exception: age=1e9
            if c.get('status')=='error' and age<86400: return c,True
    return None,False

def save_entry(x,status,text,note='',kind=None):
    d={'url':x.get('url'),'fetched_at':dt.datetime.now(dt.timezone.utc).isoformat(),'status':status,'note':note,'text':text[:MAX_TEXT]}
    if kind: d['block']=kind
    (CACHE/f"{x['id']}.json").write_text(json.dumps(d,ensure_ascii=False))

def enrich_sources(xs):
    stats={'cache_hit':0,'fetched_ok':0,'fetched_thin':0,'fetch_error':0,'budget_skipped':0}
    start=time.monotonic(); fetches=0
    for x in xs:
        url=x.get('url','')
        if not url.startswith('http'): SOURCES[x['id']]={}; stats['fetch_error']+=1; continue
        c,cached=cache_entry(x)
        if cached: SOURCES[x['id']]=c; stats['cache_hit']+=1; continue
        if fetches>=MAX_FETCHES or time.monotonic()-start>FETCH_BUDGET_S:
            SOURCES[x['id']]={}; stats['budget_skipped']+=1; continue
        fetches+=1; time.sleep(FETCH_DELAY_S)
        body,err,kind=None,None,None
        for attempt in (1,2):
            try: body,err,kind=fetch_url(url)
            except Exception as e: body,err,kind=None,str(e)[:160],'error'
            if body: break
            time.sleep(FETCH_DELAY_S)
        if not body:
            save_entry(x,'error','',err or 'fetch failed',kind); SOURCES[x['id']]={'status':'error','block':kind}; stats['fetch_error']+=1; continue
        text=html_to_text(body)
        if text:
            probe=text[:2000]; bad=sum(1 for ch in probe if (ord(ch)<32 and ch not in '\n\t') or ord(ch)==0xfffd)
            if bad/max(len(probe),1)>0.05:
                save_entry(x,'error','','non-text or compressed response body'); SOURCES[x['id']]={'status':'error'}; stats['fetch_error']+=1; continue
        if len(text)<400:
            kind2=classify_block(body,None)
            if kind2=='paywall':
                save_entry(x,'thin',text,'paywall markers in page','paywall'); SOURCES[x['id']]={'status':'thin','text':text,'block':'paywall'}
            else:
                save_entry(x,'thin',text,'extracted text under 400 chars'); SOURCES[x['id']]={'status':'thin','text':text}
            stats['fetched_thin']+=1
        else:
            save_entry(x,'ok',text); SOURCES[x['id']]={'status':'ok','text':text}; stats['fetched_ok']+=1
    print('Source fetch: '+', '.join(f'{k}={v}' for k,v in stats.items()))

def sentences_of(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"“\'])',text) if s.strip()]

def words_of(s): return re.findall(r"[a-zA-Z][a-zA-Z\-']+",s)

def summarize_article(text,title):
    cand=[]
    for i,s in enumerate(sentences_of(text)):
        s=re.sub(r'\s+',' ',s).strip(); w=words_of(s)
        if not (8<=len(w)<=55) or JUNK.search(s) or s.isupper(): continue
        cand.append((i,s))
    if len(cand)<3: return None
    freq=Counter(w for w in (w.lower() for w in words_of(text)) if w not in STOPWORDS and len(w)>3)
    if not freq: return None
    maxf=max(freq.values()); twords={w.lower() for w in words_of(title)}-STOPWORDS
    scored=[]
    for i,s in cand:
        ws=[w.lower() for w in words_of(s)]
        sc=sum(freq.get(w,0)/maxf for w in ws)/len(ws)+0.6/(1+i*0.15)+0.25*len(twords&set(ws))/max(1,len(twords) or 1)
        scored.append((sc,i,s))
    early=[x for x in scored if x[1]<12] or scored
    prose_pick=sorted(sorted(early,key=lambda x:-x[0])[:3],key=lambda x:x[1])
    used={i for _,i,_ in prose_pick}
    hl=[]; seen=[]
    for sc,i,s in sorted((x for x in scored if x[1] not in used),key=lambda x:-x[0]):
        key={w.lower() for w in words_of(s)}-STOPWORDS
        if any(len(key&k)/max(1,len(key|k))>0.6 for k in seen): continue
        seen.append(key); hl.append((i,s))
        if len(hl)>=8: break
    def trim(s):
        return (s[:237].rsplit(' ',1)[0]+'…') if len(s)>240 else s
    prose=[trim(s) for _,_,s in prose_pick]
    highlights=[trim(s) for _,s in sorted(hl)] if len(hl)>=3 else []
    return {'prose':prose,'highlights':highlights}

def rich_summary(x):
    e=SOURCES.get(x.get('id')) or {}
    base=esc(x.get('summary'))
    base=re.sub(r'^TLDR AI selected this story in its latest issue:\s*','',base)
    base=base+' ' if base else ''
    text=(base+(e.get('text','') if e.get('status') in ('ok','thin') else '')).strip()
    if len(text)<200: return None
    return summarize_article(text[:MAX_TEXT],x.get('feed_title') or x.get('title',''))

def esc(text): return re.sub(r'\s+',' ',str(text or '')).strip()

def md_label(text):
    return esc(text).replace('[','').replace(']','')
def corpus_text(x): return ((x.get('feed_title') or x.get('title',''))+' '+x.get('title','')+' '+x.get('summary','')).lower()
def match(xs,terms): return [x for x in xs if any(t in corpus_text(x) for t in terms)]
def fmt_date(value): return (value or '')[:10] or dt.date.today().isoformat()
def metadata(kind,created,updated,confidence='medium',tags=()):
    tag_line=' '.join(f'`{t}`' for t in tags)
    return f'_type: {kind} · created: {created} · updated: {updated} · confidence: {confidence}_\n\n{tag_line}'.rstrip()

def compute_new():
    global NEW_IDS,NEW_STORIES,LATEST_DAY
    snaps=sorted(RAW.glob('*.json'))
    if not snaps: return
    latest=json.loads(snaps[-1].read_text()); LATEST_DAY=latest.get('generated_at','')[:10]
    latest_ids={x.get('id') for x in latest.get('items',[]) if x.get('id')}
    prev=set()
    for q in snaps[:-1]:
        prev.update(x.get('id') for x in json.loads(q.read_text()).get('items',[]) if x.get('id'))
    NEW_IDS=latest_ids-prev
    by_id={}
    for q in snaps:
        for x in json.loads(q.read_text()).get('items',[]):
            if x.get('id'): by_id[x['id']]=x
    NEW_STORIES=sorted((by_id[i] for i in NEW_IDS if i in by_id),key=lambda x:-x.get('score',0))
    seen_keep=set(); remapped=[]
    for x in NEW_STORIES:
        kid=MERGED.get(x['id'],{}).get('to',x['id'])
        if kid in seen_keep or kid not in by_id: continue
        seen_keep.add(kid); remapped.append(by_id[kid])
    NEW_STORIES=remapped
    state={'generated_at':latest.get('generated_at',''),'stories':[{'id':x['id'],'title':short_title(x),'source':x.get('source',''),'url':x.get('url','')} for x in NEW_STORIES]}
    (WIKI/'new.json').write_text(json.dumps(state,ensure_ascii=False,indent=1))

from urllib.parse import urlsplit,parse_qsl,urlencode
def canon_url(u):
    u=(u or '').strip()
    if not u: return ''
    u=u.split('#')[0]
    try: parts=urlsplit(u)
    except Exception: return u.lower().rstrip('/')
    host=parts.netloc.lower()
    if host.startswith('www.'): host=host[4:]
    path=parts.path.rstrip('/') or '/'
    q=''
    if host=='news.ycombinator.com':
        q=urlencode([(k,v) for k,v in parse_qsl(parts.query) if k=='id'])
    elif host.endswith('youtube.com'):
        q=urlencode([(k,v) for k,v in parse_qsl(parts.query) if k=='v'])
    return f'{host}{path}'+(f'?{q}' if q else '')

def _ttoks(t):
    return set(re.sub(r'[^a-z0-9 ]',' ',(t or '').lower()).split())

def url_specific(cu):
    p=cu.split('?',1)[0]; i=p.find('/')
    if i<0: return False
    path=p[i:]; segs=[s for s in path.split('/') if s]
    return len(segs)>=2 and len(path)>=12

def titles_alike(a,b):
    ta,tb=_ttoks(a),_ttoks(b)
    if not ta or not tb: return False
    inter=len(ta&tb); small=min(len(ta),len(tb))
    return inter/max(1,len(ta|tb))>=0.5 or (small>=2 and inter/small>=0.8)

def load_stories():
    rows={}
    for p in sorted(RAW.glob('*.json')):
        data=json.loads(p.read_text()); seen_at=data.get('generated_at','')
        for raw in data.get('items',[]):
            x=dict(raw); key=x.get('id') or re.sub(r'\W+',' ',x.get('title','').lower()).strip()
            if key not in rows:
                x['first_seen']=seen_at; x['last_seen']=seen_at; rows[key]=x
            else:
                old=rows[key]; old['last_seen']=max(old.get('last_seen',''),seen_at)
                if len(esc(x.get('summary'))) > len(esc(old.get('summary'))): old['summary']=x['summary']
                if x.get('score',0)>old.get('score',0): old['score']=x['score']; old['comments']=x.get('comments',0)
    by_url={}
    for key,x in rows.items():
        cu=canon_url(x.get('url'))
        if cu: by_url.setdefault(cu,[]).append(key)
    for cu,keys in by_url.items():
        if len(keys)<2: continue
        keys.sort(key=lambda k:(rows[k].get('first_seen',''),k))
        keep=rows[keys[0]]
        for k in keys[1:]:
            dup=rows[k]
            if not titles_alike(keep.get('feed_title') or keep.get('title'), dup.get('feed_title') or dup.get('title')) and not url_specific(cu): continue
            if dup.get('id') and keep.get('id'): MERGED[dup['id']]={'to':keep['id'],'title':short_title(dup)}
            keep['last_seen']=max(keep.get('last_seen',''),dup.get('last_seen',''))
            keep['first_seen']=min(keep.get('first_seen',''),dup.get('first_seen',''))
            if len(esc(dup.get('summary')))>len(esc(keep.get('summary'))): keep['summary']=dup['summary']
            if dup.get('score',0)>keep.get('score',0): keep['score']=dup['score']; keep['comments']=dup.get('comments',0)
            del rows[k]
    xs=list(rows.values()); stamp=max((x.get('last_seen','') for x in xs),default='')
    red=[{'from':k,'to':v['to'],'title':v['title']} for k,v in sorted(MERGED.items())]
    (RAW.parent/'redirects.json').write_text(json.dumps(red,ensure_ascii=False,indent=1))
    return xs,stamp

def story_summary(x):
    r=RICH.get(x.get('id'))
    if r and r['prose']: return r['prose'][0]
    desc=esc(x.get('summary')); title=esc(x.get('feed_title') or x.get('title')); dtitle=esc(x.get('title'))
    desc=re.sub(r'^TLDR AI selected this story in its latest issue:\s*','',desc)
    desc=re.sub(r'^[A-Z][^.:]{1,50} :\s+','',desc)
    basetitle=re.sub(r'\s*\([^()]{1,60}\)\s*$','',title)
    for t in (title,basetitle):
        if t and desc.lower().startswith(t.lower()):
            desc=desc[len(t):].lstrip(' \u2014\u2013-:|'); break
    desc=strip_headline_repeat(desc,title)
    if desc and desc.lower()!=title.lower() and len(desc)>35:
        desc=re.sub(r'^(?:[A-Z][^:]{1,60} / [^:]{1,60} :\s*)', '', desc)
        sentences=re.split(r'(?<=[.!?])\s+',desc)
        picked=' '.join(sentences[:2]).strip()
        if len(picked)>520: picked=picked[:517].rsplit(' ',1)[0]+'…'
        return picked if re.search(r"[.!?…][\"'‘’“”)]?$",picked) else picked+'.'
    return f'{dtitle}. {x.get("source","The source feed")} selected it as an AI-relevant development.'

def related(x):
    e=[slug for slug,(_,_,terms,_) in ENTITY_DEFS.items() if any(t in corpus_text(x) for t in terms)]
    c=[slug for slug,(_,terms,_) in CONCEPTS.items() if any(t in corpus_text(x) for t in terms)]
    return e,c

def story_link(x,base='..'): return f'[{md_label(x["title"])}]({base}/summaries/{x["id"]}.md)'
def entity_link(slug,base='..'): return f'[{ENTITY_DEFS[slug][0]}]({base}/entities/{slug}.md)'
def concept_link(slug,base='..'): return f'[{CONCEPTS[slug][0]}]({base}/concepts/{slug}.md)'

def event_line(x,base='..'):
    ents,concepts=related(x); links=[story_link(x,base)]+[entity_link(s,base) for s in ents]+[concept_link(s,base) for s in concepts]
    summary=story_summary(x)
    if len(summary)>260: summary=summary[:257].rsplit(' ',1)[0]+'…'
    lock=' 🔒' if x.get('id') in PAYWALLED else ''
    return f'- **{fmt_date(x.get("first_seen"))}** - {summary} ('+' · '.join(links)+')'+lock

PAYWALLED=set()

def build_summaries(xs,stamp):
    PAYWALLED.clear()
    out=WIKI/'summaries'; out.mkdir(exist_ok=True)
    valid=set()
    for x in xs:
        valid.add(f'{x["id"]}.md'); ents,concepts=related(x); tags=[x.get('source','source').lower().replace(' ','-')]+ents+concepts
        related_links=[entity_link(s) for s in ents]+[concept_link(s) for s in concepts]
        meta=metadata('news-summary',fmt_date(x.get('first_seen')),fmt_date(stamp),'high',tags)
        src_url=SOURCES.get(x['id'],{}).get('url') or x['url']
        source=f'[Read the original story]({src_url})'
        if x.get('newsletter_url'): source+=f' · [TLDR AI issue]({x["newsletter_url"]})'
        r=None; llm=False; lf=ROOT/'raw'/'llm'/f"{x['id']}.json"
        if lf.exists():
            try:
                d=json.loads(lf.read_text())
                if d.get('prose'): r={'prose':d['prose'],'highlights':d.get('highlights',[])}; llm=True
            except Exception: r=None
        if r is None: r=rich_summary(x)
        RICH[x['id']]=r
        if r:
            prose='\n\n'.join(r['prose'])
            hl='\n\n## Highlights\n\n'+'\n'.join(f'- {h}' for h in r['highlights']) if r['highlights'] else ''
            summary_sec=prose+hl
        else: summary_sec=story_summary(x)
        st=SOURCES.get(x['id'],{})
        if not llm and st.get('status') in ('thin','error'):
            dom=re.sub(r'^www\.','',urlsplit(st.get('url') or x.get('url') or '').netloc)
            if st.get('block')=='paywall' or dom in PAYWALL_DOMAINS:
                summary_sec+='\n\n_The original source is behind a paywall._'
                PAYWALLED.add(x['id'])
            else:
                summary_sec+='\n\n_The full source text could not be retrieved (blocked or unreadable page); this summary is based on the feed excerpt._'
        text=f'# {x["title"]}\n\n{meta}\n\n## Summary\n\n{summary_sec}\n\n## Source\n\n{source}\n\n## Related pages\n\n'+((' · '.join(related_links)) if related_links else '_No related entity or concept page yet._')+'\n'
        (out/f'{x["id"]}.md').write_text(text)
    for p in out.glob('*.md'):
        if p.name not in valid: p.unlink()

def build_entities(xs,stamp):
    out=WIKI/'entities'; out.mkdir(exist_ok=True)
    for slug,(name,kind,terms,overview) in ENTITY_DEFS.items():
        hits=sorted(match(xs,terms),key=lambda x:(x.get('first_seen',''),x.get('score',0)),reverse=True)
        tags=['entity',slug]+sorted({c for x in hits for c in related(x)[1]})[:4]
        created=min((fmt_date(x.get('first_seen')) for x in hits),default=fmt_date(stamp))
        lines='\n'.join(event_line(x) for x in hits) or '_No matching events in the current corpus._'
        (out/f'{slug}.md').write_text(f'# {name}\n\n{metadata(kind,created,fmt_date(stamp),"medium",tags)}\n\n## Overview\n\n{overview}\n\n## Timeline\n\n{lines}\n')

def build_concepts(xs,stamp):
    out=WIKI/'concepts'; out.mkdir(exist_ok=True)
    for slug,(title,terms,overview) in CONCEPTS.items():
        hits=sorted(match(xs,terms),key=lambda x:(x.get('first_seen',''),x.get('score',0)),reverse=True)
        entities=Counter(e for x in hits for e in related(x)[0])
        links=' · '.join(entity_link(e) for e,_ in entities.most_common(8)) or '_No linked entities yet._'
        timeline='\n'.join(event_line(x) for x in hits[:30]) or '_No matching events in the current corpus._'
        created=min((fmt_date(x.get('first_seen')) for x in hits),default=fmt_date(stamp))
        (out/f'{slug}.md').write_text(f'# Concept: {title}\n\n{metadata("concept",created,fmt_date(stamp),"medium",["concept",slug])}\n\n## Overview\n\n{overview}\n\n## Related entities\n\n{links}\n\n## Timeline\n\n{timeline}\n')

def build_comparisons(xs,stamp):
    out=WIKI/'comparisons'; out.mkdir(exist_ok=True)
    for slug,(title,a,b,overview) in COMPARISONS.items():
        left=sorted(match(xs,a),key=lambda x:(x.get('first_seen',''),x.get('score',0)),reverse=True)[:20]
        right=sorted(match(xs,b),key=lambda x:(x.get('first_seen',''),x.get('score',0)),reverse=True)[:20]
        all_hits={x['id']:x for x in left+right}.values(); created=min((fmt_date(x.get('first_seen')) for x in all_hits),default=fmt_date(stamp))
        l='\n'.join(event_line(x) for x in left) or '_No current signals._'; r='\n'.join(event_line(x) for x in right) or '_No current signals._'
        ltitle,rtitle=(title.split(' vs ',1)+['Evidence B'])[:2]
        (out/f'{slug}.md').write_text(f'# Comparison: {title}\n\n{metadata("comparison",created,fmt_date(stamp),"medium",["comparison",slug])}\n\n## Overview\n\n{overview}\n\n## {ltitle}\n\n{l}\n\n## {rtitle}\n\n{r}\n')

def prose_links(items,limit=4):
    chosen=sorted(items,key=lambda x:(x.get('source')!='Hacker News', x.get('score',0)),reverse=True)[:limit]
    if not chosen: return 'The current corpus has no matching story for this theme.'
    parts=[]
    for x in chosen:
        t=story_summary(x)
        if len(t)>280: t=t[:280].rsplit(' ',1)[0].rstrip(' ,;:')+'\u2026'
        lock=' 🔒' if x.get('id') in PAYWALLED else ''
        parts.append(f"{t} ([read more](../summaries/{x['id']}.md){lock}).")
    midpoint=max(1,(len(parts)+1)//2)
    return ' '.join(parts[:midpoint])+'\n\n'+' '.join(parts[midpoint:]) if len(parts)>1 else parts[0]

def build_weekly(xs,stamp):
    # Regenerate every week present in the corpus, so style fixes apply retroactively.
    # Weeks follow the same first-observed Europe/Madrid days as the dailies.
    first=first_observed_days()
    groups={}
    for x in xs:
        try: iso=dt.date.fromisoformat(first.get(x.get('id'),fmt_date(x.get('first_seen')))).isocalendar()
        except Exception: continue
        groups.setdefault((iso[0],iso[1]),[]).append(x)
    (WIKI/'weekly').mkdir(exist_ok=True)
    for (yr,wk),week in sorted(groups.items()):
        slug=f'{yr}-W{wk:02d}'
        _write_weekly(slug,week,stamp)

def _write_weekly(slug,week,stamp):
    themes=[]
    for concept_slug,(label,terms,_) in CONCEPTS.items():
        hits=sorted(match(week,terms),key=lambda x:x.get('score',0),reverse=True)
        if hits: themes.append((len(hits),concept_slug,label,hits))
    themes.sort(reverse=True)
    title=f'Week {slug}'
    sections=[]; used=set()
    for _,concept_slug,label,hits in themes[:3]:
        fresh=[x for x in hits if x.get('id') not in used]
        if not fresh: continue
        for x in fresh: used.add(x.get('id'))
        entity_counts=Counter(e for x in fresh for e in related(x)[0])
        entity_refs=' · '.join(entity_link(e) for e,_ in entity_counts.most_common(4))
        opening=f'The most visible related entities are {entity_refs}. ' if entity_refs else ''
        sections += [f'## {label}','',opening+prose_links(fresh),'']
    safety=next((hits for _,slug_name,_,hits in themes if slug_name=='ai-safety-incidents'),[])
    agents=next((hits for _,slug_name,_,hits in themes if slug_name=='agentic-systems'),[])
    specialist=next((hits for _,slug_name,_,hits in themes if slug_name=='small-specialist-models'),[])
    tensions=[]
    if agents and safety: tensions.append('Faster agent deployment raises a control question: how much autonomy should systems receive before evaluation and observability catch up? ([Agentic systems](../concepts/agentic-systems.md) · [AI safety incidents and controls](../concepts/ai-safety-incidents.md))')
    if specialist and agents: tensions.append('General-purpose capability competes with smaller specialist systems on cost, latency and auditability. ([Small and specialist models](../concepts/small-specialist-models.md))')
    if match(week,['openai']) and match(week,['anthropic']): tensions.append('OpenAI and Anthropic continue to diverge and converge across products, enterprise positioning, evaluation and safety claims. ([OpenAI](../entities/openai.md) · [Anthropic](../entities/anthropic.md))')
    counts=Counter(x.get('source','?') for x in week)
    body=[f'# {title}','',metadata('synthesis',fmt_date(stamp),fmt_date(stamp),'medium',['synthesis',slug.lower()]),'',f'Synthesis of {len(week)} unique stories first observed in {slug}. Each inline story link opens a generated summary with its original source.','']+sections+['## Tensions and open debates','']+([f'- {x}' for x in tensions] or ['- The corpus is still too small to identify a grounded tension this week.'])+['','## Coverage appendix','']+[f'- {k}: {v}' for k,v in counts.most_common()]
    (WIKI/'weekly').mkdir(exist_ok=True); (WIKI/'weekly'/f'{slug}.md').write_text('\n'.join(body)+'\n')

def build_hubs():
    hubs={'agentic-ai':('Agentic AI','Entry point to systems that act, specialist models and observability.',['../concepts/agentic-systems.md','../concepts/small-specialist-models.md','../concepts/ai-coding-agents.md']), 'safety-governance':('Safety and governance','Evaluation, incidents and controls in one route.',['../concepts/external-evaluation.md','../concepts/ai-safety-incidents.md']), 'frontier-models':('Frontier models','Launches and the labs behind them.',['../entities/openai.md','../entities/anthropic.md','../entities/google.md'])}
    for _slug,_d in _load_overlay('hubs.json').items():
        if _slug not in hubs: hubs[_slug]=(_d['title'],_d['desc'],_d['links'])
    out=WIKI/'hubs'; out.mkdir(exist_ok=True)
    for slug,(title,desc,links) in hubs.items():
        labels=[Path(u).stem.replace('-',' ').title() for u in links]
        (out/f'{slug}.md').write_text(f'# Hub: {title}\n\n{desc}\n\n## Explore\n\n'+'\n'.join(f'- [{n}]({u})' for n,u in zip(labels,links))+'\n')

def update_index(stamp,xs):
    days=sorted((WIKI/'daily').glob('*.md'),reverse=True)
    summaries=sorted((WIKI/'summaries').glob('*.md'))
    date=dt.date.fromisoformat(fmt_date(stamp)); iso=date.isocalendar(); week=f'{iso.year}-W{iso.week:02d}'
    summary_target=summaries[0].name if summaries else ''
    lines=['# AI News Wiki','','A cumulative, cross-linked map of AI news. Every story has its own summary and original source.','',f'_Updated: `{stamp}` · {len(xs)} unique stories._','','## Explore','',f'- [Daily](daily/{days[0].name if days else "index.md"})',f'- [Weekly](weekly/{week}.md)',f'- [Stories](summaries/{summary_target})','- [Entities](entities/openai.md)','- [Hubs](hubs/agentic-ai.md)','- [Concepts](concepts/agentic-systems.md)','','## Daily briefings','']+[f'- [{p.stem}](daily/{p.name})' for p in days]
    (WIKI/'index.md').write_text('\n'.join(lines)+'\n')

def strip_headline_repeat(desc,title):
    def norm(t): return re.sub(r'[^a-z0-9 ]',' ',(t or '').lower())
    parts=re.split(r'\s+\u2014\s+',desc,maxsplit=1)
    if len(parts)==2:
        a=set(norm(parts[0]).split()); b=set(norm(title).split())
        if len(a)>=4 and b and len(a&b)/len(a)>=0.6: return parts[1]
    return desc

def trim_blurb(text,cap=300):
    text=re.sub(r'\s+',' ',text or '').strip()
    sentences=re.split(r'(?<=[.!?])\s+',text)
    picked=' '.join(sentences[:2]).strip()
    if len(picked)>cap: picked=picked[:cap-1].rsplit(' ',1)[0]+'\u2026'
    return picked

def render_daily(day,items,generated):
    try:
        import datetime
        from zoneinfo import ZoneInfo
        generated=datetime.datetime.fromisoformat(generated).astimezone(ZoneInfo('Europe/Madrid')).strftime('%d %b %Y, %H:%M %Z')
    except Exception: pass
    lines=[f"# AI in the news - {day}","",f"Updated: `{generated}`","",
           "Sources: Techmeme, Hacker News, Lobsters, Latent.Space, Stratechery and TLDR AI.",""]
    lines.append(f'Digest of {len(items)} unique stories first observed on {day}. Each inline story link opens a generated summary with its original source.')
    lines.append('')
    bf=ROOT/'raw'/'llm'/f"digest-{day}.json"
    digest=None
    if bf.exists():
        try:
            digest=json.loads(bf.read_text())
            lead=digest.get('lead') or digest.get('prose',[])[:1]
            for para in lead[:1]:
                lines.extend([para,""])
        except Exception: digest=None
    # Authored, day-specific sections (digest schema 3) win when present: the
    # pass writes what genuinely mattered THAT day instead of fixed taxonomy.
    authored=False
    if digest:
        secs=digest.get('sections') or []
        by_id={x.get('id'):x for x in items}
        used=set()
        for sec in secs[:6]:
            fresh=[by_id[i] for i in sec.get('stories',[]) if i in by_id and i not in used]
            if not fresh: continue
            for x in fresh: used.add(x.get('id'))
            blurb=(sec.get('intro') or '').strip()
            lines.extend([f"## {sec.get('title','Section')}",""] + ([blurb,""] if blurb else []) + [prose_links(fresh,limit=6),''])
            authored=True
    if not authored:
        themes=[]
        for concept_slug,(label,terms,_) in CONCEPTS.items():
            hits=sorted(match(items,terms),key=lambda x:x.get('score',0),reverse=True)
            if hits: themes.append((len(hits),concept_slug,label,hits))
        themes.sort(reverse=True)
        used=set()
        for _,concept_slug,label,hits in themes[:4]:
            fresh=[x for x in hits if x.get('id') not in used]
            if not fresh: continue
            for x in fresh: used.add(x.get('id'))
            entity_counts=Counter(e for x in fresh for e in related(x)[0])
            entity_refs=' · '.join(entity_link(e) for e,_ in entity_counts.most_common(4))
            opening=f'The most visible related entities are {entity_refs}. ' if entity_refs else ''
            lines.extend([f'## {label}','',opening+prose_links(fresh),''])
    counts=Counter(i.get('source','?') for i in items)
    lines.extend(["## Sources",""])
    lines.extend([f"- {k}: {v} stories" for k,v in counts.most_common()])
    lines.extend(["",f"_{sum(counts.values())} stories processed this day. Each briefing link opens the full story page; the complete list lives under Stories._",""])
    return "\n".join(lines).rstrip()+"\n"

def first_observed_days():
    # The Europe/Madrid day each story was FIRST observed. Stories lingering in a
    # feed for several days do not reappear in later digests.
    from zoneinfo import ZoneInfo
    madrid=ZoneInfo('Europe/Madrid')
    first={}
    for p in sorted(RAW.glob('*.json')):
        data=json.loads(p.read_text()); gen=data.get('generated_at','')
        try:
            day=dt.datetime.fromisoformat(gen.replace('Z','+00:00')).astimezone(madrid).date().isoformat()
        except Exception:
            day=gen[:10]
        for raw in data.get('items',[]):
            key=raw.get('id')
            if key and key not in first: first[key]=day
    return first

def build_daily():
    # A story belongs to exactly one daily: the Europe/Madrid day it was FIRST observed.
    from zoneinfo import ZoneInfo
    madrid=ZoneInfo('Europe/Madrid')
    days={}; stamps={}; first=first_observed_days()
    for p in sorted(RAW.glob('*.json')):
        data=json.loads(p.read_text()); gen=data.get('generated_at','')
        try:
            day=dt.datetime.fromisoformat(gen.replace('Z','+00:00')).astimezone(madrid).date().isoformat()
        except Exception:
            day=gen[:10]
        if not re.match(r'\d{4}-\d{2}-\d{2}',day): continue
        stamps[day]=max(stamps.get(day,''),gen)
        for raw in data.get('items',[]):
            x=dict(raw); key=x.get('id')
            if not key: continue
            if first.get(key)!=day: continue
            rows=days.setdefault(day,{})
            if key not in rows: rows[key]=x
            else:
                old=rows[key]
                if x.get('score',0)>old.get('score',0): old['score']=x['score']; old['comments']=x.get('comments',0)
                if len(esc(x.get('summary'))) > len(esc(old.get('summary'))): old['summary']=x['summary']
    (WIKI/'daily').mkdir(exist_ok=True)
    for stale in (WIKI/'daily').glob('*.md'):
        if stale.stem not in days: stale.unlink()
    for day,rows in sorted(days.items()):
        (WIKI/'daily'/f"{day}.md").write_text(render_daily(day,list(rows.values()),stamps[day]))

TITLE_OVERRIDES={}
_to=ROOT/'raw'/'llm'/'titles.json'
if _to.exists():
    try: TITLE_OVERRIDES=json.loads(_to.read_text())
    except Exception: TITLE_OVERRIDES={}

def short_title(x):
    """Succinct display title: editorial override, else original-style trim of the feed title. Never touches ids."""
    t=TITLE_OVERRIDES.get(x.get('id',''))
    if t: return t
    t=(x.get('title') or '').strip()
    t=re.sub(r'^(Sources?|Report|Exclusive|Rumou?r):\s+','',t)
    m=re.search(r'\s*\(([A-Za-z][^()]{0,58})\)\s*$',t)
    if m:
        inner=m.group(1)
        if '/' in inner or re.match(r'^[A-Z][A-Za-z0-9.&+]*(?: [A-Za-z0-9.&+]+){0,3}$',inner):
            t=t[:m.start()].rstrip()
    return t or (x.get('title') or '').strip()

def main():
    xs,stamp=load_stories(); compute_new()
    for x in xs:
        t=short_title(x); x['feed_title']=x.get('title',''); x['title']=t
    enrich_sources(xs); build_summaries(xs,stamp); build_daily(); build_entities(xs,stamp); build_concepts(xs,stamp); build_weekly(xs,stamp); build_hubs(); update_index(stamp,xs)
    print(f'Regenerated summaries and contextual pages from {len(xs)} unique stories')
if __name__=='__main__': main()
