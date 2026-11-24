import random
from PIL import Image, ImageFilter, ImageEnhance
random.seed(3)
D='../P4/'
for src,dst in (('layout1.jpg','layout2.jpg'),('walt.jpg','walt2.jpg')):
    im=Image.open(D+src).convert('RGB').filter(ImageFilter.GaussianBlur(1.4))
    px=im.load()
    w,h=im.size
    for y in range(h):
        for x in range(w):
            r,g,b=px[x,y]; n=random.randint(-14,14)
            px[x,y]=(min(255,max(0,r+n+18)),min(255,max(0,g+n+8)),min(255,max(0,b+n-10)))
    im=ImageEnhance.Contrast(im).enhance(0.85)
    im.save(D+dst,quality=35)
