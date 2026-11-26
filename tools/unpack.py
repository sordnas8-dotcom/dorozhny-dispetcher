from pathlib import Path
from zipfile import ZipFile
import json
from io import BytesIO
root=Path('.').resolve()
archives=list(sorted(root.glob('site-part-*.zip')))
for first in sorted(root.glob('site-part-*.zip.001')):
 chunks=sorted(root.glob(first.name[:-3]+'[0-9][0-9][0-9]'))
 archives.append(BytesIO(b''.join(p.read_bytes() for p in chunks)))
for group in [archives,sorted((root/'updates').glob('update_*.zip'))]:
 for archive in group:
  with ZipFile(archive) as z:
   for item in z.infolist():
    target=(root/item.filename).resolve()
    if not target.is_relative_to(root/'docs') or item.file_size>100*1024*1024:
     raise ValueError(f'Unexpected archive entry: {item.filename}')
   z.extractall(root)
assert (root/'docs/index.html').exists()
for row in json.loads((root/'docs/data/schemes.json').read_text()):
 p=(root/'docs'/row['pdf']).resolve()
 assert p.is_relative_to(root/'docs') and p.is_file(),row['filename']
print('Pages ready; all indexed PDF files exist.')
