from PIL import Image; import numpy as np, json
a=np.asarray(Image.open('/tmp/claude-0/s131/mk/m09/work/record.jpg').convert('L')).astype(float)/255
H,W=a.shape; N=1464
x0,x1=2.5,296.5
xs=x0+np.arange(N)*(x1-x0)/(N-1)
# subpixel row profile by linear interp across columns, upsample y x4
Y=np.arange(0,H,0.25)
def col(x):
    i=int(np.floor(x)); f=x-i
    c=a[:,i]*(1-f)+a[:,min(i+1,W-1)]*f
    return np.interp(Y,np.arange(H),c)
D=np.array([col(x) for x in xs])  # brightness, low=dark
cost=D  # 0..1
S=len(Y); lam=0.012
dy=np.abs(Y[:,None]-Y[None,:])
trans=lam*dy**1.0
acc=cost[0].copy(); bp=np.zeros((N,S),int)
for t in range(1,N):
    m=acc[:,None]+trans  # from i to j
    bp[t]=m.argmin(0); acc=m.min(0)+cost[t]
path=np.zeros(N,int); path[-1]=acc.argmin()
for t in range(N-1,0,-1): path[t-1]=bp[t,path[t]]
y=Y[path]
v=(90-y)  # value proxy
json.dump([round(float(q),2) for q in v],open('series.json','w'))
im=Image.new('L',(W*4,H*4),255)
px=im.load()
for t in range(N):
    X=int(xs[t]*4);Yy=int(y[t]*4)
    for dx in range(-2,3):
        for dyy in range(-2,3):
            if 0<=X+dx<W*4 and 0<=Yy+dyy<H*4: px[X+dx,Yy+dyy]=0
im.save('recon.png')
Image.open('/tmp/claude-0/s131/mk/m09/work/record.jpg').resize((W*4,H*4)).save('orig4.png')
print(v.min(),v.max())
