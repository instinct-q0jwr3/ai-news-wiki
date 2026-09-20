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
 'agentic-systems': ('Sistemas agénticos', ['agent','agentic','tool call','computer use','claude code','agents.md']),
 'external-evaluation': ('Evaluación externa de IA', ['evaluat','metr','redwood','apollo','aef-1','benchmark']),
 'small-specialist-models': ('Modelos pequeños y especialistas', ['small model','local-llm','local llm','needle','system one','cua-s1','edge','on-device']),
 'ai-safety-incidents': ('Incidentes y controles de seguridad', ['safety','security','hack','misalign','kill-switch','hallucin','collusion','guardrail']),
}
COMPARISONS={
 'openai-vs-anthropic': ('OpenAI vs Anthropic', ['openai','gpt-6','astra'], ['anthropic','claude','fable','mythos']),
 'generalistas-vs-especialistas': ('Modelos generalistas vs especialistas', ['gpt','claude','gemini','foundation model'], ['needle','cua-s1','small model','specialist','local-llm']),
 'agentes-abiertos-vs-cerrados': ('Agentes abiertos vs plataformas cerradas', ['open source','github','local','agents.md'], ['openai','anthropic','salesforce','meta']),
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
    if x.get('score'): meta+=f" · {x['score']} puntos HN"
    return f"- [{x['title']}]({x['url']}){meta}"

def replace_block(path, title, intro, lines):
    path.parent.mkdir(parents=True,exist_ok=True)
    block='\n'.join([BEGIN,'## Evidencia viva','']+lines+['',END])
    if path.exists():
        text=path.read_text()
        if BEGIN in text and END in text:
            text=re.sub(re.escape(BEGIN)+r'.*?'+re.escape(END),block,text,flags=re.S)
        else: text=text.rstrip()+'\n\n'+block+'\n'
    else: text=f"# {title}\n\n{intro}\n\n{block}\n"
    path.write_text(text)

def ensure_curated():
    seeds={
      'agentic-systems': 'Sistemas que planifican o actúan mediante herramientas. Esta página sigue su arquitectura, control, observabilidad y adopción.',
      'external-evaluation': 'Cómo terceros, estándares y evaluaciones embebidas intentan medir capacidades y riesgos de modelos avanzados.',
      'small-specialist-models': 'Modelos estrechos que cambian capacidad general por coste, latencia y control local.',
      'ai-safety-incidents': 'Registro interpretado de fallos, ataques y propuestas de control. Un incidente reportado no equivale por sí solo a un riesgo general demostrado.',
    }
    return seeds

def build_concepts(xs, stamp):
    for slug,(title,terms) in CONCEPTS.items():
        hits=sorted(match(xs,terms),key=lambda x:x.get('score',0),reverse=True)[:14]
        lines=[f"_Actualización automática: `{stamp or 'sin sello'}` · {len(hits)} señales seleccionadas._",'']+[bullet(x) for x in hits]
        replace_block(WIKI/'concepts'/f'{slug}.md',f'Concepto: {title}',ensure_curated()[slug],lines)

def build_comparisons(xs, stamp):
    intros={
      'openai-vs-anthropic': 'Comparación continua de lanzamientos, precio, empresa, evaluación y seguridad. No es una tabla de clasificación: conserva la evidencia y separa anuncios de resultados independientes.',
      'generalistas-vs-especialistas': 'Los generalistas maximizan amplitud y razonamiento; los especialistas buscan menor coste, latencia y una superficie de acción verificable.',
      'agentes-abiertos-vs-cerrados': 'Contrasta control y auditabilidad local con la integración y capacidad de las plataformas alojadas.',
    }
    for slug,(title,a,b) in COMPARISONS.items():
        left=sorted(match(xs,a),key=lambda x:x.get('score',0),reverse=True)[:8]
        right=sorted(match(xs,b),key=lambda x:x.get('score',0),reverse=True)[:8]
        lines=[f"_Actualización automática: `{stamp or 'sin sello'}`._",'',f"### Señales: {title.split(' vs ')[0]}",'']+[bullet(x) for x in left]+['',f"### Señales: {title.split(' vs ')[-1]}",'']+[bullet(x) for x in right]
        replace_block(WIKI/'comparisons'/f'{slug}.md',f'Comparativa: {title}',intros[slug],lines)

def build_weekly(xs, stamp):
    day=(stamp[:10] if stamp else dt.date.today().isoformat()); date=dt.date.fromisoformat(day); iso=date.isocalendar(); slug=f'{iso.year}-W{iso.week:02d}'
    cats={title:match(xs,terms) for title,terms in CONCEPTS.values()}
    source_counts=Counter(x.get('source','?') for x in xs)
    top=sorted(xs,key=lambda x:x.get('score',0),reverse=True)[:8]
    lines=[f'# Síntesis semanal · {slug}','',f'_Corte de datos: `{stamp}` · {len(xs)} historias únicas._','',
      '## Lectura ejecutiva','',
      'La semana está dominada por el paso de chat a sistemas que actúan, mientras evaluación y seguridad se convierten en infraestructura. En paralelo aparecen modelos pequeños y especialistas como alternativa de coste y control a los modelos frontera.','',
      '## Señales por eje','']
    for title,hits in cats.items():
        lines.append(f"- **{title}:** {len(hits)} historias relacionadas.")
    lines += ['', '## Historias con más conversación en Hacker News','']+[bullet(x) for x in top]
    lines += ['', '## Cobertura por fuente','']+[f"- {k}: {v}" for k,v in source_counts.most_common()]
    lines += ['', '## Qué vigilar','',
      '- Si los estándares de evaluación externa pasan de anuncios a resultados publicados y comparables.',
      '- Si los modelos especialistas mantienen su ventaja fuera de tareas estrechas.',
      '- Si la observabilidad de agentes se consolida como categoría propia de infraestructura.','']
    (WIKI/'weekly').mkdir(exist_ok=True); (WIKI/'weekly'/f'{slug}.md').write_text('\n'.join(lines))

def build_hubs():
    hubs={
      'agentic-ai': ('IA agéntica','Punto de entrada a sistemas que actúan, modelos especialistas y observabilidad.',[
        ('Concepto · Sistemas agénticos','../concepts/agentic-systems.md'),('Concepto · Modelos pequeños y especialistas','../concepts/small-specialist-models.md'),('Comparativa · Generalistas vs especialistas','../comparisons/generalistas-vs-especialistas.md'),('Tema · Agentes','../topics/agentes.md')]),
      'safety-governance': ('Seguridad y gobernanza','Evaluación, incidentes, regulación y controles en una sola ruta.',[
        ('Concepto · Evaluación externa','../concepts/external-evaluation.md'),('Concepto · Incidentes y controles','../concepts/ai-safety-incidents.md'),('Tema · Seguridad y alineación','../topics/seguridad-y-alineacion.md'),('Tema · Regulación y política','../topics/regulacion-y-politica.md')]),
      'frontier-models': ('Modelos frontera','Lanzamientos, entidades y comparaciones entre laboratorios.',[
        ('Comparativa · OpenAI vs Anthropic','../comparisons/openai-vs-anthropic.md'),('Tema · Modelos','../topics/modelos.md'),('Entidad · OpenAI','../entities/openai.md'),('Entidad · Anthropic','../entities/anthropic.md')])}
    d=WIKI/'hubs'; d.mkdir(exist_ok=True)
    for slug,(title,desc,links) in hubs.items():
        (d/f'{slug}.md').write_text('\n'.join([f'# Hub: {title}','',desc,'','## Explorar','']+[f'- [{n}]({u})' for n,u in links]+['']))

def update_index(stamp):
    path=WIKI/'index.md'; text=path.read_text() if path.exists() else '# AI News Wiki\n'
    d=dt.date.fromisoformat(stamp[:10]) if stamp else dt.date.today(); iso=d.isocalendar(); week=f'{iso.year}-W{iso.week:02d}'
    auto=f'''<!-- AUTO:NAV -->
## Hubs

- [IA agéntica](hubs/agentic-ai.md)
- [Seguridad y gobernanza](hubs/safety-governance.md)
- [Modelos frontera](hubs/frontier-models.md)

## Conceptos

- [Sistemas agénticos](concepts/agentic-systems.md)
- [Evaluación externa de IA](concepts/external-evaluation.md)
- [Modelos pequeños y especialistas](concepts/small-specialist-models.md)
- [Incidentes y controles de seguridad](concepts/ai-safety-incidents.md)

## Comparativas

- [OpenAI vs Anthropic](comparisons/openai-vs-anthropic.md)
- [Generalistas vs especialistas](comparisons/generalistas-vs-especialistas.md)
- [Agentes abiertos vs plataformas cerradas](comparisons/agentes-abiertos-vs-cerrados.md)

## Síntesis semanal

- [Semana actual](weekly/{week}.md)
<!-- /AUTO:NAV -->'''
    if '<!-- AUTO:NAV -->' in text: text=re.sub(r'<!-- AUTO:NAV -->.*?<!-- /AUTO:NAV -->',auto,text,flags=re.S)
    else: text=text.rstrip()+'\n\n'+auto+'\n'
    path.write_text(text)

def main():
    xs,weekly,stamp=stories(); build_concepts(xs,stamp); build_comparisons(xs,stamp); build_weekly(weekly,stamp); build_hubs(); update_index(stamp)
    print(f'Refreshed derived evidence from {len(xs)} unique stories')
if __name__=='__main__': main()
