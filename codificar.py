import sys
import cv2
import numpy as np


def show_usage():
    print('Usage: python3 codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png')


if len(sys.argv) < 5:
    show_usage()
    quit()

img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
file = open(sys.argv[2], 'r')
text = file.read()
bits = int(sys.argv[3])
# '00000011' character "End of Text"
text = bin(int.from_bytes(text.encode(), 'big')).replace('b', '') + '00000011'

coded_img = img.copy()
i = 0
for h in range(img.shape[0]):
    for w in range(img.shape[1]):
        for color in range(img.shape[2]):
            if i < len(text):
                pixel = img[h, w, color]
                operator = 1 << bits
                pixel = pixel & ~operator
                operator = int(text[i]) << bits
                pixel = pixel | operator
                i = i + 1
                coded_img[h, w, color] = pixel


cv2.imshow('Original Image', img)
mask_bit_0 = 1 << 0
cv2.imshow('Bit 0', cv2.bitwise_and(coded_img, np.array([mask_bit_0, mask_bit_0, mask_bit_0])) * 255)

mask_bit_1 = 1 << 1
cv2.imshow('Bit 1', cv2.bitwise_and(coded_img, np.array([mask_bit_1, mask_bit_1, mask_bit_1]))/2 * 255)

mask_bit_2 = 1 << 2
cv2.imshow('Bit 2', cv2.bitwise_and(coded_img, np.array([mask_bit_2, mask_bit_2, mask_bit_2]))/4 * 255)

mask_bit_7 = 1 << 7
cv2.imshow('Bit 7', cv2.bitwise_and(coded_img, np.array([mask_bit_7, mask_bit_7, mask_bit_7])))

cv2.imshow('Coded Image', coded_img)
cv2.imwrite(sys.argv[4], coded_img)
cv2.waitKey(-1)
cv2.destroyAllWindows()



