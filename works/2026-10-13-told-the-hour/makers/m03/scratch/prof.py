from PIL import Image
im=Image.open('../work/record.jpg').convert('L'); w,h=im.size; px=im.load()
D=[[max(0,230-px[x,y])/230 for y in range(h)] for x in range(w)]
# top envelope: first row (from top) where darkness >0.4
top=[];bot=[];cen=[]
for x in range(w):
    ys=[y for y in range(h) if D[x][y]>0.4]
    top.append(min(ys) if ys else None); bot.append(max(ys) if ys else None)
    s=sum(D[x]); cen.append(sum(y*D[x][y] for y in range(h))/s if s else None)
print('first/last col with ink', [x for x in range(w) if top[x] is not None][0], [x for x in range(w) if top[x] is not None][-1])
print('rows ink range', min(t for t in top if t is not None), max(b for b in bot if b is not None))
import math
c=[v if v is not None else 0 for v in cen]
m=sum(c)/len(c)
# detrend with moving average 35
def ma(a,k):
    out=[]
    for i in range(len(a)):
        lo=max(0,i-k);hi=min(len(a),i+k+1); out.append(sum(a[lo:hi])/(hi-lo))
    return out
t=[v if v is not None else 0 for v in top]
for name,a in (('cen',c),('top',t)):
    s=ma(a,20); r=[a[i]-s[i] for i in range(len(a))][5:-5]
    ac=[]
    for lag in range(2,60):
        n=len(r)-lag; ac.append((lag,sum(r[i]*r[i+lag] for i in range(n))/n))
    print(name, ' '.join(f'{l}:{v:.1f}' for l,v in ac))
print('top', t)
