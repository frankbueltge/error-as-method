vals=[float(l) for l in open('values.txt')]
data=','.join(str(int(round(v*10))) for v in vals)
html=open('template.html').read().replace('__DATA__',data)
open('/tmp/claude-0/s137/mk/m11/work/index.html','w').write(html)
print(len(html))
