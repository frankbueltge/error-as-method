from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m07/work/record.jpg').convert('L')
w,h=im.size;p=im.load()
D=[[ (255-p[x,y])/255 for y in range(h)] for x in range(w)]
# total ink per column
tot=[sum(c) for c in D]
floor=[D[x][83]+D[x][84] for x in range(w)]
print('total ink', sum(tot))
print('ink rows 82-85', sum(sum(D[x][y] for y in range(82,86)) for x in range(w)))
# floor per x
print(''.join('#' if f>1.2 else ('+' if f>0.6 else ('.' if f>0.2 else ' ')) for f in floor))
# per-day top
pd=w/61
for d in range(61):
  xs=range(int(d*pd),int((d+1)*pd))
  top=min((y for x in xs for y in range(h) if D[x][y]>0.35),default=None)
  ink=sum(D[x][y] for x in xs for y in range(80))
  # mean y weighted above floor
  m=sum(D[x][y]*y for x in xs for y in range(80))/max(ink,1e-9)
  print(d,top,round(ink,1),round(m,1))
