import numpy as np, json
from PIL import Image
im=np.asarray(Image.open('/tmp/claude-0/s131/mk/m04/work/record.jpg').convert('L')).astype(float)
D=(255-im)/255; H,W=D.shape
v=np.load('vals_fit.npy'); xs=2.6+np.arange(1464)*294/1463
d=v.reshape(61,24).copy()
for i in range(61):
  cols=range(int(np.round(xs[24*i])),int(np.round(xs[24*i+23]))+1)
  rows=[r for c in cols for r in np.where(D[:,c]>0.35)[0]]
  imin=H-1-max(rows); top=d[i].max(); fmin=d[i].min()
  if imin<fmin-3 and top-fmin>1:
    d[i]=top-(top-d[i])*(top-imin)/(top-fmin)
vals=np.round(d.ravel()*10).astype(int).tolist()
json.dump(vals,open('vals.json','w'))
print(min(vals),max(vals),len(vals))
