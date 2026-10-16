from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m11/work/record.jpg').convert('L'); p=im.load()
W,H=im.size
d=[[max(0,255-p[x,y]-15) for y in range(H)] for x in range(W)]
x0,x1=3.0,296.0; hpp=1463/(x1-x0)
for P in (24.0,24.84,25.82,23.93,12.42):
  bins=[[0,0] for _ in range(12)]
  for x in range(2,298):
    s=sum(d[x]); 
    if s<300: continue
    c=sum(y*v for y,v in enumerate(d[x]))/s
    ph=((x-x0)*hpp % P)/P
    b=int(ph*12)%12; bins[b][0]+=c; bins[b][1]+=1
  prof=[b[0]/b[1] for b in bins]
  print(P, ' '.join('%.1f'%v for v in prof), 'range %.1f'%(max(prof)-min(prof)))
# diurnal amplitude by 6-day windows
print('windows')
for w0 in range(3,296,30):
  re=im_=0;n=0;cs=[]
  for x in range(w0,min(w0+30,297)):
    s=sum(d[x]); c=sum(y*v for y,v in enumerate(d[x]))/s; cs.append((x,c))
  m=sum(c for _,c in cs)/len(cs)
  for x,c in cs:
    a=2*math.pi*(x-x0)*hpp/24; re+=(c-m)*math.cos(a); im_+=(c-m)*math.sin(a)
  print(w0, 'amp %.2f phase %.0f mean %.1f'%(2*math.hypot(re,im_)/len(cs), math.degrees(math.atan2(im_,re)), m))
