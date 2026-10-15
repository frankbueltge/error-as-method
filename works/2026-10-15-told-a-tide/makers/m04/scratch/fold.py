from PIL import Image
import math, json
g=Image.open('../work/record.jpg').convert('L'); W,H=g.size; p=g.load()
S=[]
for x in range(W):
  for y in range(H):
    d=max(0,(240-p[x,y]))/240.0
    if d>0.08: S.append((x,y,d))
x0,x1=2.5,296.5  # assumed centres of first/last dot
def t(x): return (x-x0)/(x1-x0)*1463
for P in (24.0,24.84,12.42,12.0,23.93,25.82):
  for thr in (50,):
    C=Sn=Wt=0
    for x,y,d in S:
      if y>thr:
        a=2*math.pi*t(x)/P; C+=d*math.cos(a); Sn+=d*math.sin(a); Wt+=d
    print(P,'deep R=%.2f phase=%.1fh'%(math.hypot(C,Sn)/Wt,(math.atan2(Sn,C)/2/math.pi*P)%P))
# phase-binned mean value at 24h
bins=[[0,0] for _ in range(24)]
for x,y,d in S:
  b=int(t(x)%24)%24; bins[b][0]+=d*y; bins[b][1]+=d
print([round(a/b,1) for a,b in bins])
# long-period: daily mean y
days=[[0,0] for _ in range(62)]
for x,y,d in S:
  k=int(t(x)//24); 
  if 0<=k<62: days[k][0]+=d*y; days[k][1]+=d
print([round(a/b,1) if b else None for a,b in days])
json.dump(S,open('samples.json','w'))
print(len(S))
