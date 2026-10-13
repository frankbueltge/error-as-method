from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s123/mk/m10/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
ink=[[max(0,255-px[x,y])/255 for x in range(W)] for y in range(H)]
# column profiles
colsum=[sum(ink[y][x] for y in range(H)) for x in range(W)]
colmean=[sum(ink[y][x]*y for y in range(H))/max(1e-9,colsum[x]) for x in range(W)]
# upper and lower envelope per column (ink>0.4)
top=[];bot=[]
for x in range(W):
    ys=[y for y in range(H) if ink[y][x]>0.35]
    top.append(min(ys) if ys else None); bot.append(max(ys) if ys else None)
json.dump(dict(colsum=colsum,colmean=colmean,top=top,bot=bot),open('cols.json','w'))
print('total ink',sum(colsum))
# autocorrelation of colmean detrended
n=W
def detrend(a,k=15):
    out=[]
    for i in range(n):
        lo=max(0,i-k);hi=min(n,i+k+1)
        out.append(a[i]-sum(a[lo:hi])/(hi-lo))
    return out
for name,a in [('mean',colmean),('top',[t if t is not None else 45 for t in top]),('bot',[b if b is not None else 45 for b in bot]),('sum',colsum)]:
    d=detrend(a)
    v=sum(x*x for x in d)/n
    ac=[sum(d[i]*d[i+l] for i in range(n-l))/(n-l)/v for l in range(1,40)]
    print(name,' '.join(f'{l+1}:{c:.2f}' for l,c in enumerate(ac)))
