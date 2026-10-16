from PIL import Image; import numpy as np, json
a=255-np.array(Image.open('../work/record.jpg').convert('L')).astype(float)
H,W=a.shape; N=1464
x0,x1=2.4,296.4
ys=np.arange(0,H,0.25)
def col(x):
    i=int(np.floor(x)); f=x-i
    c=a[:,i]*(1-f)+a[:,min(i+1,W-1)]*f
    return np.interp(ys,np.arange(H),c)
xs=x0+np.arange(N)*(x1-x0)/(N-1)
E=np.log(0.03+np.array([np.maximum.reduce([col(min(max(x+d,0),W-1.01)) for d in (-0.5,0,0.5)]) for x in xs])/255.0)
lam=0.003
D=(ys[:,None]-ys[None,:])**2
cost=-E[0]; back=[]
for i in range(1,N):
    t=cost[None,:]+lam*D  # [to,from]
    b=t.argmin(1); back.append(b)
    cost=t[np.arange(len(ys)),b]-E[i]
p=[cost.argmin()]
for b in reversed(back): p.append(b[p[-1]])
p=p[::-1]; y=ys[p]
v=(H-y)
np.save('y.npy',y)
json.dump([round(float(t),2) for t in v],open('vals.json','w'))
# overlay
im=Image.open('../work/record.jpg').convert('RGB').resize((W*4,H*4))
from PIL import ImageDraw
d=ImageDraw.Draw(im)
pts=[(xs[i]*4+2,y[i]*4+2) for i in range(N)]
d.line(pts,fill=(255,0,0),width=1)
im.save('overlay.png')
im.crop((0,0,600,360)).save('ov1.png')
