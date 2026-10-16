from PIL import Image; import numpy as np, json
im=np.array(Image.open('/tmp/claude-0/s131/mk/m05/work/record.jpg').convert('L')).astype(float)
H,W=im.shape
ink=(255-im)/255.0
# x extent
cols=np.where((im<128).any(0))[0]; x0,x1=cols[0],cols[-1]
N=1464
xs=x0+np.arange(N)*(x1-x0)/(N-1)
ys=np.arange(H)
def emis(x):
    i=int(np.floor(x)); f=x-i
    a=ink[:,i]; b=ink[:,min(i+1,W-1)]
    return (1-f)*a+f*b
E=np.array([emis(x) for x in xs])  # N x H
cost_e=-np.log(E+0.02)
dy=ys[:,None]-ys[None,:]
lam=0.08
T=lam*np.abs(dy)  # linear penalty
D=cost_e[0].copy(); back=np.zeros((N,H),int)
for t in range(1,N):
    M=D[:,None]+T   # prev x cur
    back[t]=M.argmin(0); D=M.min(0)+cost_e[t]
path=np.zeros(N,int); path[-1]=D.argmin()
for t in range(N-1,0,-1): path[t-1]=back[t,path[t]]
# subpixel refine by local centroid
yr=[]
for t,p in enumerate(path):
    lo,hi=max(p-1,0),min(p+2,H); w=E[t,lo:hi]; yr.append(float((w*ys[lo:hi]).sum()/w.sum()))
yr=np.array(yr)
val=(H-1-yr)
json.dump([round(v,2) for v in val],open('series.json','w'))
# render comparison
out=np.full((H*5,W*5),255,np.uint8)
for x,y in zip(xs,yr):
    X=int(x*5);Y=int(y*5); out[max(Y-1,0):Y+2,max(X-1,0):X+2]=0
big=np.array(Image.fromarray(im.astype(np.uint8)).resize((W*5,H*5),Image.NEAREST))
Image.fromarray(np.vstack([big,out])).save('compare.png')
# coverage: fraction of ink pixels near a path point
print('done', val.min(), val.max())
