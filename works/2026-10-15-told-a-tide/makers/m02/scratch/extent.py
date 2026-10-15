from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m02/work/record.jpg').convert('L'); px=im.load()
W,H=im.size
ink=[sum(max(0,200-px[x,y]) for y in range(H)) for x in range(W)]
print('left',[ (x,ink[x]) for x in range(8)]); print('right',[(x,ink[x]) for x in range(W-8,W)])
rows=[sum(max(0,200-px[x,y]) for x in range(W)) for y in range(H)]
print('rows', [y for y in range(H) if rows[y]>0][:3], [y for y in range(H) if rows[y]>0][-3:])
