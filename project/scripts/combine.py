import sys
import os
import re
from pathlib import Path

INCLUDE_RE = re.compile(r'^#include "([^"]+)"', re.M)
INCLUDE_DIR = Path('include')
SRC_DIR = Path('src')

def read_file(match: re.Match[str]) -> str:
    """Read a header file identified by the match."""
    h_filename = match.group(1)
    print(f'{Path(filename).name}: Expanding {h_filename}')
    with open(INCLUDE_DIR / h_filename) as h_file:
        return h_file.read()

with open("combined.c", "a") as combined_file:
    for filename in sys.argv[1:]:
        with open(filename, "r") as c_file:
            contents = c_file.read()
        # keep expanding local includes (since some headers may include others)
        while re.search(INCLUDE_RE, contents):
            contents = INCLUDE_RE.sub(read_file, contents)
        # write expanded contents after a file header
        print(f'/******** {Path(filename).name} ********/\n', file=combined_file)
        combined_file.write(contents)
        print(file=combined_file)

# copy file contents to clipboard on Windows
if sys.platform.startswith('win'):
    os.system('type combined.c | clip')
