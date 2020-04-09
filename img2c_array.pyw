import sys
import os
from numpy import asarray, rot90, uint8
from cv2 import imread, IMREAD_GRAYSCALE, threshold, THRESH_BINARY
from math import ceil, floor
from re import findall
from datetime import date, datetime


def error(string):
    BASE_PATH = os.path.dirname(os.path.realpath(__file__))
    NAME = format(date.today()) + '_' + format(datetime.now().time())
    NAME = NAME.replace('.', '_')
    NAME = NAME.replace(':', '_')
    NAME += '.txt'
    ERROR_PATH = os.path.join(BASE_PATH, 'errors')
    if not os.path.isdir(ERROR_PATH):
        os.mkdir(ERROR_PATH)
    TARGET_PATH = os.path.join(ERROR_PATH, NAME)
    with open(TARGET_PATH, 'wt') as file:
        file.write(string)
    sys.exit()


if len(sys.argv) > 1:
    BASE_PATH = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isfile(sys.argv[1]):
        error('FILE NOT FOUND')
    try:
        file_name = findall(r'(([A-Za-z0-9_-]+?)\.)', sys.argv[1])[0][-1]
    except IndexError:
        error('INVALID FILE NAME')
    TARGET_PATH = os.path.join(BASE_PATH, file_name + '.h')
    if os.path.isfile(TARGET_PATH):
        os.remove(TARGET_PATH)
    img = imread(sys.argv[1], IMREAD_GRAYSCALE)
    if img is None:
        error('FILE IS NOT AN IMAGE')
    img = 255 - asarray(img)
    img = threshold(img, 60, 255, THRESH_BINARY)[1]
    img = rot90(img, -1)
    SIZE = img.shape
    with open(TARGET_PATH, 'wt') as file:
        file.write('#ifndef _ZIKA_T_IMAGE_\n')
        file.write('#define _ZIKA_T_IMAGE_\n\n')
        file.write('typedef struct {\n\tconst uint16_t width;\n')
        file.write('\tconst uint16_t height;\n\tconst uint8_t *data;\n')
        file.write('}TImage;\n#endif\n\n#ifndef _ZIKA_I_' + file_name.upper())
        file.write('_\n#define _ZIKA_I_' + file_name.upper() + '_\n')
        file.write('TImage ' + file_name + ' = {\n')
        file.write('\t.width=' + str(SIZE[1]) + ',\n')
        file.write('\t.height=' + str(SIZE[0]) + ',\n')
        file.write('\t.data=(const uint8_t [' + str(SIZE[0]) + '*')
        file.write(str(SIZE[1]) + ']) {\n\t\t')
        for i in range(SIZE[0]):
            row = asarray([0] * ceil(SIZE[1]/8), dtype=uint8)
            for j in range(SIZE[1]):
                if img[i, j] != 0:
                    row[floor(j/8)] |= (1 << (7 - j % 8))
            row.tofile(file, ', ', format='0x%02x')
            file.write(',\n\t\t')
        file.write('}\n};\n#endif\n')
