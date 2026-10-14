import json, math
pts=[tuple(map(int,t)) for t in zip(*[iter(open('pts.txt').read().split(','))]*3)]
P=295/61.0; X0=3
# fold profile, finer, with local detrend by 1-day running mean of pixel y
from collections import defaultdict
byx=defaultdict(list)
for x,y,w in pts: byx[x].append((y,w))
def cm(x):
    c=byx.get(x); 
    return None if not c else sum(y*w for y,w in c)/sum(w for _,w in c)
def base(x):
    v=[cm(i) for i in range(x-2,x+3) if cm(i) is not None]; return sum(v)/len(v)
B=12; acc=[0]*B; wt=[0]*B
for x,y,w in pts:
    ph=((x-X0)/P)%1; k=int(ph*B); acc[k]+=(y-base(x))*w; wt[k]+=w
prof=[acc[k]/wt[k] for k in range(B)]
mu=sum(prof)/B; rng=max(prof)-min(prof); shape=[(p-mu)/rng for p in prof]
print('shape',[round(s,2) for s in shape])
def s_at(ph):  # periodic linear interp at bin centers
    u=ph*B-0.5; i=math.floor(u); f=u-i
    return shape[i%B]*(1-f)+shape[(i+1)%B]*f
days=[]
for d in range(61):
    xa=X0+P*d; xb=xa+P
    sel=[(y,w,s_at(((x-X0)/P)%1)) for x,y,w in pts if xa-0.5<=x<xb+0.5]
    W=sum(w for y,w,s in sel); 
    Sy=sum(w*y for y,w,s in sel); Ss=sum(w*s for y,w,s in sel); Sss=sum(w*s*s for y,w,s in sel); Sys=sum(w*y*s for y,w,s in sel)
    det=W*Sss-Ss*Ss; a=(W*Sys-Ss*Sy)/det; b=(Sy-a*Ss)/W
    lo=min(y for y,_,_ in sel); hi=max(y for y,_,_ in sel)
    days.append(dict(b=round(b,1),a=round(a,1),lo=lo,hi=hi))
for i,dd in enumerate(days): print(i,dd)
json.dump(dict(shape=shape,days=days),open('fit.json','w'))
