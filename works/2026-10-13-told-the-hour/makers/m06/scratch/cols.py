import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; p=im.load()
xs=[];top=[];bot=[];mean=[]
for x in range(W):
    w=[(255-p[x,y]) for y in range(H)]
    ys=[y for y in range(H) if p[x,y]<140]
    if not ys: continue
    s=sum(w); m=sum(y*wi for y,wi in enumerate(w))/s
    xs.append(x);top.append(min(ys));bot.append(max(ys));mean.append(m)
print('x range',xs[0],xs[-1],len(xs))
for i in range(len(xs)):
    print(xs[i],top[i],bot[i],round(mean[i],1))
# autocorrelation of mean
import statistics
mu=statistics.mean(mean); d=[v-mu for v in mean]
for lag in range(1,60):
    c=sum(d[i]*d[i+lag] for i in range(len(d)-lag))/sum(v*v for v in d)
    print('lag',lag,round(c,3))
