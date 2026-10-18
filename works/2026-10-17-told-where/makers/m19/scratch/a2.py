from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m19/work/record.jpg').convert('L'); p=im.load()
def show(x0,y0,w=7,h=6):
  for y in range(y0,y0+h): print(' '.join('%3d'%p[x,y] for x in range(x0,x0+w)))
  print()
show(28,9); show(120,3); show(1,80); show(90,80,10); show(288,80,10)
