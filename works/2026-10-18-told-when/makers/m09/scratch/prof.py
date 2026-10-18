import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); w,h=im.size; p=im.load()
for y in range(h):
    s=sum(255-p[x,y] for x in range(w))
    print(y, s, '*'*(s//400))
# column extent
xs=[x for x in range(w) if any(p[x,y]<150 for y in range(h))]
print('xmin',min(xs),'xmax',max(xs))
