import json, numpy as np
c=json.load(open('cols.json'))
xs=[x for x in range(300) if c[x]]
x0,x1=xs[0],xs[-1]; print(x0,x1)
N=1464
# hour i -> x position
pos=x0-0.5+(np.arange(N)+0.5)*(x1-x0+1)/N
cnt={x:int(((pos>=x-0.5)&(pos<x+0.5)).sum()) for x in xs}
series=[]; prev=None
for x in range(x0,x1+1):
    b=sorted(c[x]); n=cnt.get(x,0)
    if n==0: continue
    if not b: b=[series[-1]]
    if prev is not None and abs(b[-1]-prev)<abs(b[0]-prev): b=b[::-1]
    if len(b)==1: vals=[b[0]]*n
    else:
        # ordered path; resample uniformly along index of blobs
        t=np.linspace(0,len(b)-1,n); vals=list(np.interp(t,range(len(b)),b))
    series+=vals; prev=vals[-1]
s=np.array(series); print(len(s), s.min(), s.max())
v=(s.max()-s)/(s.max()-s.min())
json.dump([round(float(a),3) for a in v],open('series.json','w'))
d=v.reshape(61,24)
for r in d: print(''.join(' .:-=+*#%@'[min(9,int(a*10))] for a in r), round(r.mean(),2))
