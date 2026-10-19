from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m13/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
for x in range(W):
    d=[y for y in range(H) if p[x,y]<150]
    if d: print(x, round(x*1464/300/24,2), min(d), max(d), len(d))
    else: print(x,'-')
