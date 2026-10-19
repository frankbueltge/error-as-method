import json
seq=json.load(open('seq.json'))
from collections import defaultdict
col=defaultdict(list)
for x,y in seq: col[x].append(y)
pts=[]
for x in sorted(col):
    n=len(col[x])
    for k,y in enumerate(col[x]): pts.append((x-0.5+(k+0.5)/n, y))
x0,x1=pts[0][0],pts[-1][0]
N=1464; out=[]; j=0
for i in range(N):
    t=x0+(x1-x0)*i/(N-1)
    while j<len(pts)-2 and pts[j+1][0]<t: j+=1
    (a,ya),(b,yb)=pts[j],pts[j+1]
    f=0 if b==a else min(1,max(0,(t-a)/(b-a)))
    y=ya+(yb-ya)*f
    out.append(round(1-(y-4)/(86-4),3))  # 0 bottom,1 top approx
json.dump(out,open('series.json','w'))
for d in range(61):
    row=out[d*24:(d+1)*24]
    print('%2d'%d, ''.join(' .:-=+*#%@'[min(9,int(v*10))] for v in row), round(max(row),2), round(min(row),2), row.index(max(row)))
