from PIL import Image; import numpy as np
a=np.asarray(Image.open('/tmp/claude-0/s131/mk/m14/work/record.jpg').convert('L')).astype(int)
print(a.shape, a.min(), a.max())
for th in (100,150,200):
    m=a<th; print(th, m.sum(), m.any(0).sum())
m=a<160
rows=[]
for x in range(a.shape[1]):
    ys=np.where(m[:,x])[0]
    rows.append(ys.tolist())
for x in range(0,300):
    print(x, rows[x])
