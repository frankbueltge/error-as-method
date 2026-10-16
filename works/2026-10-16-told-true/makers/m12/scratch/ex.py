from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m12/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
print(W,H)
rows=[]
for x in range(W):
    d=[(y,255-px[x,y]) for y in range(H) if px[x,y]<160]
    rows.append(d)
for x in range(0,300,1):
    print(x, ''.join('#' if px[x,y]<100 else ('+' if px[x,y]<180 else '.') for y in range(H)))
