import json
pts=json.load(open('pts.json'))
pts.sort()
data=','.join(f'{round(x*10)},{round(y*10)},{max(1,round(m/300))}' for x,y,m in pts)
html=open('template.html').read().replace('__DATA__',data)
open('/tmp/claude-0/s123/mk/m12/work/index.html','w').write(html)
print(len(html))
