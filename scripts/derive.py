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


import html as _html, time, urllib.request

CACHE=ROOT/'raw'/'cache'/'sources'
FETCH_BUDGET_S=420; FETCH_DELAY_S=0.8; MAX_FETCHES=150; MAX_TEXT=60000
UA={'User-Agent':'ai-news-wiki/1.0 (+https://instinct-q0jwr3.github.io/ai-news-wiki/)','Accept':'text/html,application/xhtml+xml'}
SOURCES={}; RICH={}

STOPWORDS=set('a an the and or but if then else when at by for with about into through during before after above below to from up down in out on off over under again further once here there all any both each few more most other some such no nor not only own same so than too very can will just should now is are was were be been being have has had having do does did doing would could ought i you he she it we they them his her its our their this that these those am of as'.split())
JUNK=re.compile(r'cookie|subscribe|sign[ -]?up|newsletter|all rights reserved|advertisement|terms of service|privacy policy|follow us|share this|enable javascript|verify you are|listen to this post|watch on youtube|listen to podcast|views\s+\d+\s+replies|\d+\s+reposts?\b.{0,12}\blikes\b',re.I)

def fetch_url(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=10) as r:
        ct=r.headers.get('content-type','')
        if 'html' not in ct: return None,f'unsupported content-type: {ct}'
        raw=r.read(1500000)
    return raw.decode('utf-8','replace'),None

def html_to_text(h):
    h=re.sub(r'(?is)<(script|style|noscript|svg|form|nav|footer|header|aside|iframe)[^>]*>.*?</\1>',' ',h)
    m=re.search(r'(?is)<article[^>]*>(.*?)</article>',h)
    seg=m.group(1) if m else h
    ps=re.findall(r'(?is)<p[^>]*>(.*?)</p>',seg)
    txt='\n\n'.join(ps) if len(ps)>=3 else seg
    txt=_html.unescape(re.sub(r'(?s)<[^>]+>',' ',txt))
    return re.sub(r'\s+',' ',txt).strip()

def cache_entry(x):
    CACHE.mkdir(parents=True,exist_ok=True)
    f=CACHE/f"{x['id']}.json"
    if f.exists():
        try: c=json.loads(f.read_text())
        except Exception: c=None
        if c and c.get('url')==x.get('url'):
            if c.get('status') in ('ok','thin'): return c,True
            try: age=(dt.datetime.now(dt.timezone.utc)-dt.datetime.fromisoformat(c.get('fetched_at',''))).total_seconds()
            except Exception: age=1e9
            if c.get('status')=='error' and age<86400: return c,True
    return None,False

def save_entry(x,status,text,note=''):
    (CACHE/f"{x['id']}.json").write_text(json.dumps({'url':x.get('url'),'fetched_at':dt.datetime.now(dt.timezone.utc).isoformat(),'status':status,'note':note,'text':text[:MAX_TEXT]},ensure_ascii=False))

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
        body,err=None,None
        for attempt in (1,2):
            try: body,err=fetch_url(url)
            except Exception as e: body,err=None,str(e)[:160]
            if body: break
            time.sleep(FETCH_DELAY_S)
        if not body:
            save_entry(x,'error','',err or 'fetch failed'); SOURCES[x['id']]={'status':'error'}; stats['fetch_error']+=1; continue
        text=html_to_text(body)
        if len(text)<400:
            save_entry(x,'thin',text,'extracted text under 400 chars'); SOURCES[x['id']]={'status':'thin','text':text}; stats['fetched_thin']+=1
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
    return summarize_article(text[:MAX_TEXT],x.get('title',''))

def esc(text): return re.sub(r'\s+',' ',str(text or '')).strip()

def md_label(text):
    return esc(text).replace('[','').replace(']','')
def corpus_text(x): return (x.get('title','')+' '+x.get('summary','')).lower()
def match(xs,terms): return [x for x in xs if any(t in corpus_text(x) for t in terms)]
def fmt_date(value): return (value or '')[:10] or dt.date.today().isoformat()
def metadata(kind,created,updated,confidence='medium',tags=()):
    tag_line=' '.join(f'`{t}`' for t in tags)
    return f'_type: {kind} · created: {created} · updated: {updated} · confidence: {confidence}_\n\n{tag_line}'.rstrip()

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
    xs=list(rows.values()); stamp=max((x.get('last_seen','') for x in xs),default='')
    return xs,stamp

def story_summary(x):
    r=RICH.get(x.get('id'))
    if r and r['prose']: return r['prose'][0]
    desc=esc(x.get('summary')); title=esc(x.get('title'))
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
    return f'{title}. {x.get("source","The source feed")} selected it as an AI-relevant development.'

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
    return f'- **{fmt_date(x.get("first_seen"))}** - {summary} ('+' · '.join(links)+')'

def build_summaries(xs,stamp):
    out=WIKI/'summaries'; out.mkdir(exist_ok=True)
    valid=set()
    for x in xs:
        valid.add(f'{x["id"]}.md'); ents,concepts=related(x); tags=[x.get('source','source').lower().replace(' ','-')]+ents+concepts
        related_links=[entity_link(s) for s in ents]+[concept_link(s) for s in concepts]
        meta=metadata('news-summary',fmt_date(x.get('first_seen')),fmt_date(stamp),'high',tags)
        source=f'[Read the original story]({x["url"]})'
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
        if not llm and SOURCES.get(x['id'],{}).get('status') in ('thin','error'):
            summary_sec+='\n\n_Extractive summary: the original source could not be fully accessed._'
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
        ents,concepts=related(x)
        refs=[story_link(x)]+[entity_link(e) for e in ents[:2]]+[concept_link(c) for c in concepts[:1]]
        parts.append(story_summary(x)[:280].rstrip(' .')+' ('+' · '.join(refs)+').')
    midpoint=max(1,(len(parts)+1)//2)
    return ' '.join(parts[:midpoint])+'\n\n'+' '.join(parts[midpoint:]) if len(parts)>1 else parts[0]

def build_weekly(xs,stamp):
    date=dt.date.fromisoformat(fmt_date(stamp)); iso=date.isocalendar(); slug=f'{iso.year}-W{iso.week:02d}'
    week=[x for x in xs if dt.date.fromisoformat(fmt_date(x.get('first_seen'))).isocalendar()[:2]==iso[:2]]
    themes=[]
    for concept_slug,(label,terms,_) in CONCEPTS.items():
        hits=sorted(match(week,terms),key=lambda x:x.get('score',0),reverse=True)
        if hits: themes.append((len(hits),concept_slug,label,hits))
    themes.sort(reverse=True)
    headline_labels=[label.replace('AI ','').replace(' and controls','').replace('External ','').replace('Small and specialist models','Small Models').replace('Agentic systems','Agentic Systems').replace('safety incidents','Safety Debates') for _,_,label,_ in themes[:3]]
    headline=', '.join(headline_labels[:-1])+(' and '+headline_labels[-1] if len(headline_labels)>1 else (headline_labels[0] if headline_labels else 'AI Developments'))
    title=f'Week {slug}: {headline}'
    sections=[]
    for _,concept_slug,label,hits in themes[:3]:
        entity_counts=Counter(e for x in hits for e in related(x)[0])
        entity_refs=' · '.join(entity_link(e) for e,_ in entity_counts.most_common(4))
        opening=f'This theme connects {len(hits)} developments around [{label}](../concepts/{concept_slug}.md).'
        if entity_refs: opening+=f' The most visible related entities are {entity_refs}.'
        sections += [f'## {label}','',opening+' '+prose_links(hits),'']
    safety=next((hits for _,slug_name,_,hits in themes if slug_name=='ai-safety-incidents'),[])
    agents=next((hits for _,slug_name,_,hits in themes if slug_name=='agentic-systems'),[])
    specialist=next((hits for _,slug_name,_,hits in themes if slug_name=='small-specialist-models'),[])
    tensions=[]
    if agents and safety: tensions.append('Faster agent deployment raises a control question: how much autonomy should systems receive before evaluation and observability catch up? ([Agentic systems](../concepts/agentic-systems.md) · [AI safety incidents and controls](../concepts/ai-safety-incidents.md))')
    if specialist and agents: tensions.append('General-purpose capability competes with smaller specialist systems on cost, latency and auditability. ([Generalist vs specialist models](../comparisons/generalist-vs-specialist-models.md) · [Small and specialist models](../concepts/small-specialist-models.md))')
    if match(week,['openai']) and match(week,['anthropic']): tensions.append('OpenAI and Anthropic continue to diverge and converge across products, enterprise positioning, evaluation and safety claims. ([OpenAI vs Anthropic](../comparisons/openai-vs-anthropic.md) · [OpenAI](../entities/openai.md) · [Anthropic](../entities/anthropic.md))')
    counts=Counter(x.get('source','?') for x in week)
    body=[f'# {title}','',metadata('synthesis',fmt_date(stamp),fmt_date(stamp),'medium',['synthesis',slug.lower()]),'',f'Synthesis of {len(week)} unique stories first observed in {slug}. Each inline story link opens a generated summary with its original source.','']+sections+['## Tensions and open debates','']+([f'- {x}' for x in tensions] or ['- The corpus is still too small to identify a grounded tension this week.'])+['','## Coverage appendix','']+[f'- {k}: {v}' for k,v in counts.most_common()]
    (WIKI/'weekly').mkdir(exist_ok=True); (WIKI/'weekly'/f'{slug}.md').write_text('\n'.join(body)+'\n')

def build_hubs():
    hubs={'agentic-ai':('Agentic AI','Entry point to systems that act, specialist models and observability.',['../concepts/agentic-systems.md','../concepts/small-specialist-models.md','../comparisons/generalist-vs-specialist-models.md']), 'safety-governance':('Safety and governance','Evaluation, incidents and controls in one route.',['../concepts/external-evaluation.md','../concepts/ai-safety-incidents.md']), 'frontier-models':('Frontier models','Launches, entities and lab comparisons.',['../comparisons/openai-vs-anthropic.md','../entities/openai.md','../entities/anthropic.md'])}
    out=WIKI/'hubs'; out.mkdir(exist_ok=True)
    for slug,(title,desc,links) in hubs.items():
        labels=[Path(u).stem.replace('-',' ').title() for u in links]
        (out/f'{slug}.md').write_text(f'# Hub: {title}\n\n{desc}\n\n## Explore\n\n'+'\n'.join(f'- [{n}]({u})' for n,u in zip(labels,links))+'\n')

def update_index(stamp,xs):
    days=sorted((WIKI/'daily').glob('*.md'),reverse=True)
    summaries=sorted((WIKI/'summaries').glob('*.md'))
    date=dt.date.fromisoformat(fmt_date(stamp)); iso=date.isocalendar(); week=f'{iso.year}-W{iso.week:02d}'
    summary_target=summaries[0].name if summaries else ''
    lines=['# AI News Wiki','','A cumulative, cross-linked map of AI news. Every story has its own summary and original source.','',f'_Updated: `{stamp}` · {len(xs)} unique stories._','','## Explore','', '- [Entities](entities/openai.md)','- [Concepts](concepts/agentic-systems.md)','- [Comparisons](comparisons/openai-vs-anthropic.md)',f'- [Story summaries](summaries/{summary_target})',f'- [Weekly synthesis](weekly/{week}.md)','- [Hubs](hubs/agentic-ai.md)','','## Daily digests','']+[f'- [{p.stem}](daily/{p.name})' for p in days]
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
    lines=[f"# AI in the news - {day}","",f"Updated: `{generated}`","",
           "Sources: Techmeme, Hacker News, Lobsters, Latent.Space, Stratechery and TLDR AI.",""]
    for source in ("Techmeme","Hacker News","Lobsters","Latent.Space","Stratechery","TLDR AI"):
        si=[i for i in items if i.get('source')==source]
        lines.extend([f"## {source}",""])
        if not si:
            lines.extend(["_No stories passed the AI filter._",""]); continue
        for item in si:
            lines.extend([f"### [{item['title']}](../summaries/{item['id']}.md)","",
                          trim_blurb(story_summary(item)),""])
            meta=[]
            if source=="Hacker News" and (item.get('score') or item.get('comments')):
                meta.append(f"{item.get('score',0)} points, {item.get('comments',0)} comments")
            meta.append(f"[Original source]({item['url']})")
            lines.extend(["_"+" \u00b7 ".join(meta)+"_",""])
    return "\n".join(lines).rstrip()+"\n"

def build_daily():
    days={}; stamps={}
    for p in sorted(RAW.glob('*.json')):
        data=json.loads(p.read_text()); gen=data.get('generated_at',''); day=gen[:10]
        if not re.match(r'\d{4}-\d{2}-\d{2}',day): continue
        rows=days.setdefault(day,{}); stamps[day]=max(stamps.get(day,''),gen)
        for raw in data.get('items',[]):
            x=dict(raw); key=x.get('id')
            if not key: continue
            if key not in rows: rows[key]=x
            else:
                old=rows[key]
                if x.get('score',0)>old.get('score',0): old['score']=x['score']; old['comments']=x.get('comments',0)
                if len(esc(x.get('summary'))) > len(esc(old.get('summary'))): old['summary']=x['summary']
    for day,rows in sorted(days.items()):
        (WIKI/'daily'/f"{day}.md").write_text(render_daily(day,list(rows.values()),stamps[day]))

def main():
    xs,stamp=load_stories(); enrich_sources(xs); build_summaries(xs,stamp); build_daily(); build_entities(xs,stamp); build_concepts(xs,stamp); build_comparisons(xs,stamp); build_weekly(xs,stamp); build_hubs(); update_index(stamp,xs)
    print(f'Regenerated summaries and contextual pages from {len(xs)} unique stories')
if __name__=='__main__': main()
