import sys
from pathlib import Path

from var_name import var_names

def str_to_c_str(text: str) -> str:
    return '"%s"' % text.encode('unicode-escape') \
        .decode('ascii').replace('"', r'\"')

with open(sys.argv[1]) as txt, open(sys.argv[2], 'w') as cfile:
    filename = Path(sys.argv[1]).name
    var_name, data_var_name = var_names(filename)

    print(f"""
/**
 * Data for {filename}
 */
#include "assets.h"

char {data_var_name}[] =
""".strip(), file=cfile)
    # strip trailing whitespace as it won't be rendered
    text = txt.read().rstrip().splitlines(keepends=True)
    for lineno, line in enumerate(text, start=1):
        if len(line.rstrip('\n')) > 80: # VGA has 80 columns of text
            print(f'  Warning: line too long at {filename}:{lineno}:81')
        print('\t' + str_to_c_str(line), file=cfile)
    print(';', file=cfile)
