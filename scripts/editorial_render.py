"""Small, side-effect-free editorial rendering rules shared with tests."""
import re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

def source_key(url):
    p=urlsplit(url or '')
    query=[(k,v) for k,v in parse_qsl(p.query,keep_blank_values=True)
           if not k.lower().startswith('utm_') and k.lower() not in {'fbclid','gclid','ref','st'}]
    return urlunsplit((p.scheme.lower(),p.netloc.lower().removeprefix('www.'),p.path.rstrip('/'),urlencode(sorted(query)),''))

def complete_excerpt(text, title='This item'):
    # Preserve all authored evidence limits, including later paragraphs.
    # A source/feed may itself end mid-sentence. Never publish that fragment
    # as connected narrative, and never invent its missing ending.
    paragraph=re.sub(r'\s+',' ',text).strip()
    if re.search(r'(?:…|\.\.\.)$',paragraph):
        sentences=re.findall(r'.*?[.!?](?=\s|$)',paragraph)
        complete=[v.strip() for v in sentences if v.strip() and not re.search(r'https?://',v)]
        if complete:
            return ' '.join(complete)+' The remaining source excerpt is incomplete.'
        return f'The feed lists "{title}". The available source excerpt is incomplete; details could not be established from it.'
    return paragraph

def group_sources(items):
    groups={}
    for item in items:
        key=source_key(item.get('url')) or item['id']
        groups.setdefault(key,[]).append(item)
    return list(groups.values())
