"""step.py <k>: copies v<k-1> to v<k> in every lineage and prints each maker's prompt (brief + paths) to briefs/run/<L>-v<k>.txt."""
import sys, os, shutil
k = int(sys.argv[1]); W = os.path.abspath(os.path.dirname(__file__))
os.makedirs(f'{W}/briefs/run', exist_ok=True)
for L in ('P1', 'P2', 'B1', 'B2'):
    src, dst = f'{W}/lineages/{L}/v{k-1}', f'{W}/lineages/{L}/v{k}'
    shutil.copytree(src, dst)
    brief = open(f'{W}/briefs/{"plain" if L[0] == "P" else "balance"}.md').read()
    brief = brief.replace('`data/extent.js`', f'`{W}/data/extent.js`', 1)
    brief += (f'\nThe directory: `{dst}/` (it holds the current version, which you replace).\n'
              f'The screenshot of the current version: `{W}/shots/{L}-v{k-1}.png` (read it as an image).\nk = {k}.\n'
              'Do not run git. When done, reply with one line: done.\n')
    open(f'{W}/briefs/run/{L}-v{k}.txt', 'w').write(brief)
