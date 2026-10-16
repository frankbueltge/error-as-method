d=open('/tmp/claude-0/s130/mk/m04/scratch/cols.txt').read()
t=open('/tmp/claude-0/s130/mk/m04/scratch/template.html').read().replace('__DATA__',d)
open('/tmp/claude-0/s130/mk/m04/work/index.html','w').write(t)
