from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m10/work/record.jpg').convert('L')
W,H=im.size
px=im.load()
print(W,H)
# per column: darkness-weighted rows
cols=[]
for x in range(W):
    ds=[(y,255-px[x,y]) for y in range(H) if px[x,y]<160]
    cols.append(ds)
for x in range(W):
    ys=[y for y,d in cols[x]]
    print(x, ys)
