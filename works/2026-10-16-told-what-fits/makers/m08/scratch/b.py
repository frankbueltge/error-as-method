from PIL import Image; import numpy as np
im=np.array(Image.open('/tmp/claude-0/s131/mk/m08/work/record.jpg').convert('L')).astype(float)
ink=np.clip((200-im)/200,0,1)
H,W=ink.shape
ys=np.arange(H)[:,None]
w=ink.sum(0)
cy=(ink*ys).sum(0)/np.maximum(w,1e-6)
top=np.array([np.argmax(ink[:,x]>0.4) if (ink[:,x]>0.4).any() else -1 for x in range(W)])
bot=np.array([H-1-np.argmax(ink[::-1,x]>0.4) if (ink[:,x]>0.4).any() else -1 for x in range(W)])
print('first/last inked col', np.where(w>0.5)[0][[0,-1]])
v=-cy; v=v-np.convolve(v,np.ones(15)/15,'same')
v=v[10:-10]
best=[]
for P in np.arange(4.5,5.5,0.005):
    t=np.arange(len(v))
    c=np.abs((v*np.exp(2j*np.pi*t/P)).sum())
    best.append((c,P))
best.sort(); print('period px',best[-5:])
print('px per day if 24h:',300/61)
np.save('cy.npy',cy); np.save('top.npy',top); np.save('bot.npy',bot)
for x in range(0,W,1): print(x,round(cy[x],1),top[x],bot[x],round(w[x],1))
