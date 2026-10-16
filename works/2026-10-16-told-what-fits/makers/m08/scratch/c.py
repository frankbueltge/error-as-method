from PIL import Image; import numpy as np
im=np.array(Image.open('/tmp/claude-0/s131/mk/m08/work/record.jpg').convert('L')).astype(float)
ink=np.clip((200-im)/200,0,1); H,W=ink.shape
x0,x1=2.5,297.0
pxh=(x1-x0)/1463
P=4.825
# phase fold of centroid
cy=np.load('cy.npy')
ph=((np.arange(W)-x0)/P)%1
vals=[[] for _ in range(10)]
for x in range(3,297): vals[int(ph[x]*10)].append(cy[x])
print('fold', [round(np.mean(v),1) for v in vals])
# per day: max height (min y), min height
nd=int((x1-x0)/P)
for d in range(nd+1):
    a=int(round(x0+d*P- P*0.0)); b=int(round(x0+(d+1)*P))
    sub=ink[:,a:b]>0.35
    rows=np.where(sub.any(1))[0]
    if len(rows): print(d,a,b,'hi',H-rows.min(),'lo',H-rows.max(),'n',int(sub.sum()))
