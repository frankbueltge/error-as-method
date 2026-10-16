from PIL import Image; import numpy as np, sys
d=(255-np.array(Image.open('/tmp/claude-0/s131/mk/m10/work/record.jpg').convert('L')).astype(float))/255
H,W=d.shape; N=1464
x0,x1,A,sig,lam=[float(a) for a in sys.argv[1:6]]
xs=x0+np.arange(N)*(x1-x0)/(N-1)
y=np.load('/tmp/claude-0/s131/mk/m10/scratch/y.npy') if len(sys.argv)<7 else np.load(sys.argv[6])
R=np.arange(H)[:,None]; ys=np.arange(3,88,0.25)
def g(yv,xv,cols):
    return A*np.exp(-((R-yv)**2)/(2*sig*sig))*np.exp(-((cols[None,:]-xv)**2)/(2*sig*sig))
Z=np.zeros((H,W)); allc=np.arange(W)
cw=[]
for t in range(N):
    c=np.arange(max(int(xs[t])-3,0),min(int(xs[t])+5,W)); cw.append(c)
    Z[:,c]+=g(y[t],xs[t],c)
def loss(): return ((d-(1-np.exp(-Z)))**2).sum()
print('start',loss())
for sweep in range(int(sys.argv[7]) if len(sys.argv)>7 else 6):
    order=np.random.permutation(N)
    for t in order:
        c=cw[t]; Z[:,c]-=g(y[t],xs[t],c)
        Zl=Z[:,c]; dl=d[:,c]
        G=A*np.exp(-((R[None,:,:]-ys[:,None,None])**2)/(2*sig*sig))*np.exp(-((c[None,None,:]-xs[t])**2)/(2*sig*sig))
        L=((dl[None]-(1-np.exp(-(Zl[None]+G))))**2).sum((1,2))
        if t>0: L+=lam*np.abs(ys-y[t-1])
        if t<N-1: L+=lam*np.abs(ys-y[t+1])
        y[t]=ys[L.argmin()]; Z[:,c]+=g(y[t],xs[t],c)
    print(sweep,loss())
np.save('/tmp/claude-0/s131/mk/m10/scratch/yfit.npy',y)
M=1-np.exp(-Z)
Image.fromarray(np.concatenate([255-d*255,255-M*255,128+(M-d)*127]).clip(0,255).astype(np.uint8)).resize((1200,1080),Image.NEAREST).save('/tmp/claude-0/s131/mk/m10/scratch/cmp.png')
