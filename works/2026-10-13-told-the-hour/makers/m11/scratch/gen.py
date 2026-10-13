from PIL import Image
im=Image.open('/tmp/claude-0/s123/mk/m11/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
# keep every pixel darker than near-white, as darkness 0-255, rows 0..89
pts=[]
for x in range(W):
    for y in range(H):
        v=px[x,y]
        if v<215: pts.append(f"{x},{y},{255-v}")
data=";".join(pts)
print(len(pts))
tpl=open('template.html').read()
open('/tmp/claude-0/s123/mk/m11/work/index.html','w').write(tpl.replace('__DATA__',data))
