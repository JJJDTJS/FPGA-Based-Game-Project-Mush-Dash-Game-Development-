import sys
from typing import Optional, Literal
from pathlib import Path
from itertools import cycle
from PIL import Image

from var_name import var_names

TRANSPARENT = 0x4947 # arbitrary unlikely-used color

def rle(data: list[int]) -> list[int]:
    result: list[int] = []
    count: int = 0
    last_byte: Optional[int] = None
    for byte in data:
        if byte != last_byte:
            if last_byte is not None:
                result += [count, last_byte]
            count = 0
            last_byte = byte
        count += 1
    if last_byte is not None:
        result += [count, last_byte]
    return result

def rgb_to_vga(rgba: tuple[int, int, int, int]) -> int:
    r, g, b, a = rgba
    if a == 0:
        return TRANSPARENT
    r = int(r / 0xff * 0b11111)
    g = int(g / 0xff * 0b111111)
    b = int(b / 0xff * 0b11111)
    return (r << 11) | (g << 5) | b

with Image.open(sys.argv[1]) as im, open(sys.argv[2], 'w') as cfile:
    im = im.convert("RGBA")
    data = list(map(rgb_to_vga, im.getdata()))
    data_rle = rle(data)
    mode: Literal["VGA", "VGA_RLE"]
    print('  RLE', len(data_rle), 'vs raw', len(data))
    if len(data_rle) < len(data):
        mode = "VGA_RLE"
        data = data_rle
    else:
        mode = "VGA"

    # assets/xyz.123!1.png => xyz_123_1(_data)
    filename = Path(sys.argv[1]).name
    var_name, data_var_name = var_names(filename)
    width = im.width
    height = im.height
    length = len(data)

    cfile.write(f"""
/**
 * Data for {filename}
 */
#include "assets.h"

static uint16_t {data_var_name}[] = {{
""".strip())
    # max 9 items per line
    for count, (i, word) in zip(cycle(range(9)), enumerate(data)):
        if count == 0:
            cfile.write('\n\t')
        cfile.write(f'{word:#06x},')
        if count != 8 and i != len(data) - 1:
            cfile.write(' ')
    print('\n};', file=cfile)
    print(f"""
struct image {var_name} = {{ {mode}, {width}, {height}, {length}, {data_var_name} }};
""".rstrip(), file=cfile)
