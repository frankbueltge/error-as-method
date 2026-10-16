import numpy as np
from PIL import Image, ImageDraw
im=np.asarray(Image.open('/tmp/claude-0/s131/mk/m04/work/record.jpg').convert('L')).astype(float)
D=np.clip((255-im)/255,0,1); H,W=D.shape
N=1464; x0,x1=2.6,296.6
xs=x0+np.arange(N)*(x1-x0)/(N-1)
y=(H-1-np.load('vals.npy')).copy()
ox=np.arange(-3,4); oy=np.arange(-5,6)
cx=np.round(xs).astype(int)
PX=cx[:,None,None]+ox[None,None,:]          # N,1,7
dxv=(PX-xs[:,None,None])
valid_x=(PX>=0)&(PX<W)
a=0.9
def step(y,sx,sy,mu):
    cy=np.round(y).astype(int)
    PY=cy[:,None,None]+oy[None,:,None]       # N,11,1
    dyv=PY-y[:,None,None]
    g=np.exp(-dxv**2/(2*sx*sx)-dyv**2/(2*sy*sy))
    PYb=np.broadcast_to(PY,g.shape); PXb=np.broadcast_to(PX,g.shape)
    ok=valid_x&(PYb>=0)&(PYb<H)
    ag=np.clip(a*g,0,0.999)
    logq=np.where(ok,np.log1p(-ag),0)
    LP=np.zeros((H,W)); np.add.at(LP,(PYb[ok],PXb[ok]),logq[ok])
    R=1-np.exp(LP); res=R-D
    loss=(res**2).sum()
    P=np.exp(LP)
    Pp=np.where(ok,P[np.clip(PYb,0,H-1),np.clip(PXb,0,W-1)],0)
    rr=np.where(ok,res[np.clip(PYb,0,H-1),np.clip(PXb,0,W-1)],0)
    dR_dy=Pp/(1-ag)*a*g*(dyv/(sy*sy))
    grad=(2*rr*dR_dy).sum((1,2))
    dif=np.diff(y); gs=np.zeros(N); gs[:-1]-=2*mu*dif; gs[1:]+=2*mu*dif
    return loss+mu*(dif**2).sum(), grad+gs, R
m=np.zeros(N); v=np.zeros(N); lr=0.3
it=0
for sx,sy,steps in [(1.2,2.5,300),(0.9,1.6,300),(0.7,1.0,400)]:
    for k in range(steps):
        it+=1
        L,g,R=step(y,sx,sy,0.002)
        m=.9*m+.1*g; v=.999*v+.001*g*g
        y-=lr*(m/(1-.9**it))/(np.sqrt(v/(1-.999**it))+1e-8)
        y=np.clip(y,0,H-1)
    print(sx,sy,L)
np.save('vals_fit.npy',H-1-y)
dark=np.argwhere(D>0.3); c=0
for yy,xx in dark:
    ts=np.where(np.abs(xs-xx)<1.0)[0]
    if np.min(np.abs(y[ts]-yy))<=2.0: c+=1
print('coverage',c/len(dark))
big=Image.open('/tmp/claude-0/s131/mk/m04/work/record.jpg').convert('RGB').resize((W*4,H*4),Image.NEAREST)
dr=ImageDraw.Draw(big)
dr.line([(xs[t]*4+2,y[t]*4+2) for t in range(N)],fill=(255,0,0),width=1)
big.crop((0,0,600,360)).resize((1200,720),Image.NEAREST).save('overlay2.png')
Image.fromarray((255*(1-R)).astype(np.uint8)).resize((W*3,H*3)).save('render.png')
