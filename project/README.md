## Prerequisites
* Python 3
* [Pillow](https://pypi.org/project/Pillow)

## CPUlator
For convenience of use on [CPUlator](https://cpulator.01xz.net/?sys=arm-de1soc), a Python script and Makefile are provided that combine all C files under `src/` into one file and expand quote-`#include`s (i.e. `#include "header.h"` and not `#include <stdio.h>`). The resulting file is suitable for use in CPUlator. On Windows, the contents of the file is placed in the clipboard as well.

## Converting image assets to C files
Run `make assets` to convert `assets/*` to `src/assets/*.c` and produce `include/assets.h`.
