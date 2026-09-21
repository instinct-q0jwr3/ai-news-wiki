#!/usr/bin/env python3
"""Build a dependency-free GitHub Pages site from wiki Markdown."""
from __future__ import annotations
import html,json,re,shutil,time
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; WIKI=ROOT/'wiki'; OUT=ROOT/'docs'
LABELS={'hubs':'Hubs','weekly':'Weekly','entities':'Entities','daily':'Digests','summaries':'Stories','concepts':'Concepts','comparisons':'Compare','topics':'Topics','trends':'Trends'}

NEW_BADGE='<span class="new-badge" title="Added in the latest update">new</span>'
def inline(s):
    s=html.escape(s,quote=False)
    s=s.replace('{new}',NEW_BADGE)
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

def slugify(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

def meta_of(p):
    meta={'type':'','created':'','updated':'','confidence':'','tags':[]}
    for line in p.read_text().splitlines()[1:9]:
        s=line.strip()
        m=re.match(r'^_type:\s*(.+?)\s*·\s*created:\s*(\S+)\s*·\s*updated:\s*(\S+)\s*·\s*confidence:\s*(\S+)_$',s)
        if m:
            meta['type'],meta['created'],meta['updated'],meta['confidence']=m.groups(); continue
        if s and re.fullmatch(r'(`[^`]+`\s*)+',s):
            meta['tags']=re.findall(r'`([^`]+)`',s); continue
        m=re.match(r'^Sources:\s*(.+?)\.?$',s)
        if m and not meta['tags']:
            meta['tags']=[slugify(x) for x in re.split(r',|\sand\s',m.group(1)) if x.strip()]; continue
    if not meta['updated']:
        m=re.search(r'(\d{4}-\d{2}-\d{2})',p.stem) or re.search(r'(\d{4}-W\d{2})',p.stem)
        if m: meta['updated']=m.group(1)
    return meta

def row_html(p,link,is_new=False):
    m=meta_of(p)
    tags=' '.join(m['tags'])
    chips=''.join(f'<code>{html.escape(t)}</code>' for t in m['tags'])
    meta=f"upd {m['updated']}" if m['updated'] else ''
    badge=NEW_BADGE if is_new else ''
    return (f'<li class="row" data-tags="{html.escape(tags,quote=True)}">'
            f'<a class="row-title" href="{link}">{html.escape(title_of(p))}</a>{badge}'
            f'<span class="row-tags">{chips}</span><span class="row-meta">{meta}</span></li>')

FILTER_JS='''<script>
document.querySelectorAll('.filter-bar').forEach(function(bar){
  var list=bar.parentElement.querySelector('.row-list'); if(!list) return;
  bar.addEventListener('click',function(e){
    var b=e.target.closest('.chip'); if(!b) return;
    bar.querySelectorAll('.chip').forEach(function(c){c.classList.toggle('active',c===b)});
    var t=b.dataset.tag;
    list.querySelectorAll('.row').forEach(function(r){
      r.style.display=(!t||r.dataset.tags.split(' ').indexOf(t)>=0)?'':'none';
    });
  });
});
</script>'''

FILTER_JS_GROUPS='''<script>
document.querySelectorAll('.filter-bar').forEach(function(bar){
  var scope=bar.parentElement; if(!scope) return;
  var groups=Array.prototype.slice.call(scope.querySelectorAll('.tree > details'));
  groups.forEach(function(g){g.dataset.init=g.open?'1':''});
  bar.addEventListener('click',function(e){
    var b=e.target.closest('.chip'); if(!b) return;
    bar.querySelectorAll('.chip').forEach(function(c){c.classList.toggle('active',c===b)});
    var t=b.dataset.tag;
    scope.querySelectorAll('.row').forEach(function(r){
      r.style.display=(!t||r.dataset.tags.split(' ').indexOf(t)>=0)?'':'none';
    });
    groups.forEach(function(g){
      var any=Array.prototype.some.call(g.querySelectorAll('.row'),function(r){return r.style.display!=='none'});
      g.style.display=any?'':'none';
      g.open=t?any:g.dataset.init==='1';
    });
  });
});
</script>'''

def filter_bar(tagcount):
    if len(tagcount)<2: return ''
    chips=''.join(f'<button class="chip" data-tag="{html.escape(t,quote=True)}">{html.escape(t)}<span>{c}</span></button>' for t,c in tagcount.most_common())
    return f'<div class="filter-bar"><button class="chip active" data-tag="">All</button>{chips}</div>'

BUILD_V=str(int(time.time()))
NAV=[('hubs','Hubs'),('weekly','Weekly'),('entities','Entities'),('daily','Digests'),('summaries','Stories'),('concepts','Concepts'),('comparisons','Compare')]
def shell(title,content,rel='',search=False,section=''):
    nav=''.join(f'<a href="{rel}{k}/index.html"'+((' class="active" aria-current="page"') if k==section else '')+f'>{v}</a>' for k,v in NAV)
    box='<div class="search-wrap"><input id="search" type="search" placeholder="Search the wiki…" autocomplete="off"><div id="results"></div></div>' if search else '<a class="search-link" href="'+rel+'index.html#search">Search</a>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · AI Wiki</title><link rel="stylesheet" href="{rel}assets/style.css?v={BUILD_V}"></head><body><header><a class="brand" href="{rel}index.html"><span>AI</span> wiki</a><nav>{nav}</nav>{box}</header><main>{content}</main><footer>AI News Wiki · Sources linked in every entry</footer>{'<script src="assets/search.js"></script>' if search else ''}</body></html>'''

def section_list(name,files,limit=5):
    rows=[]
    for p in files[:limit]:
        rel=p.relative_to(WIKI).with_suffix('.html').as_posix(); rows.append(row_html(p,rel))
    return f'<section><div class="section-head"><h2>{name}</h2></div><ul class="row-list">'+''.join(rows)+'</ul></section>'

def load_new():
    f=WIKI/'new.json'
    if not f.exists(): return set(),[]
    try:
        d=json.loads(f.read_text())
        return {x['id'] for x in d.get('stories',[])},d.get('stories',[])
    except Exception: return set(),[]

def main():
    NEW_IDS,NEW_STORIES=load_new()
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT/'assets').mkdir(parents=True)
    files=sorted(WIKI.rglob('*.md'))
    docs=[]
    for p in files:
        relpath=p.relative_to(WIKI).with_suffix('.html'); dest=OUT/relpath; dest.parent.mkdir(parents=True,exist_ok=True)
        rel='../'*len(relpath.parent.parts); text=p.read_text(); title=title_of(p)
        sec=relpath.parts[0] if len(relpath.parts)>1 and relpath.parts[0] in dict(NAV) else ''
        dest.write_text(shell(title,f'<article>{render_md(text)}</article>',rel,section=sec))
        plain=re.sub(r'[#*_`\[\]()]',' ',text)
        if p.name=='log.md': continue
        docs.append({'title':title,'url':relpath.as_posix(),'text':re.sub(r'\s+',' ',plain)[:2400],'type':p.parent.name})
    for folder,label in LABELS.items():
        d=WIKI/folder
        if not d.exists(): continue
        arr=sorted(d.glob('*.md'),reverse=True)
        tagcount=Counter()
        for p in arr:
            for t in meta_of(p)['tags']: tagcount[t]+=1
        if folder=='summaries':
            groups={}
            for p in arr:
                m=meta_of(p); day=m['created'] or m['updated'] or 'undated'
                groups.setdefault(day,[]).append(p)
            parts=[]
            for i,day in enumerate(sorted(groups,reverse=True)):
                rows=''.join(row_html(p,f'{p.stem}.html',is_new=(p.stem in NEW_IDS)) for p in sorted(groups[day],key=lambda p:title_of(p)))
                openattr=' open' if i<3 else ''
                parts.append(f'<details class="ty"{openattr}><summary>{day}<span class="tc">{len(groups[day])} stories</span></summary><ul class="row-list tree-list" style="margin-left:32px">{rows}</ul></details>')
            body=(f'<div class="page-title"><span class="eyebrow">Library</span><h1>{label}</h1>'
                  f'<p>{len(arr)} pages maintained from the corpus, grouped by first-seen date.</p></div>'
                  f'{filter_bar(tagcount)}<div class="tree">' + ''.join(parts) + f'</div>{FILTER_JS_GROUPS}')
        else:
            rows=''.join(row_html(p,f'{p.stem}.html',is_new=(folder=='summaries' and p.stem in NEW_IDS)) for p in arr)
            body=(f'<div class="page-title"><span class="eyebrow">Library</span><h1>{label}</h1>'
                  f'<p>{len(arr)} pages maintained from the corpus.</p></div>'
                  f'{filter_bar(tagcount)}<ul class="row-list">{rows}</ul>{FILTER_JS}')
        (OUT/folder/'index.html').write_text(shell(label,body,'../',section=folder if folder in dict(NAV) else ''))
    weekly=sorted((WIKI/'weekly').glob('*.md'),reverse=True); latest=weekly[0] if weekly else None
    entities=sorted((WIKI/'entities').glob('*.md'),key=lambda p:p.stat().st_mtime,reverse=True)
    daily=sorted((WIKI/'daily').glob('*.md'),reverse=True)
    concepts=list((WIKI/'concepts').glob('*.md')); comparisons=list((WIKI/'comparisons').glob('*.md'))
    corpus=[]
    for p in files:
        if p.name in ('index.md','log.md'): continue
        corpus.extend(re.findall(r'\[([^]]+)\]\((https?://[^)]+)\)',p.read_text()))
    counts=Counter(label for label,url in corpus)
    most='<section><div class="section-head"><h2>Most Linked</h2><span>recurring signals</span></div><ol class="ranked">'+''.join(f'<li><span>{html.escape(k[:88])}</span><b>{v:02d}</b></li>' for k,v in counts.most_common(8))+'</ol></section>'
    hero=f'<a class="hero" href="{latest.relative_to(WIKI).with_suffix(".html").as_posix() if latest else "weekly/index.html"}"><span class="eyebrow">Weekly synthesis</span><h1>{html.escape(title_of(latest)) if latest else "The week in AI"}</h1><p>A connected read of the changes, tensions and signals running through the corpus.</p><span class="cta">Read the synthesis →</span></a>'
    stats=f'<div class="stats"><span><b>{len(files)}</b> pages</span><span><b>{len(entities)}</b> entities</span><span><b>{len(concepts)}</b> concepts</span><span><b>{len(comparisons)}</b> comparisons</span><span><b>{len(daily)}</b> digests</span></div>'
    if NEW_STORIES:
        nrows=''.join(f'<li class="row"><a class="row-title" href="summaries/{html.escape(x["id"],quote=True)}.html">{html.escape(x.get("title",""))}</a>{NEW_BADGE}<span class="row-meta">{html.escape(x.get("source",""))}</span></li>' for x in NEW_STORIES)
        newsec=f'<section><div class="section-head"><h2>New this update</h2><span>{len(NEW_STORIES)} added in the latest pass</span></div><ul class="row-list">{nrows}</ul></section>'
    else:
        newsec=''
    body=stats+hero+newsec+'<div class="home-grid"><div>'+section_list('Latest Digests',daily,6)+section_list('Recently Updated',entities+concepts,8)+'</div><div>'+most+section_list('Explore Hubs',sorted((WIKI/'hubs').glob('*.md')),5)+'</div></div>'
    (OUT/'index.html').write_text(shell('AI News Wiki',body,'',True))
    (OUT/'assets'/'search-index.json').write_text(json.dumps(docs,ensure_ascii=False))
    (OUT/'assets'/'search.js').write_text("""const q=document.querySelector('#search'),r=document.querySelector('#results');let docs=[];fetch('assets/search-index.json').then(x=>x.json()).then(x=>docs=x);q?.addEventListener('input',()=>{let s=q.value.trim().toLowerCase();if(s.length<2){r.innerHTML='';return}let m=docs.filter(d=>(d.title+' '+d.text).toLowerCase().includes(s)).slice(0,8);r.innerHTML=m.map(d=>`<a href="${d.url}"><b>${d.title}</b><span>${d.type}</span></a>`).join('')||'<i>No results</i>'});""")
    (OUT/'assets'/'style.css').write_text(CSS)
    (OUT/'.nojekyll').write_text('')
    print(f'Built {len(files)} wiki pages in docs/')

CSS='''
:root{--bg:#0b0d0f;--panel:#111418;--line:#242a30;--text:#e8edf2;--muted:#8c98a4;--cyan:#74c7e8;--green:#8ad6b1;--max:1120px}*{box-sizing:border-box}html{background:var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,sans-serif}body{margin:0}a{color:var(--cyan);text-decoration:none}a:hover{color:#b8e8fb}header{height:58px;border-bottom:1px solid var(--line);display:flex;align-items:center;padding:0 28px;gap:30px;position:sticky;top:0;background:rgba(11,13,15,.94);backdrop-filter:blur(12px);z-index:10}.brand{font-weight:750;color:var(--text);font-size:17px;letter-spacing:-.02em}.brand span{color:var(--cyan)}nav{display:flex;gap:22px;flex:1}nav a,.search-link{font-size:13px;color:var(--muted)}nav a:hover{color:var(--text)}nav a.active{color:var(--text);font-weight:700;border-bottom:2px solid var(--cyan);padding-bottom:2px}main{max-width:var(--max);margin:0 auto;padding:52px 28px 90px}.stats{font:12px ui-monospace,SFMono-Regular,monospace;color:var(--muted);display:flex;gap:20px;margin-bottom:22px}.stats b{color:var(--text)}.hero{display:block;color:var(--text);margin:0 0 44px}.hero h1{max-width:820px;font-size:clamp(34px,5vw,58px);line-height:1.02;letter-spacing:-.045em;margin:12px 0 14px;color:var(--text)}.hero p{color:#a8b3bd;max-width:610px;font-size:17px;line-height:1.6}.eyebrow{text-transform:uppercase;letter-spacing:.13em;color:var(--green);font-size:11px;font-weight:700}.cta{display:inline-block;margin-top:18px;color:var(--cyan);font-weight:650}.home-grid{display:grid;grid-template-columns:1fr 1fr;gap:46px}section{margin:0 0 42px}.section-head{display:flex;align-items:baseline;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:10px}.section-head h2{font-size:12px;text-transform:uppercase;letter-spacing:.12em;margin:0;color:#c3cbd3}.section-head span{font-size:11px;color:var(--muted)}.ranked{list-style:none;padding:0;margin:0}.ranked li{border-bottom:1px solid #1c2126;padding:11px 0;display:flex;justify-content:space-between;gap:18px}.ranked li span{color:#b8c2cb;font-size:13px}.ranked b{font:12px ui-monospace,monospace;color:var(--muted)}.filter-bar{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 20px}.chip{font:12px ui-monospace,SFMono-Regular,monospace;background:transparent;border:1px solid var(--line);color:var(--muted);border-radius:999px;padding:5px 12px;cursor:pointer}.chip span{color:var(--cyan);margin-left:7px}.chip:hover{border-color:#3b4b56;color:var(--text)}.chip.active{background:var(--cyan);border-color:var(--cyan);color:#06222e}.chip.active span{color:#06222e}.row-list{list-style:none;padding:0;margin:0 0 42px}.row{display:flex;align-items:baseline;gap:14px;border-bottom:1px solid #1c2126;padding:9px 0}.row-title{font-size:14px;flex:1;min-width:180px}.row-tags{display:flex;gap:6px;flex-wrap:wrap}.row-tags code{background:#171b20;border:1px solid var(--line);padding:1px 5px;border-radius:4px;font-size:11px;color:var(--cyan);white-space:nowrap}.new-badge{display:inline-block;font:10px ui-monospace,SFMono-Regular,monospace;text-transform:uppercase;letter-spacing:.08em;color:var(--green);border:1px solid #2c4a3b;border-radius:999px;padding:1px 7px;margin-left:8px;vertical-align:middle;white-space:nowrap}.row-meta{font:11px ui-monospace,SFMono-Regular,monospace;color:var(--muted);white-space:nowrap}.search-wrap{position:relative;width:250px}.search-wrap input{width:100%;background:#111418;border:1px solid var(--line);color:var(--text);border-radius:6px;padding:9px 12px;outline:none}.search-wrap input:focus{border-color:#426c80}#results{position:absolute;right:0;top:42px;width:420px;background:#111418;border:1px solid var(--line);border-radius:8px;box-shadow:0 16px 50px #000;padding:5px;max-height:420px;overflow:auto}#results:empty{display:none}#results a{display:flex;justify-content:space-between;padding:10px;border-radius:5px;color:var(--text)}#results a:hover{background:#182027}#results span{color:var(--muted);font-size:11px}article{max-width:800px;margin:auto}article h1{font-size:clamp(25px,3.2vw,32px);letter-spacing:-.025em;line-height:1.16;margin:12px 0 26px}article h2{margin-top:46px;border-bottom:1px solid var(--line);padding-bottom:10px;font-size:21px}article h3{margin-top:32px;font-size:16px}article p,article li{color:#b7c0c9;line-height:1.7;font-size:15px}article li{margin:8px 0}article>p.meta+ p code{display:inline-block;margin:3px 4px 3px 0;color:var(--cyan)}article code{background:#171b20;border:1px solid var(--line);padding:2px 5px;border-radius:4px;font-size:12px}.meta{color:var(--muted);font:12px ui-monospace,monospace}.page-title{margin-bottom:28px}.page-title h1{font-size:clamp(28px,3.6vw,36px);margin:10px 0}.page-title p{color:var(--muted)}footer{border-top:1px solid var(--line);padding:24px;text-align:center;color:#5f6972;font-size:12px}@media(max-width:760px){article p,article li{font-size:16px;line-height:1.72}article h2{margin-top:38px}.page-title h1{font-size:28px}header{padding:10px 16px;gap:8px 16px;flex-wrap:wrap;height:auto}nav{display:flex;order:3;flex:1 1 100%;overflow-x:auto;gap:18px;padding-bottom:4px;scrollbar-width:none}nav::-webkit-scrollbar{display:none}nav a{white-space:nowrap}.search-wrap{width:auto;flex:1}.home-grid{grid-template-columns:1fr}main{padding:34px 18px 70px}.stats{overflow:auto}.hero h1{font-size:36px}article h1{font-size:25px}#results{width:100%}.row{flex-wrap:wrap;gap:6px 12px;padding:10px 0}.row-title{flex:1 1 100%}.row-meta{margin-left:auto}}.tree details{margin:0 0 2px}.tree summary{cursor:pointer;list-style:none;font:700 15px/1.9 ui-monospace,monospace;color:#e8edf3;user-select:none}.tree summary::before{content:"+";display:inline-block;width:16px;color:#6b7684}.tree details[open]>summary::before{content:"-"}.tree .tc{margin-left:10px;font:400 11px ui-monospace,monospace;color:#6b7684}.tree .tm{margin-left:16px}.tree .td{margin-left:32px}.tree .td summary{font:400 12px/2 ui-monospace,monospace;color:#9aa5b1}.tree .tree-list{margin-left:48px;margin-bottom:10px}
'''
if __name__=='__main__': main()
