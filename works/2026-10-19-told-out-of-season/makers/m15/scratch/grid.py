from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m15/work/record.jpg').convert('L')
px=im.load()
rows=[]
for y in range(90):
    s=''
    for x in range(2,298):
        d=max(0,255-px[x,y]-40)  # drop faint JPEG halo
        s+='0123456789abcdef'[min(15,d*16//216)]
    rows.append(s)
open('grid.txt','w').write('\n'.join(rows))
ys=[y for y in range(90) if any(c!='0' for c in rows[y])]
print(min(ys),max(ys))
