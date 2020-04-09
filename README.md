# Image to C array converter

Takes input image as an argument and creates .h C header file with image structure defined as followed:
```
typedef struct {
	const uint16_t width;
	const uint16_t height;
	const uint8_t *data;
}TImage;
```
with every generated image an instance of this structure is created named `_ZIKA_I_<image-name>_`.

Input image is converted to grayscale, rotated by -90 degrees and converted to indexed 2 format -> output image is binary and approximately 8 times smaller if input is greyscale or 24 times smaller if input is in RGB format.

### Error handeling
On error an error file is created at `./errors` describing its cause.

Possible errors are at the moment:
- File not found
- Invalid file name
- File not recognized as an image
