from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m13/work/record.jpg').convert('L')
p=im.load()
def d(x,y): return max(0,255-p[x,y]-8)
above=sum(d(x,y) for x in range(300) for y in range(0,81))
fl=sum(d(x,y) for x in range(300) for y in range(81,90))
print('above',above,'floor',fl)
# isolated dot near (123,5)
print([[255-p[x,y] for x in range(120,127)] for y in range(2,9)])
s=sum(d(x,y) for x in range(119,128) for y in range(1,9));print('dot mass',s)
for (x0,y0) in [(53,13),(66,14),(37,26)]:
    print([[255-p[x,y] for x in range(x0-3,x0+4)] for y in range(y0-3,y0+4)])
