import json
from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m06/work/record.jpg').convert('L')
W,H=im.size;px=im.load()
D=[[255-px[x,y] for x in range(W)] for y in range(H)]
# baseline profile
prof=[max(D[83][x],D[84][x]) for x in range(W)]
# night blocks via threshold 120, subpixel edges
blocks=[];x=0
while x<W:
  if prof[x]>=120:
    s=x
    while x<W and prof[x]>=120: x+=1
    e=x-1
    # subpixel edges at level 120
    def interp(a,b):  # a below, b above threshold -> fraction
      return (120-prof[a])/(prof[b]-prof[a]) if prof[b]!=prof[a] else 0.5
    le = s-1+interp(s-1,s) if s>0 else s
    re = e+1-interp(e+1,e) if e<W-1 else e
    blocks.append((le,re))
  else: x+=1
print(len(blocks))
cent=[(a+b)/2 for a,b in blocks]
import statistics
per=(cent[-1]-cent[0])/(len(cent)-1)
pxh=per/24
print('period px',per,'px/h',pxh)
light=[]
for k in range(len(blocks)-1):
  gap=blocks[k+1][0]-blocks[k][1]
  hrs=(gap+1.6)/pxh-1   # rough
  light.append(hrs)
print([round(h,1) for h in light])
nightw=[b-a for a,b in blocks]
print([round(n,2) for n in nightw])
# dots: local maxima above baseline
Y0=83.5;YT=5.5
dots=[]
for y in range(1,82):
  for x in range(1,W-1):
    v=D[y][x]
    if v<70: continue
    nb=[D[y+dy][x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dx,dy)!=(0,0)]
    # strict max w/ tie-breaking
    if all(v>n or (v==n and (dy,dx)<(0,0)) for n,(dy,dx) in zip(nb,[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dx,dy)!=(0,0)])):
      sw=sx=sy=0
      for dy in (-1,0,1):
        for dx in (-1,0,1):
          w=D[y+dy][x+dx]; sw+=w; sx+=w*(x+dx); sy+=w*(y+dy)
      dots.append((sx/sw,sy/sw,v))
print('dots',len(dots))
# assign to days
days=[[] for _ in range(len(cent)+1)]
for x,y,v in dots:
  k=sum(1 for c in cent if c<=x)
  ph=None
  if 0<k<len(cent): ph=(x-cent[k-1])/(cent[k]-cent[k-1])*24
  elif k==0: ph=24-(cent[0]-x)/pxh
  else: ph=(x-cent[-1])/pxh
  val=max(0,min(1,(Y0-y)/(Y0-YT)))
  days[k].append([round(ph,2),round(val,3)])
for k,d in enumerate(days):
  d.sort()
  print(k,len(d),round(max([v for _,v in d]+[0]),2), ' '.join('%.0f'%(v*100) for _,v in sorted(d,key=lambda t:-t[1])))
json.dump({'days':days,'light':light,'night':nightw},open('data.json','w'))
