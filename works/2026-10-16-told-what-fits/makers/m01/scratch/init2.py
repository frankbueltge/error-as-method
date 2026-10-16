import numpy as np, sys
from PIL import Image
a=np.array(Image.open('/tmp/claude-0/s131/mk/m01/work/record.jpg').convert('L')).astype(float)
D=np.clip((255-a)/255,0,1); H,W=D.shape; N=1464
x0,x1=float(sys.argv[1]),float(sys.argv[2])
xi=x0+np.arange(N)*(x1-x0)/(N-1)
ci=np.floor(xi).astype(int)
y=np.zeros(N); prev=None
for c in range(W):
    idx=np.where(ci==c)[0]
    if len(idx)==0: continue
    p=D[:,c]**2; 
    if p.sum()<1e-6: p=np.ones(H)
    cdf=np.cumsum(p)/p.sum()
    q=(np.arange(len(idx))+0.5)/len(idx)
    ys=np.interp(q,cdf,np.arange(H)+0.5)
    if prev is not None:
        # choose order (ascending or descending) minimizing jump + internal path
        if abs(ys[0]-prev)>abs(ys[-1]-prev): ys=ys[::-1]
    y[idx]=ys; prev=ys[-1]
np.save('y0.npy',y)
