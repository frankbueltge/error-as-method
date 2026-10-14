import json, base64
y=json.load(open('y_fit.json'))
vals=[round(90-v,1) for v in y]           # up = larger, in source-pixel units
img=base64.b64encode(open('/tmp/claude-0/s124/mk/m08/work/record.jpg','rb').read()).decode()
html=open('template.html').read().replace('__DATA__',json.dumps(vals,separators=(',',':'))).replace('__IMG__',img)
open('/tmp/claude-0/s124/mk/m08/work/index.html','w').write(html)
print(len(html))
