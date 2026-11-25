"""Build the static GitHub Pages site from the design-canvas sources.
Usage: python3 build_site.py <project_dir> <blob_dir> <out_dir>"""
import re, shutil, sys, os
proj, blobs, out = sys.argv[1:4]
os.makedirs(out + '/images', exist_ok=True)
pages = [('Main.dc.html', 'index.html'), ('MainEN.dc.html', 'en.html')]
used = set()
for src, dst in pages:
    s = open(os.path.join(proj, src), encoding='utf-8').read()
    ids = set(re.findall(r'/_blob/([0-9a-f]{32})', s))
    for i in ids:
        f = os.path.join(blobs, i)
        if not os.path.exists(f): sys.exit('missing image ' + i)
        shutil.copy(f, f'{out}/images/{i}.webp'); used.add(i)
    s = re.sub(r'/_blob/([0-9a-f]{32})', r'images/\1.webp', s)
    s = s.replace('href="Main.dc.html"', 'href="index.html"').replace('href="MainEN.dc.html"', 'href="en.html"')
    open(os.path.join(out, dst), 'w', encoding='utf-8').write(s)
# drop images no longer referenced
for f in os.listdir(out + '/images'):
    if f[:-5] not in used: os.remove(os.path.join(out, 'images', f))
print('pages', len(pages), 'images', len(used))
