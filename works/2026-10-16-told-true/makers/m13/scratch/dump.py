from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m13/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
print(W,H)
chars=' .:-=+*#%@'
for y in range(H):
    print('%2d '%y+''.join(chars[min(9,(255-px[x,y])//26)] for x in range(0,W)))
