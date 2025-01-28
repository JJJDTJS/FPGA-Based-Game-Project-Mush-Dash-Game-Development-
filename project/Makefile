#############
# Utilities #
#############

#Recursive version of wildcard (i.e. it checks all subdirectories)
# For example:
# 	$(call rwildcard, /tmp/, *.c *.h)
# will return all files ending in .c or .h in /tmp and any of tmp's sub-directories
#NOTE: the directory (e.g. /tmp/) should end with a slash (i.e. /)
rwildcard=$(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2) $(filter $(subst *,%,$2),$d))

#Recursively find directories containing specifc files (useful for finding header include directories)
# For example:
# 	$(call rfiledirs, /tmp/, *.h *.hpp)
# will return all directories in /tmp which contain .h or .hpp files
#NOTE: the directory (e.g. /tmp/) should end with a slash (i.e. /)
rfiledirs=$(sort $(dir $(call rwildcard, $1, $2)))

BUILD = build
SRC_DIR = src
ASSET_DIR = assets

SRC_FILES=$(call rwildcard, $(SRC_DIR), *.c)
IMG_FILES=$(call rwildcard, $(ASSET_DIR), *.png *.jpg *.bmp)
TXT_FILES=$(call rwildcard, $(ASSET_DIR), *.txt)
ASSET_C_FILES=$(patsubst assets/%, src/assets/%.c, $(IMG_FILES) $(TXT_FILES))

combined.c: $(SRC_FILES)
	echo '#define CPULATOR' > combined.c
	python3 scripts/combine.py $^

assets: $(ASSET_C_FILES)
	python3 scripts/assets_combine.py

src/assets/%.txt.c: assets/%.txt
	python3 scripts/txt_convert.py $< $@

src/assets/%.c: assets/%
	python3 scripts/img_convert.py $< $@
