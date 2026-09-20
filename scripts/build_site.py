#!/usr/bin/env python3
"""Build a dependency-free GitHub Pages site from wiki Markdown."""
from __future__ import annotations
import html,json,re,shutil
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; WIKI=ROOT/'wiki'; OUT=ROOT/'docs'
LABELS={'hubs':'Hubs','weekly':'Weekly','entities':'Entities','daily':'Digests','concepts':'Concepts','comparisons':'Compare','topics':'Topics','trends':'Trends'}

def inline(s):
    s=html.escape(s,quote=False)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'\[([^]]+)\]\(([^)]+)\)',lambda m:f'<a href="{href(m.group(2))}">{m.group(1)}</a>',s)
    return s

def href(u):
    if re.match(r'https?://',u): return html.escape(u,quote=True)
    u=u.replace('.md','.html'); return html.escape(u,quote=True)

def render_md(text):
    out=[]; in_list=False
    for raw in text.splitlines():
        line=raw.strip()
        if line.startswith('<!--'): continue
        if line.startswith('#'):
            if in_list: out.append('</ul>'); in_list=False
            level=len(line)-len(line.lstrip('#')); out.append(f'<h{level}>{inline(line[level:].strip())}</h{level}>')
        elif line.startswith('- '):
            if not in_list: out.append('<ul>'); in_list=True
            out.append(f'<li>{inline(line[2:])}</li>')
        elif not line:
            if in_list: out.append('</ul>'); in_list=False
        elif line.startswith('_') and line.endswith('_'): out.append(f'<p class="meta">{inline(line[1:-1])}</p>')
        else: out.append(f'<p>{inline(line)}</p>')
    if in_list: out.append('</ul>')
    return '\n'.join(out)

def title_of(p):
    for line in p.read_text().splitlines():
        if line.startswith('# '): return line[2:].strip()
    return p.stem.replace('-',' ').title()

def shell(title,content,rel='',search=False):
    nav=''.join(f'<a href="{rel}{k}/index.html">{v}</a>' for k,v in [('hubs','Hubs'),('weekly','Weekly'),('entities','Entities'),('daily','Digests'),('concepts','Concepts'),('comparisons','Compare')])
    box='<div class="search-wrap"><input id="search" type="search" placeholder="Buscar en la wiki…" autocomplete="off"><div id="results"></div></div>' if search else '<a class="search-link" href="'+rel+'index.html#search">Buscar</a>'
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · AI Wiki</title><link rel="stylesheet" href="{rel}assets/style.css"></head><body><header><a class="brand" href="{rel}index.html"><span>AI</span> wiki</a><nav>{nav}</nav>{box}</header><main>{content}</main><footer>AI News Wiki · Fuentes enlazadas en cada entrada</footer>{'<script src="assets/search.js"></script>' if search else ''}</body></html>'''

def section_cards(name,files,limit=5):
    cards=[]
    for p in files[:limit]:
        rel=p.relative_to(WIKI).with_suffix('.html').as_posix(); cards.append(f'<li><a href="{rel}">{html.escape(title_of(p))}</a><span>{p.stat().st_mtime_ns}</span></li>')
    return f'<section><div class="section-head"><h2>{name}</h2></div><ul class="link-list">'+''.join(cards)+'</ul></section>'

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT/'assets').mkdir(parents=True)
    files=sorted(WIKI.rglob('*.md'))
    docs=[]
    for p in files:
        relpath=p.relative_to(WIKI).with_suffix('.html'); dest=OUT/relpath; dest.parent.mkdir(parents=True,exist_ok=True)
        rel='../'*len(relpath.parent.parts); text=p.read_text(); title=title_of(p)
        dest.write_text(shell(title,f'<article>{render_md(text)}</article>',rel))
        plain=re.sub(r'[#*_`\[\]()]',' ',text); docs.append({'title':title,'url':relpath.as_posix(),'text':re.sub(r'\s+',' ',plain)[:2400],'type':p.parent.name})
    for folder,label in LABELS.items():
        d=WIKI/folder
        if not d.exists(): continue
        arr=sorted(d.glob('*.md'),reverse=True)
        cards=[]
        for p in arr:
            desc=next((x for x in p.read_text().splitlines()[1:] if x.strip() and not x.startswith(("#","<!--","_"))), "Abrir página")
            cards.append(f'<a class="card" href="{p.stem}.html"><span class="eyebrow">{html.escape(label)}</span><h2>{html.escape(title_of(p))}</h2><p>{html.escape(desc)}</p></a>')
        cards=''.join(cards)
        (OUT/folder/'index.html').write_text(shell(label,f'<div class="page-title"><span class="eyebrow">Biblioteca</span><h1>{label}</h1><p>{len(arr)} páginas mantenidas desde el corpus.</p></div><div class="card-grid">{cards}</div>','../'))
    weekly=sorted((WIKI/'weekly').glob('*.md'),reverse=True); latest=weekly[0] if weekly else None
    entities=sorted((WIKI/'entities').glob('*.md'),key=lambda p:p.stat().st_mtime,reverse=True)
    daily=sorted((WIKI/'daily').glob('*.md'),reverse=True)
    concepts=list((WIKI/'concepts').glob('*.md')); comparisons=list((WIKI/'comparisons').glob('*.md'))
    corpus=[]
    for p in files:
        if p.name in ('index.md','log.md'): continue
        corpus.extend(re.findall(r'\[([^]]+)\]\((https?://[^)]+)\)',p.read_text()))
    counts=Counter(label for label,url in corpus)
    most='<section><div class="section-head"><h2>Most Linked</h2><span>señales recurrentes</span></div><ol class="ranked">'+''.join(f'<li><span>{html.escape(k[:88])}</span><b>{v:02d}</b></li>' for k,v in counts.most_common(8))+'</ol></section>'
    hero=f'<a class="hero-card" href="{latest.relative_to(WIKI).with_suffix(".html").as_posix() if latest else "weekly/index.html"}"><span class="eyebrow">Weekly synthesis</span><h1>{html.escape(title_of(latest)) if latest else "La semana en IA"}</h1><p>Una lectura conectada de los cambios, tensiones y señales que atraviesan el corpus.</p><span class="cta">Leer síntesis →</span></a>'
    stats=f'<div class="stats"><span><b>{len(files)}</b> páginas</span><span><b>{len(entities)}</b> entidades</span><span><b>{len(concepts)}</b> conceptos</span><span><b>{len(comparisons)}</b> comparativas</span><span><b>{len(daily)}</b> digests</span></div>'
    body=stats+hero+'<div class="home-grid"><div>'+section_cards('Latest Digests',daily,6)+section_cards('Recently Updated',entities+concepts,8)+'</div><div>'+most+section_cards('Explore Hubs',sorted((WIKI/'hubs').glob('*.md')),5)+'</div></div>'
    (OUT/'index.html').write_text(shell('AI News Wiki',body,'',True))
    (OUT/'assets'/'search-index.json').write_text(json.dumps(docs,ensure_ascii=False))
    (OUT/'assets'/'search.js').write_text("""const q=document.querySelector('#search'),r=document.querySelector('#results');let docs=[];fetch('assets/search-index.json').then(x=>x.json()).then(x=>docs=x);q?.addEventListener('input',()=>{let s=q.value.trim().toLowerCase();if(s.length<2){r.innerHTML='';return}let m=docs.filter(d=>(d.title+' '+d.text).toLowerCase().includes(s)).slice(0,8);r.innerHTML=m.map(d=>`<a href="${d.url}"><b>${d.title}</b><span>${d.type}</span></a>`).join('')||'<i>Sin resultados</i>'});""")
    (OUT/'assets'/'style.css').write_text(CSS)
    (OUT/'.nojekyll').write_text('')
    print(f'Built {len(files)} wiki pages in docs/')
CSS='''
:root{--bg:#0b0d0f;--panel:#111418;--line:#242a30;--text:#e8edf2;--muted:#8c98a4;--cyan:#74c7e8;--green:#8ad6b1;--max:1120px}*{box-sizing:border-box}html{background:var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,sans-serif}body{margin:0}a{color:var(--cyan);text-decoration:none}a:hover{color:#b8e8fb}header{height:58px;border-bottom:1px solid var(--line);display:flex;align-items:center;padding:0 28px;gap:30px;position:sticky;top:0;background:rgba(11,13,15,.94);backdrop-filter:blur(12px);z-index:10}.brand{font-weight:750;color:var(--text);font-size:17px;letter-spacing:-.02em}.brand span{color:var(--cyan)}nav{display:flex;gap:22px;flex:1}nav a,.search-link{font-size:13px;color:var(--muted)}nav a:hover{color:var(--text)}main{max-width:var(--max);margin:0 auto;padding:52px 28px 90px}.stats{font:12px ui-monospace,SFMono-Regular,monospace;color:var(--muted);display:flex;gap:20px;margin-bottom:22px}.stats b{color:var(--text)}.hero-card{display:block;padding:42px;border:1px solid var(--line);border-radius:12px;background:radial-gradient(800px 300px at 0 0,#173442 0,transparent 55%),var(--panel);color:var(--text);margin-bottom:36px}.hero-card h1{max-width:760px;font-size:clamp(34px,5vw,58px);line-height:1.02;letter-spacing:-.045em;margin:12px 0 14px}.hero-card p{color:#a8b3bd;max-width:610px;font-size:17px;line-height:1.6}.eyebrow{text-transform:uppercase;letter-spacing:.13em;color:var(--green);font-size:11px;font-weight:700}.cta{display:inline-block;margin-top:22px;color:var(--cyan);font-weight:650}.home-grid{display:grid;grid-template-columns:1fr 1fr;gap:46px}section{margin:0 0 42px}.section-head{display:flex;align-items:baseline;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:10px}.section-head h2{font-size:12px;text-transform:uppercase;letter-spacing:.12em;margin:0;color:#c3cbd3}.section-head span{font-size:11px;color:var(--muted)}.link-list,.ranked{list-style:none;padding:0;margin:0}.link-list li,.ranked li{border-bottom:1px solid #1c2126;padding:11px 0;display:flex;justify-content:space-between;gap:18px}.link-list a{font-size:14px}.link-list span{display:none}.ranked li span{color:#b8c2cb;font-size:13px}.ranked b{font:12px ui-monospace,monospace;color:var(--muted)}.search-wrap{position:relative;width:250px}.search-wrap input{width:100%;background:#111418;border:1px solid var(--line);color:var(--text);border-radius:6px;padding:9px 12px;outline:none}.search-wrap input:focus{border-color:#426c80}#results{position:absolute;right:0;top:42px;width:420px;background:#111418;border:1px solid var(--line);border-radius:8px;box-shadow:0 16px 50px #000;padding:5px;max-height:420px;overflow:auto}#results:empty{display:none}#results a{display:flex;justify-content:space-between;padding:10px;border-radius:5px;color:var(--text)}#results a:hover{background:#182027}#results span{color:var(--muted);font-size:11px}article{max-width:800px;margin:auto}article h1{font-size:44px;letter-spacing:-.035em;line-height:1.08;margin:14px 0 36px}article h2{margin-top:46px;border-bottom:1px solid var(--line);padding-bottom:10px;font-size:21px}article h3{margin-top:32px;font-size:16px}article p,article li{color:#b7c0c9;line-height:1.7;font-size:15px}article li{margin:8px 0}article code{background:#171b20;border:1px solid var(--line);padding:2px 5px;border-radius:4px;font-size:12px}.meta{color:var(--muted);font:12px ui-monospace,monospace}.page-title{margin-bottom:34px}.page-title h1{font-size:48px;margin:10px 0}.page-title p{color:var(--muted)}.card-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.card{border:1px solid var(--line);border-radius:9px;background:var(--panel);padding:24px;color:var(--text)}.card:hover{border-color:#3b4b56}.card h2{font-size:19px;margin:10px 0}.card p{font-size:13px;line-height:1.55;color:var(--muted)}footer{border-top:1px solid var(--line);padding:24px;text-align:center;color:#5f6972;font-size:12px}@media(max-width:760px){header{padding:0 16px;gap:16px}nav{display:none}.search-wrap{width:auto;flex:1}.home-grid,.card-grid{grid-template-columns:1fr}.hero-card{padding:28px}main{padding:34px 18px 70px}.stats{overflow:auto}.hero-card h1{font-size:36px}article h1{font-size:34px}#results{width:100%}}
'''
if __name__=='__main__': main()
