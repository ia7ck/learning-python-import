import sys
import pathlib

for p in pathlib.Path(".").iterdir():
    if p.is_dir():
        sys.path.append(str(p.resolve()))

import pkg.aaa

pkg.aaa.hello()
