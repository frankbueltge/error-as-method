from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m13/work/record.jpg').convert('L')
w,h=im.size;print(w,h)
p=im.load()
chars=' .:-=+*#%@'
for y in range(h):
    print('%2d '%y+''.join(chars[min(9,(255-p[x,y])//26)] for x in range(0,300)))
