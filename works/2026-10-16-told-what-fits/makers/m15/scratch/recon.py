from PIL import Image; import numpy as np, json
a=np.asarray(Image.open('/tmp/claude-0/s131/mk/m15/work/record.jpg').convert('L')).astype(float)
d=np.clip((200-a)/200,0,1)  # darkness
N=1464; x0,x1=2.3,296.4
xs=x0+np.arange(N)*(x1-x0)/(N-1)
H=90
# emission: darkness at column(s) near xs, interpolated
E=np.zeros((N,H))
for i,x in enumerate(xs):
    c=int(np.floor(x)); f=x-c
    col=(1-f)*d[:,c]+f*d[:,min(c+1,299)]
    E[i]=col
lam=0.004
cost=-E[0].copy(); back=np.zeros((N,H),int)
ys=np.arange(H)
P=lam*(ys[:,None]-ys[None,:])**2
for i in range(1,N):
    tot=cost[None,:]+P  # [new,old]
    back[i]=tot.argmin(1)
    cost=tot.min(1)-E[i]
path=np.zeros(N,int); path[-1]=cost.argmin()
for i in range(N-1,0,-1): path[i-1]=back[i,path[i]]
v=(90-path).astype(int)
json.dump(v.tolist(),open('vals.json','w'))
# coverage check
cov=E[np.arange(N),path]
print('mean emission',cov.mean(), (cov<0.2).sum())
# re-render
img=np.full((90,300),255,np.uint8)
for x,y in zip(xs,path): img[y,int(round(x))]=0
Image.fromarray(img).resize((900,270),Image.NEAREST).save('rerender.png')
Image.open('/tmp/claude-0/s131/mk/m15/work/record.jpg').resize((900,270),Image.NEAREST).save('orig.png')
D=v.reshape(61,24)
np.set_printoptions(linewidth=200)
print(D[:8]); print(D[-4:])
print('daily mean',D.mean(1).round(1))
print('hour mean',D.mean(0).round(1))
