from PIL import Image
import base64
im=Image.open('/tmp/claude-0/s133/mk/m01/work/record.jpg').convert('L')
raw=bytes(255-p for p in im.getdata())
data=base64.b64encode(raw).decode()
html=open('template.html').read().replace('__DATA__',data)
open('/tmp/claude-0/s133/mk/m01/work/index.html','w').write(html)
print(len(data))
