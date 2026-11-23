import re,html,json,sys,hashlib
S=sys.argv[1]
out=[]
for i in ['57-3','57-2','57-1','56-3','56-2','56-1']:
    p=f'{S}/dl/mh{i}.html' if i!='57-3' else f'{S}/dl/mh573h.html'
    raw=open(p,'rb').read(); t=raw.decode('utf-8','replace')
    tables=re.findall(r'<table.*?</table>',t,flags=re.S|re.I)
    poems=[]
    for tb in tables:
        if 'align="right"' not in tb: continue
        parts=re.split(r'<div align="right"',tb,maxsplit=1)
        if len(parts)<2: continue
        body=parts[0]
        body=re.sub(r'<br\s*/?>','\n',body,flags=re.I);body=re.sub(r'</p>|</div>|</td>','\n',body,flags=re.I)
        body=html.unescape(re.sub(r'<[^>]+>','',body))
        lines=[l.strip() for l in body.split('\n') if l.strip()]
        if 0<len(lines)<=8: poems.append({'lines':lines})
    out.append({'issue':i,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'url':f'https://www.modernhaiku.org/issue{i}/haiku.html','poems':poems})
    print(i,len(poems),[x['lines'] for x in poems[:2]])
json.dump(out,open(f'{S}/journal_parsed.json','w'),indent=1,ensure_ascii=False)
