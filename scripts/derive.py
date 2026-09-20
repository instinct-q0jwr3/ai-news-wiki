#!/usr/bin/env python3
"""Refresh the machine-maintained evidence layer of the LLM-owned derived wiki."""
from __future__ import annotations
import datetime as dt, json, re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WIKI=ROOT/'wiki'; RAW=ROOT/'raw'/'snapshots'
BEGIN='<!-- AUTO:EVIDENCE -->'; END='<!-- /AUTO:EVIDENCE -->'

CONCEPTS={
 'agentic-systems': ('Agentic systems', ['agent','agentic','tool call','computer use','claude code','agents.md']),
 'external-evaluation': ('External AI evaluation', ['evaluat','metr','redwood','apollo','aef-1','benchmark']),
 'small-specialist-models': ('Small and specialist models', ['small model','local-llm','local llm','needle','system one','cua-s1','edge','on-device']),
 'ai-safety-incidents': ('AI safety incidents and controls', ['safety','security','hack','misalign','kill-switch','hallucin','collusion','guardrail']),
}
COMPARISONS={
 'openai-vs-anthropic': ('OpenAI vs Anthropic', ['openai','gpt-6','astra'], ['anthropic','claude','fable','mythos']),
 'generalistas-vs-especialistas': ('Generalist vs specialist models', ['gpt','claude','gemini','foundation model'], ['needle','cua-s1','small model','specialist','local-llm']),
 'agentes-abiertos-vs-cerrados': ('Open agents vs closed platforms', ['open source','github','local','agents.md'], ['openai','anthropic','salesforce','meta']),
}

def stories():
    snapshots=[]
    for p in sorted(RAW.glob('*.json')):
        data=json.loads(p.read_text()); snapshots.append(data)
    stamp=max((x.get('generated_at','') for x in snapshots), default='')
    latest_date=dt.date.fromisoformat(stamp[:10]) if stamp else dt.date.today()
    latest_week=latest_date.isocalendar()[:2]
    def unique(selected):
        seen={}
        for data in selected:
            for x in data.get('items',[]):
                key=x.get('id') or re.sub(r'\W+',' ',x.get('title','').lower()).strip()
                old=seen.get(key)
                if old is None or x.get('score',0)>old.get('score',0): seen[key]=x
        return list(seen.values())
    weekly=[x for x in snapshots if x.get('generated_at') and dt.date.fromisoformat(x['generated_at'][:10]).isocalendar()[:2]==latest_week]
    return unique(snapshots), unique(weekly), stamp

def match(xs, terms):
    return [x for x in xs if any(t in (x.get('title','')+' '+x.get('summary','')).lower() for t in terms)]

def bullet(x):
    meta=f" · {x.get('source','Fuente')}"
    if x.get('score'): meta+=f" · {x['score']} HN points"
    return f"- [{x['title']}]({x['url']}){meta}"

def replace_block(path, title, intro, lines):
    path.parent.mkdir(parents=True,exist_ok=True)
    block='\n'.join([BEGIN,'## Living evidence','']+lines+['',END])
    if path.exists():
        text=path.read_text()
        if BEGIN in text and END in text:
            text=re.sub(re.escape(BEGIN)+r'.*?'+re.escape(END),block,text,flags=re.S)
        else: text=text.rstrip()+'\n\n'+block+'\n'
    else: text=f"# {title}\n\n{intro}\n\n{block}\n"
    path.write_text(text)

def ensure_curated():
    seeds={
      'agentic-systems': 'Systems that plan or act through tools. This page tracks their architecture, control, observability and adoption.',
      'external-evaluation': 'How third parties, standards and embedded evaluations try to measure capabilities and risks of advanced models.',
      'small-specialist-models': 'Narrow models that trade general capability for cost, latency and local control.',
      'ai-safety-incidents': 'An interpreted record of failures, attacks and control proposals. A reported incident does not by itself prove a general risk.',
    }
    return seeds

def build_concepts(xs, stamp):
    for slug,(title,terms) in CONCEPTS.items():
        hits=sorted(match(xs,terms),key=lambda x:x.get('score',0),reverse=True)[:14]
        lines=[f"_Automatic update: `{stamp or 'no stamp'}` · {len(hits)} selected signals._",'']+[bullet(x) for x in hits]
        replace_block(WIKI/'concepts'/f'{slug}.md',f'Concept: {title}',ensure_curated()[slug],lines)

def build_comparisons(xs, stamp):
    intros={
      'openai-vs-anthropic': 'Running comparison of launches, pricing, business, evaluation and safety. Not a leaderboard: it keeps the evidence and separates announcements from independent results.',
      'generalistas-vs-especialistas': 'Generalists maximize breadth and reasoning; specialists aim for lower cost, latency and a verifiable action surface.',
      'agentes-abiertos-vs-cerrados': 'Contrasts local control and auditability with the integration and capability of hosted platforms.',
    }
    for slug,(title,a,b) in COMPARISONS.items():
        left=sorted(match(xs,a),key=lambda x:x.get('score',0),reverse=True)[:8]
        right=sorted(match(xs,b),key=lambda x:x.get('score',0),reverse=True)[:8]
        lines=[f"_Automatic update: `{stamp or 'no stamp'}`._",'',f"### Signals: {title.split(' vs ')[0]}",'']+[bullet(x) for x in left]+['',f"### Signals: {title.split(' vs ')[-1]}",'']+[bullet(x) for x in right]
        replace_block(WIKI/'comparisons'/f'{slug}.md',f'Comparison: {title}',intros[slug],lines)

def build_weekly(xs, stamp):
    day=(stamp[:10] if stamp else dt.date.today().isoformat()); date=dt.date.fromisoformat(day); iso=date.isocalendar(); slug=f'{iso.year}-W{iso.week:02d}'
    cats={title:match(xs,terms) for title,terms in CONCEPTS.values()}
    source_counts=Counter(x.get('source','?') for x in xs)
    top=sorted(xs,key=lambda x:x.get('score',0),reverse=True)[:8]
    lines=[f'# Weekly synthesis · {slug}','',f'_Data cut: `{stamp}` · {len(xs)} unique stories._','',
      '## Executive read','',
      'The week is dominated by the shift from chat to systems that act, while evaluation and safety turn into infrastructure. In parallel, small specialist models emerge as a cost-and-control alternative to frontier models.','',
      '## Signals by axis','']
    for title,hits in cats.items():
        lines.append(f"- **{title}:** {len(hits)} related stories.")
    lines += ['', '## Most discussed on Hacker News','']+[bullet(x) for x in top]
    lines += ['', '## Coverage by source','']+[f"- {k}: {v}" for k,v in source_counts.most_common()]
    lines += ['', '## What to watch','',
      '- Whether external-evaluation standards move from announcements to published, comparable results.',
      '- Whether specialist models keep their edge outside narrow tasks.',
      '- Whether agent observability consolidates as its own infrastructure category.','']
    (WIKI/'weekly').mkdir(exist_ok=True); (WIKI/'weekly'/f'{slug}.md').write_text('\n'.join(lines))

def build_hubs():
    hubs={
      'agentic-ai': ('Agentic AI','Entry point to systems that act, specialist models and observability.',[
        ('Concept · Agentic systems','../concepts/agentic-systems.md'),('Concept · Small and specialist models','../concepts/small-specialist-models.md'),('Comparison · Generalists vs specialists','../comparisons/generalistas-vs-especialistas.md'),('Topic · Agents','../topics/agentes.md')]),
      'safety-governance': ('Safety and governance','Evaluation, incidents, regulation and controls in one route.',[
        ('Concept · External evaluation','../concepts/external-evaluation.md'),('Concept · Incidents and controls','../concepts/ai-safety-incidents.md'),('Topic · Safety and alignment','../topics/seguridad-y-alineacion.md'),('Topic · Regulation and policy','../topics/regulacion-y-politica.md')]),
      'frontier-models': ('Frontier models','Launches, entities and lab comparisons.',[
        ('Comparison · OpenAI vs Anthropic','../comparisons/openai-vs-anthropic.md'),('Topic · Models','../topics/modelos.md'),('Entity · OpenAI','../entities/openai.md'),('Entity · Anthropic','../entities/anthropic.md')])}
    d=WIKI/'hubs'; d.mkdir(exist_ok=True)
    for slug,(title,desc,links) in hubs.items():
        (d/f'{slug}.md').write_text('\n'.join([f'# Hub: {title}','',desc,'','## Explorar','']+[f'- [{n}]({u})' for n,u in links]+['']))

def update_index(stamp):
    path=WIKI/'index.md'; text=path.read_text() if path.exists() else '# AI News Wiki\n'
    d=dt.date.fromisoformat(stamp[:10]) if stamp else dt.date.today(); iso=d.isocalendar(); week=f'{iso.year}-W{iso.week:02d}'
    auto=f'''<!-- AUTO:NAV -->
## Hubs

- [Agentic AI](hubs/agentic-ai.md)
- [Safety and governance](hubs/safety-governance.md)
- [Frontier models](hubs/frontier-models.md)

## Concepts

- [Agentic systems](concepts/agentic-systems.md)
- [External AI evaluation](concepts/external-evaluation.md)
- [Small and specialist models](concepts/small-specialist-models.md)
- [AI safety incidents and controls](concepts/ai-safety-incidents.md)

## Comparisons

- [OpenAI vs Anthropic](comparisons/openai-vs-anthropic.md)
- [Generalist vs specialist models](comparisons/generalistas-vs-especialistas.md)
- [Open agents vs closed platforms](comparisons/agentes-abiertos-vs-cerrados.md)

## Weekly synthesis

- [Current week](weekly/{week}.md)
<!-- /AUTO:NAV -->'''
    if '<!-- AUTO:NAV -->' in text: text=re.sub(r'<!-- AUTO:NAV -->.*?<!-- /AUTO:NAV -->',auto,text,flags=re.S)
    else: text=text.rstrip()+'\n\n'+auto+'\n'
    path.write_text(text)

def main():
    xs,weekly,stamp=stories(); build_concepts(xs,stamp); build_comparisons(xs,stamp); build_weekly(weekly,stamp); build_hubs(); update_index(stamp)
    print(f'Refreshed derived evidence from {len(xs)} unique stories')
if __name__=='__main__': main()
