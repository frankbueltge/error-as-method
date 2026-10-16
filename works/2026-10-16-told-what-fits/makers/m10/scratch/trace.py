from PIL import Image; import numpy as np, json, sys

def gaussian_filter(a,s):
    r=int(3*s)+1; k=np.exp(-np.arange(-r,r+1)**2/(2*s*s)); k/=k.sum()
    a=np.apply_along_axis(lambda v:np.convolve(v,k,'same'),0,a)
    return np.apply_along_axis(lambda v:np.convolve(v,k,'same'),1,a)
def map_coordinates(a,rc,order=1):
    r,c=rc; r0=np.clip(np.floor(r).astype(int),0,a.shape[0]-2); c0=np.clip(np.floor(c).astype(int),0,a.shape[1]-2)
    fr=r-r0; fc=c-c0
    return a[r0,c0]*(1-fr)*(1-fc)+a[r0+1,c0]*fr*(1-fc)+a[r0,c0+1]*(1-fr)*fc+a[r0+1,c0+1]*fr*fc
d=(255-np.array(Image.open('/tmp/claude-0/s131/mk/m10/work/record.jpg').convert('L')).astype(float))/255
N=1464
x0,x1=float(sys.argv[1]) if len(sys.argv)>1 else 2.8, float(sys.argv[2]) if len(sys.argv)>2 else 296.6
lam=float(sys.argv[3]) if len(sys.argv)>3 else 0.08
xs=x0+np.arange(N)*(x1-x0)/(N-1)
ds=gaussian_filter(d,0.7)
ys=np.arange(0,90,0.25); S=len(ys)
E=np.array([map_coordinates(ds,[ys,np.full(S,x)],order=1) for x in xs])  # N x S
E=E/E.max()
cost=-E[0].copy(); back=np.zeros((N,S),int)
dy=np.abs(ys[:,None]-ys[None,:])*lam
for t in range(1,N):
    tot=cost[:,None]+dy   # from i to j
    back[t]=tot.argmin(0); cost=tot.min(0)-E[t]
path=np.zeros(N,int); path[-1]=cost.argmin()
for t in range(N-1,0,-1): path[t-1]=back[t,path[t]]
y=ys[path]
np.save('/tmp/claude-0/s131/mk/m10/scratch/y.npy',y)
# render check
H,W=90,300; R=np.zeros((H*4,W*4))
for xx,yy in zip(xs,y):
    cx,cy=int(round(xx*4)),int(round(yy*4))
    R[max(cy-3,0):cy+4,max(cx-3,0):cx+4]=1
Image.fromarray(((1-R)*255).astype(np.uint8)).save('/tmp/claude-0/s131/mk/m10/scratch/render.png')
Image.open('/tmp/claude-0/s131/mk/m10/work/record.jpg').resize((1200,360),Image.NEAREST).save('/tmp/claude-0/s131/mk/m10/scratch/orig4.png')
# coverage: fraction of dark pixels within 1px of a dot
dark=np.argwhere(d>0.45)
pts=np.stack([y,xs],1)
dist=np.sqrt(((dark[:,None,:]-pts[None,:,:])**2).sum(-1)).min(1)
print('dark px',len(dark),'covered<1.2',np.mean(dist<1.2),'mean emission',E[np.arange(N),path].mean())
