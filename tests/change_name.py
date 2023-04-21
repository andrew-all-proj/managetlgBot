import os
from os import walk
path = 'D:\kotiki\short_video\kot_na_potom'



filenames = next(walk(path), (None, None, []))[2]
ch = 413
for file in filenames:
    root, ext = os.path.splitext(file[-6:])
    ext = ext.lower()
    ch += 1
    print(ch)
    print(ext)
    print(f'{path}\{ch}{ext}')
    os.rename(f'{path}\{file}', f'{path}\{ch}{ext}')
