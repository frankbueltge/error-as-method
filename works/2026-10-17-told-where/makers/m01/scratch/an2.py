from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m01/work/record.jpg').convert('L')
W,H=im.size;P=W/61;off=3.96-P
pk=[]
for d in range(62):
  a=off+d*P;b=a+P
  xs=[x for x in range(W) if a<=x+0.5<b]
  if not xs: continue
  top=None
  for y in range(82):
    if any(255-im.getpixel((x,y))>110 for x in xs): top=y;break
  pk.append((d,xs[0],xs[-1],top, 83.5-top if top is not None else None))
for p in pk: print(p)
v=[p[4] for p in pk if p[4] is not None]
n=len(v);print('first 20 mean',sum(v[:20])/20,'last 20',sum(v[-20:])/20)
# 90th percentile peak in windows
def q(s):s=sorted(s);return s[int(.8*len(s))]
print([q(v[i:i+15]) for i in range(0,n-14,5)])
