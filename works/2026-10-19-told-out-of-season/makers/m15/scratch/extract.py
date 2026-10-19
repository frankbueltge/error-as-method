from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m15/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
print(W,H)
# per column: darkness-weighted mean y and min/max of dark pixels
cols=[]
for x in range(W):
    ys=[(y,255-px[x,y]) for y in range(H) if px[x,y]<160]
    if ys:
        cols.append((x,min(y for y,_ in ys),max(y for y,_ in ys),sum(y*w for y,w in ys)/sum(w for _,w in ys)))
    else: cols.append((x,None,None,None))
for c in cols: print(c)
# ascii
for y in range(H):
    print(''.join('#' if px[x,y]<100 else ('+' if px[x,y]<180 else ' ') for x in range(W)))
