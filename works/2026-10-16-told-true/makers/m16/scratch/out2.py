from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m16/work/record.jpg').convert('L'); px=im.load()
seen=set()
for x in range(300):
  ys=[y for y in range(0,42) if px[x,y]<170]
  if ys:
    t=(x-2)*1463/295
    print(x, ys, 'hour %.1f  phase %.1f'%(t, t%24))
