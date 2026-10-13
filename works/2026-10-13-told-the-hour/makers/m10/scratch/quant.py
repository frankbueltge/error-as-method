from PIL import Image
import json
im=Image.open('/tmp/claude-0/s123/mk/m10/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
N=1464; x0,x1=1.0,298.0
xs=[x0+i*(x1-x0)/(N-1) for i in range(N)]
cols={}
for i,x in enumerate(xs): cols.setdefault(int(round(x)),[]).append(i)
ink=lambda x,y: max(0,255-px[x,y]-25) if 0<=x<W else 0
vals=[None]*N
colmean={}
for c,idx in cols.items():
    prof=[ink(c,y)+0.4*(ink(c-1,y)+ink(c+1,y)) for y in range(H)]
    tot=sum(prof); k=len(idx)
    cum=0; qs=[]; targets=[(j+0.5)/k*tot for j in range(k)]; t=0
    for y in range(H):
        prev=cum; cum+=prof[y]
        while t<k and cum>=targets[t]:
            frac=(targets[t]-prev)/prof[y] if prof[y] else 0
            qs.append(y-0.5+frac); t+=1
    colmean[c]=sum(qs)/len(qs); cols[c]=(idx,qs)
cs=sorted(cols)
for n,c in enumerate(cs):
    idx,qs=cols[c]
    a=colmean[cs[max(0,n-1)]]; b=colmean[cs[min(len(cs)-1,n+1)]]
    # y increases downward; if next col lower on screen (b>a) values falling -> y ascending in time
    order=sorted(qs) if b>=a else sorted(qs,reverse=True)
    for i,y in zip(idx,order): vals[i]=y
v=[(90-y) for y in vals]  # larger = higher
json.dump(v,open('series.json','w'))
print(min(v),max(v))
