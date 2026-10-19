from PIL import Image
import json
im=Image.open('/tmp/claude-0/s137/mk/m06/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
cols=[]
for x in range(W):
    ws=[(y,max(0,200-px[x,y])) for y in range(H)]
    tot=sum(w for y,w in ws)
    dark=[y for y,w in ws if w>60]
    cols.append(dict(x=x,ink=tot,top=min(dark) if dark else None,bot=max(dark) if dark else None,
      mean=(sum(y*w for y,w in ws)/tot if tot else None)))
json.dump(cols,open('cols.json','w'))
# per day
for d in range(61):
    a=int(round(d*300/61)); b=int(round((d+1)*300/61))
    cs=[c for c in cols[a:b] if c['top'] is not None]
    if not cs: print(d,'none'); continue
    t=min(c['top'] for c in cs); bt=max(c['bot'] for c in cs)
    m=sum(c['mean']*c['ink'] for c in cs)/sum(c['ink'] for c in cs)
    print(d, a,b, 'top',t,'bot',bt,'range',bt-t,'mean %.1f'%m, 'ink',sum(c['ink'] for c in cs))
