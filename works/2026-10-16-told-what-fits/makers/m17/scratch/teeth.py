from PIL import Image; import numpy as np
a=np.asarray(Image.open('/tmp/claude-0/s131/mk/m17/work/record.jpg').convert('L')).astype(float)
d=a<140
cols=np.where(d.any(0))[0]; print('ink x',cols.min(),cols.max())
top=np.array([np.where(d[:,x])[0].min() if d[:,x].any() else 99 for x in range(300)])
# local maxima of value = local minima of top row
pk=[x for x in range(2,298) if top[x]<=top[x-1] and top[x]<=top[x+1] and top[x]<min(top[x-2],top[x+2])+0]
print(len(pk),pk)
