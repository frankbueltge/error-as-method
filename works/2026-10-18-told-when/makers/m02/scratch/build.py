t=open('template.html').read(); d=open('data.txt').read().strip()
open('/tmp/claude-0/s135/mk/m02/work/index.html','w').write(t.replace('__DATA__',d))
