from PIL import Image
import sys
im=Image.open('/tmp/claude-0/s133/mk/m22/work/record.jpg').convert('L')
px=im.load()
for (cx,cy) in [(123,5),(128,2),(32,8),(74,8),(135,10),(62,9),(37,13)]:
    print(cx,cy)
    for y in range(cy-3,cy+4):
        print(' '.join('%3d'%(255-px[x,y]) if 0<=y<90 else '  .' for x in range(cx-3,cx+4)))
