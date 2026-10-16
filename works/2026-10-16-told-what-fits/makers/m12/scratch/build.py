import numpy as np, json
from PIL import Image, ImageDraw
D=np.load('D.npy')
x0,x1=2,297; P=(x1-x0+1)/61; ph=4.755-P/2  # day centred on its peak
Y0,Y1=4,86
days=[]
for d in range(61):
  a=x0+ph+d*P; b=a+P
  prof=np.zeros(90)
  for c in range(300):
    w=max(0,min(b,c+1)-max(a,c))
    if w>0: prof+=w*D[:,c]
  if prof.sum()==0: prof=None
  days.append(prof)
# first/last days are partial (start before x0/ end after x1) - still has data
out=[]
for d,prof in enumerate(days):
  cdf=np.cumsum(prof); cdf/=cdf[-1]
  q=(np.arange(24)+0.5)/24
  ys=[]
  for qq in q:
    i=np.searchsorted(cdf,qq)
    lo=cdf[i-1] if i>0 else 0
    f=(qq-lo)/max(cdf[i]-lo,1e-9)
    ys.append(round(i+f,2))   # pixel row (0=top), continuous
  out.append(ys)
json.dump(out,open('hours.json','w'))
mx=[min(o) for o in out]; mn=[max(o) for o in out]
print('top',mx); print('bottom',mn)
# source raster, 0-9 digits rows 4..86, cols 2..298
src=''.join(''.join(str(int(round(v*9))) for v in D[r,0:300]) for r in range(90))
open('src.txt','w').write(src)
