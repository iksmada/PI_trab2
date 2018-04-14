import sys
import cv2
import numpy as np


def show_usage():
    print('Usage: python3 decodificar.py imagem_saida.png plano_bits texto_saida.txt')


if len(sys.argv) < 3:
    show_usage()
    quit()

img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
bits = int(sys.argv[2])

text_bin = str()
for h in range(img.shape[0]):
    for w in range(img.shape[1]):
        for color in range(img.shape[2]):
            pixel = img[h, w, color]
            operator = 1 << bits
            bit = (pixel & operator != 0) * 1
            text_bin = text_bin + str(bit)

text_bin = text_bin[0] + 'b' + text_bin[1:]

text = int(text_bin, 2)
text = text.to_bytes((text.bit_length() + 7) // 8, 'big').decode()
text = text.replace('\x00', '')
print("Message: " + text)
file = open(sys.argv[3], 'w+')
file.write(text)


cv2.imshow('Coded Image', img)
mask_bit_0 = 1 << 0
cv2.imshow('Bit 0', cv2.bitwise_and(img, np.array([mask_bit_0, mask_bit_0, mask_bit_0])) * 255)

mask_bit_1 = 1 << 1
cv2.imshow('Bit 1', cv2.bitwise_and(img, np.array([mask_bit_1, mask_bit_1, mask_bit_1]))/2 * 255)

mask_bit_2 = 1 << 2
cv2.imshow('Bit 2', cv2.bitwise_and(img, np.array([mask_bit_2, mask_bit_2, mask_bit_2]))/4 * 255)

mask_bit_7 = 1 << 7
cv2.imshow('Bit 7', cv2.bitwise_and(img, np.array([mask_bit_7, mask_bit_7, mask_bit_7])))

cv2.waitKey(-1)
cv2.destroyAllWindows()
