/**
 * Definition of image data structures
 */
#ifndef IMAGE_DATA_H
#define IMAGE_DATA_H

#include <stdint.h>

/**** Image data data structures ****/

/**
 * @brief Enum of possible image encodings.
 */
enum image_encoding {
	VGA,
	VGA_RLE,
};

/**
 * @brief Data structure encapsulating image data.
 * Includes encoding and size metadata in addition to the data.
 */
struct image {
	// The encoding of the image data
	enum image_encoding encoding;
	// The width (in pixels) of the image
	int width;
	// The height (in pixels) of the image
	int height;
	// The length of the data
	int length;
	// Pointer to a global array of data for the image.
	// 320x240=76800 which is more than uint16 can hold in the RLE case
	// but we assume no real image is one color for the entire screen size.
	uint16_t* data;
};

#endif
