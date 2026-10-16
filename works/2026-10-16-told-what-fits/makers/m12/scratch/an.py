from PIL import Image; import numpy as np
im=np.array(Image.open('/tmp/claude-0/s131/mk/m12/work/record.jpg').convert('L')).astype(float)
D=np.clip((235-im)/200,0,1)  # darkness
D[D<0.12]=0
cols=np.where(D.sum(0)>0)[0]; rows=np.where(D.sum(1)>0)[0]
print('x',cols.min(),cols.max(),'y',rows.min(),rows.max())
y=np.arange(90)
cent=(D*y[:,None]).sum(0)/np.maximum(D.sum(0),1e-9)
top=np.array([np.argmax(D[:,c]>0.3) if (D[:,c]>0.3).any() else np.nan for c in range(300)])
x0,x1=cols.min(),cols.max()
s=top[x0:x1+1]; s=np.nan_to_num(s-np.nanmean(s))
s=s-np.convolve(s,np.ones(15)/15,'same')
F=np.abs(np.fft.rfft(s,4096)); fr=np.fft.rfftfreq(4096)
k=np.argmax(F[50:])+50; print('period px',1/fr[k],'days',(x1-x0+1)*fr[k])
# phase via template
P=(x1-x0+1)/61
best=None
for ph in np.linspace(0,P,50,endpoint=False):
  ph_s=[]
  t=np.arange(len(s)); w=np.cos(2*np.pi*(t-ph)/P)
  v=(w*s).sum()
  if best is None or v<best[0]: best=(v,ph)
print('P',P,'phase (top min at)',best)
np.save('D.npy',D)
