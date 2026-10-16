import numpy as np, sys
from PIL import Image
a=np.array(Image.open('/tmp/claude-0/s131/mk/m01/work/record.jpg').convert('L')).astype(float)
D=np.clip((255-a)/255,0,1)
H,W=D.shape
N=1464
x0,x1=float(sys.argv[1]),float(sys.argv[2])
xi=x0+np.arange(N)*(x1-x0)/(N-1)
# pixel grid for each value: 5 columns around
off=np.arange(-2,3)
cols=np.clip(np.floor(xi).astype(int)[:,None]+off[None,:],0,W-1)  # N x 5
cx=cols+0.5
ry=np.arange(H)+0.5
# init: ink-weighted mean y in nearest column
c0=np.clip(np.floor(xi).astype(int),0,W-1)
w=D[:,c0]
y=np.load('/tmp/claude-0/s131/mk/m01/scratch/y0.npy')
def run(y,s,A,iters,lr,lam):
    for it in range(iters):
        dx=(cx-xi[:,None])           # N x5
        dy=(ry[None,:]-y[:,None])    # N x H
        g=A*np.exp(-dx[:,:,None]**2/(2*s*s))*np.exp(-dy[:,None,:]**2/(2*s*s))  # N x5 x H
        S=np.zeros((W,H))
        np.add.at(S,cols,g)
        P=1-np.exp(-S)
        R=(P-D.T)  # W x H
        # dL/dS = 2R*exp(-S)
        G=2*R*np.exp(-S)
        Gi=G[cols]  # N x5 x H
        dgdy=g*(dy[:,None,:])/(s*s)
        grad=(Gi*dgdy).sum((1,2))
        dd=np.diff(y)
        sm=np.zeros(N); sm[:-1]-=dd; sm[1:]+=dd
        grad+=lam*sm
        y=y-lr*np.clip(grad,-50,50)
        y=np.clip(y,0,H)
    return y,(R**2).sum()
for s,it in [(1.0,300),(0.8,600)]:
    y,L=run(y,s,0.9,it,0.1,0.0)
    print(s,L,flush=True)
np.save('/tmp/claude-0/s131/mk/m01/scratch/y.npy',y)
# render
dx=(cx-xi[:,None]);dy=(ry[None,:]-y[:,None]);s=0.8
g=0.9*np.exp(-dx[:,:,None]**2/(2*s*s))*np.exp(-dy[:,None,:]**2/(2*s*s))
S=np.zeros((W,H));np.add.at(S,cols,g);P=1-np.exp(-S)
img=np.concatenate([D,P.T,np.abs(P.T-D)],0)
Image.fromarray((255-img*255).astype(np.uint8)).resize((1200,1080),Image.NEAREST).save('/tmp/claude-0/s131/mk/m01/scratch/cmp.png')
