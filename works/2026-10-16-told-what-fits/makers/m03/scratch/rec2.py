from PIL import Image, ImageDraw; import numpy as np, json
a=255-np.array(Image.open('../work/record.jpg').convert('L')).astype(float)
H,W=a.shape; N=1464
x0,x1=2.4,296.4
dx=(x1-x0)/(N-1)
xs=x0+np.arange(N)*dx
ys=np.arange(0,H,0.25)
yy_,xx_=np.where(a>110)
cen=np.stack([yy_,xx_+0.0],1)
def col(x):
    i=int(np.floor(x)); f=x-i
    c=a[:,i]*(1-f)+a[:,min(i+1,W-1)]*f
    return np.interp(ys,np.arange(H),c)
E=np.log(0.03+np.array([np.maximum.reduce([col(min(max(x+d,0),W-1.01)) for d in (-0.6,0,0.6)]) for x in xs])/255.0)
# anchors: per 24-sample window (sliding with several phases), bottom-most component centroid
bonus=np.zeros_like(E)
for ph in range(0,24,6):
  for s in range(-ph,N,24):
    lo=xs[max(s,0)]-0.5; hi=xs[min(s+24,N-1)]+0.5
    m=(cen[:,1]>=lo)&(cen[:,1]<=hi)
    if not m.any(): continue
    c=cen[m]; 
    for yy,xx in (c[c[:,0].argmax()],c[c[:,0].argmin()]):
      k=np.argsort(np.abs(xs-xx))[:3]
      for kk in k: bonus[kk]=np.maximum(bonus[kk],8*np.exp(-((ys-yy)**2)/2))
E=E+bonus
lam=0.008
D=(ys[:,None]-ys[None,:])**2
cost=-E[0]; back=[]
for i in range(1,N):
    t=cost[None,:]+lam*D
    b=t.argmin(1); back.append(b)
    cost=t[np.arange(len(ys)),b]-E[i]
p=[cost.argmin()]
for b in reversed(back): p.append(b[p[-1]])
y=ys[p[::-1]]
np.save('y.npy',y)
json.dump([round(float(H-t),2) for t in y],open('vals.json','w'))
im=Image.open('../work/record.jpg').convert('RGB').resize((W*4,H*4))
d=ImageDraw.Draw(im)
d.line([(xs[i]*4+2,y[i]*4+2) for i in range(N)],fill=(255,0,0),width=1)
im.save('overlay.png'); im.crop((0,0,600,360)).save('ov1.png'); im.crop((560,0,1200,360)).save('ov2.png')
