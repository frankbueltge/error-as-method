from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m03/work/record.jpg').convert('L')
W,H=im.size; p=im.load(); hp=1464/W
def colstats(x):
  ws=[(y,max(0,230-p[x,y])) for y in range(H)]; m=sum(w for _,w in ws)
  if m==0: return None
  c=sum(y*w for y,w in ws)/m
  dk=[y for y,w in ws if w>90]
  return c, (min(dk) if dk else None),(max(dk) if dk else None), m
S=[colstats(x) for x in range(298)]
def pg(series,name):
  xs=[i for i,v in enumerate(series) if v is not None]; vs=[series[i] for i in xs]; mu=sum(vs)/len(vs)
  out=[]
  for Th in [h/10 for h in range(100,800)]:  # period in hours
    P=Th/hp
    c=sum((v-mu)*math.cos(2*math.pi*x/P) for x,v in zip(xs,vs)); s=sum((v-mu)*math.sin(2*math.pi*x/P) for x,v in zip(xs,vs))
    out.append(((c*c+s*s)/len(xs),Th))
  top=sorted(out,reverse=True)[:5]
  print(name,[(round(a),t) for a,t in top])
  # list local peaks
  pk=[(a,t) for i,(a,t) in enumerate(out[1:-1],1) if a>out[i-1][0] and a>out[i+1][0]]
  print('  peaks',[ (round(a),t) for a,t in sorted(pk,reverse=True)[:8]])
pg([s[0] for s in S],'centroid')
pg([s[1] for s in S],'top')
pg([s[2] for s in S],'bottom')
pg([s[3] for s in S],'mass')
pg([ (s[2]-s[1]) if s[1] is not None else None for s in S],'spread')
