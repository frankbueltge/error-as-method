from PIL import Image; import numpy as np
a=np.asarray(Image.open('/tmp/claude-0/s131/mk/m09/work/record.jpg').convert('L')).astype(float)
print(a.shape, a.min(), a.max())
d=a<128
rows=[]
for x in range(a.shape[1]):
    ys=np.where(d[:,x])[0]
    rows.append(ys)
for x in range(0,300):
    ys=rows[x]
    s=''.join('#' if d[y,x] else '.' for y in range(90))
    print(f"{x:3d} {s}")
