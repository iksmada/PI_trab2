import sys
import cv2


def show_usage():
    print(sys.argv)
    print('python codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png')


if len(sys.argv) < 5:
    show_usage()
    quit()

img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
file = open(sys.argv[2], 'r')
text = file.read()
bits = int(sys.argv[3])
text = bin(int.from_bytes(text.encode(), 'big')).replace('b', '')

i = 0
for h in range(img.shape[0]):
    for w in range(img.shape[1]):
        for color in range(img.shape[2]):
            if i >= len(text):
                break
            pixel = img[h, w, color]
            operator = 1 << bits
            pixel = pixel & ~operator
            operator = int(text[i]) << bits
            img[h, w, color] = pixel | operator
            i = i + 1

cv2.imshow('Coded Image', img)
cv2.imwrite(sys.argv[4], img)
cv2.waitKey(20000) & 0xFF

