from PIL import Image
import math
im=Image.open('/tmp/claude-0/s124/mk/m07/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
cols=[]
for x in range(W):
  ws=[(max(0,200-p[x,y]),y) for y in range(H)]
  tot=sum(w for w,y in ws)
  if tot==0: cols.append(None); continue
  m=sum(w*y for w,y in ws)/tot
  dark=[y for w,y in ws if w>80]
  cols.append((m, min(dark) if dark else m, max(dark) if dark else m, tot))
# fill
mean=[c[0] if c else None for c in cols]
for i in range(W):
  if mean[i] is None: mean[i]=mean[i-1] if i else mean[i+1]
print(' '.join('%d'%(H-m) for m in mean))
print('lo/hi');print(' '.join('%d-%d'%(H-c[2],H-c[1]) if c else '.' for c in cols))
mu=sum(mean)/W; z=[m-mu for m in mean]
# detrend with 15px moving avg
sm=[sum(mean[max(0,i-7):i+8])/len(mean[max(0,i-7):i+8]) for i in range(W)]
r=[mean[i]-sm[i] for i in range(W)]
for lag in range(2,40):
  n=W-lag; c=sum(r[i]*r[i+lag] for i in range(n))/n
  print(lag, round(c,2))
