import sys
d=open(sys.argv[1],'rb').read()
# parse P5
parts=d.split(b'\n',3)
w,h=map(int,parts[1].split()); px=parts[3]
rows=[px[y*w:(y+1)*w] for y in range(h)]
chars=" .:-=+*#%@"
for y in range(h):
    print(''.join(chars[min(9,(255-rows[y][x])//26)] for x in range(0,w)))
