from PIL import Image
import math
im=Image.open('/tmp/claude-0/s128/mk/m12/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
cen=[]
for x in range(W):
    ws=[max(0,235-px[x,y]) for y in range(H)]
    t=sum(ws) or 1
    cen.append(sum(y*w for y,w in enumerate(ws))/t)
# detrend with 15px moving avg
k=7
d=[cen[i]-sum(cen[max(0,i-k):i+k+1])/len(cen[max(0,i-k):i+k+1]) for i in range(W)]
res=[]
for f in range(20,150):
    re=sum(d[i]*math.cos(2*math.pi*f*i/W) for i in range(W))
    im_=sum(d[i]*math.sin(2*math.pi*f*i/W) for i in range(W))
    res.append((math.hypot(re,im_),f))
for a,f in sorted(res,reverse=True)[:15]: print(f, round(a,1), 'period hours', round(1464/f,2))
dd=dict((f,a) for a,f in res)
for f in [55,56,57,58,59,60,61,62,63,116,117,118,119,120,121,122,123,124,125]: print('f',f,round(dd[f],1))
cols=[x for x in range(W) if any(px[x,y]<200 for y in range(H))]
print('ink x range',cols[0],cols[-1])
