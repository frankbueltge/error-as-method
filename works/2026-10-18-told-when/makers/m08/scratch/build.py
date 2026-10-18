import json
M=json.load(open('M.json'))
# quantize darkness to 0..9 per column per level (0 = absent)
rows=[]
for k in range(18):
    s=''
    for x in range(300):
        d=M[x][k]
        s+= '0' if d<90 else str(min(9,1+int((d-90)/18)))
    rows.append(s)
data=json.dumps(rows)
html=open('template.html').read().replace('__DATA__',data)
open('/tmp/claude-0/s135/mk/m08/work/index.html','w').write(html)
print(len(html))
