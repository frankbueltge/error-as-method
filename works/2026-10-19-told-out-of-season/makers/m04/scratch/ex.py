from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m04/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
cols=[]
for x in range(W):
    d=[(y,255-p[x,y]) for y in range(H) if p[x,y]<200]
    cols.append(d)
# print ascii
for y in range(H):
    print(''.join('#' if p[x,y]<100 else ('+' if p[x,y]<180 else ' ') for x in range(W)))
