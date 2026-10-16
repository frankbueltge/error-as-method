import numpy as np
from PIL import Image
im=np.asarray(Image.open('/tmp/claude-0/s131/mk/m04/work/record.jpg').convert('L')).astype(float)
D=np.clip((255-im)/255,0,1)
H,W=D.shape
# light vertical blur
from numpy import convolve
K=np.array([.25,.5,.25])
Db=np.array([np.convolve(D[:,x],K,'same') for x in range(W)]).T
N=1464; x0,x1=2.6,296.6
xs=x0+np.arange(N)*(x1-x0)/(N-1)
ys=np.arange(H)
# emission via linear interp in x
xi=np.floor(xs).astype(int); fr=xs-xi
E=np.array([(1-f)*Db[:,i]+f*Db[:,min(i+1,W-1)] for i,f in zip(xi,fr)])  # N x H
cost_e=-np.log(E+0.03)
lam=float(__import__("os").environ.get("LAM","0.02"))
dy=ys[:,None]-ys[None,:]
T=lam*np.abs(dy)
acc=cost_e[0].copy(); back=np.zeros((N,H),int)
for t in range(1,N):
    m=acc[None,:]+T  # [to,from]
    back[t]=m.argmin(1); acc=m.min(1)+cost_e[t]
path=np.zeros(N,int); path[-1]=acc.argmin()
for t in range(N-1,0,-1): path[t-1]=back[t,path[t]]
# subpixel refine: weighted centroid within +-2
v=[]
for t,y in enumerate(path):
    lo,hi=max(0,y-2),min(H,y+3); w=E[t,lo:hi]+1e-6
    v.append((w*ys[lo:hi]).sum()/w.sum())
v=np.array(v)
val=(H-1-v)  # larger up
np.save('vals.npy',val)
# coverage check: fraction of dark pixels within 1.5px of path at their column
dark=np.argwhere(D>0.3); 
covered=0
for y,x in dark:
    ts=np.where(np.abs(xs-x)<0.8)[0]
    if len(ts) and np.min(np.abs(v[ts]-y))<=2.0: covered+=1
print('coverage',covered/len(dark), len(dark))
# overlay
from PIL import ImageDraw
big=Image.open('/tmp/claude-0/s131/mk/m04/work/record.jpg').convert('RGB').resize((W*4,H*4),Image.NEAREST)
dr=ImageDraw.Draw(big)
pts=[(xs[t]*4+2,v[t]*4+2) for t in range(N)]
dr.line(pts,fill=(255,0,0),width=1)
big.save('overlay.png')
d=val.reshape(61,24)
np.set_printoptions(linewidth=200,precision=0,suppress=True)
print(d[:8])
