from PIL import Image
import math, json
g=Image.open('/tmp/claude-0/s137/mk/m08/work/record.jpg').convert('L'); px=g.load()
W,H=g.size
# per-column weighted mean y
cm=[]
for x in range(W):
    ws=[(max(0,200-px[x,y]),y) for y in range(H)]
    s=sum(w for w,_ in ws); cm.append(sum(w*y for w,y in ws)/s if s else float('nan'))
# autocorrelation of detrended
def detr(a,k=15):
    out=[]
    for i in range(len(a)):
        seg=a[max(0,i-k):i+k+1]; out.append(a[i]-sum(seg)/len(seg))
    return out
d=detr(cm)
for lag in range(2,40):
    n=len(d)-lag
    r=sum(d[i]*d[i+lag] for i in range(n))/n
    print(lag, round(r,2), round(lag*1464/300,1),'h')
