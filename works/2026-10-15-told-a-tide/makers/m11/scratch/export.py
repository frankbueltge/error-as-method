import json, math
from PIL import Image
im=Image.open('../work/record.jpg').convert('L'); W,H=im.size; px=im.load()
pts=json.load(open('peaks.json')); xs=[p[0] for p in pts]; x0,x1=min(xs),max(xs)
t=lambda x:(x-x0)/(x1-x0)*1463
mv=sum((89-p[1])*p[2] for p in pts)/sum(p[2] for p in pts)
best=max(((lambda re,im:re*re+im*im)(
  sum(p[2]*((89-p[1])-mv)*math.cos(2*math.pi*t(p[0])/P) for p in pts),
  sum(p[2]*((89-p[1])-mv)*math.sin(2*math.pi*t(p[0])/P) for p in pts)),P) for P in [23.9+i*0.005 for i in range(80)])
P=best[1]; print('P',P)
hpp=1463/(x1-x0)*24/P   # hours per source pixel once the cycle is taken as 24 h
print('x0',x0,'hpp',hpp,'span hours', (W-x0)*hpp)
s=[]
for y in range(H):
  for x in range(W):
    d=255-px[x,y]
    if d>=24: s.append(f'{x},{89-y},{d}')
print(len(s))
open('pix.txt','w').write(';'.join(s))
json.dump({'x0':x0,'hpp':hpp},open('cal.json','w'))
