from PIL import Image; import numpy as np
im=np.array(Image.open('/tmp/claude-0/s131/mk/m07/work/record.jpg').convert('L')).astype(float)
d=im<140
cols=[np.where(d[:,x])[0] for x in range(300)]
occ=[x for x in range(300) if len(cols[x])]
print('x range',occ[0],occ[-1], 'y range', np.where(d.any(1))[0][[0,-1]])
top=np.array([c.min() if len(c) else np.nan for c in cols]); bot=np.array([c.max() if len(c) else np.nan for c in cols])
cnt=np.array([len(c) for c in cols])
# darkness sum per column
dark=(255-im).sum(0)
s=dark-dark.mean()
ac=[np.dot(s[:-k],s[k:])/len(s[k:]) for k in range(1,40)]
for k,a in enumerate(ac,1): print(k,round(a/ac[0],2),end=' | ')
print()
# fine period search via fourier
xs=np.arange(300)
for P in np.arange(4.6,5.3,0.02):
  ph=np.exp(2j*np.pi*xs/P); print(round(P,2),round(abs((s*ph).sum())),end='; ')
print()
print('top',list(top.astype(int)[2:300]))
print('cnt',list(cnt))
