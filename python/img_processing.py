import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

img_path = 'img/src/dog.jpg'
img = Image.open(img_path).convert('L')
img = np.array(img)

plt.imshow(img)
plt.savefig('img/output/grayscale_img.png')
print(img)


def apply_kernel(kernel, image, starting_point):
    # el starting point es el punto superior izquierdo desde el que arranco a aplicar el kernel
    # el applied_kernel ahora es un escalar pero podría ser una matriz...
    applied_kernel = 0
    for i in range(0, kernel.shape[0]):
        for j in range(0, kernel.shape[1]):
            applied_kernel += kernel[i][j] * image[starting_point[0] + i][starting_point[1] + j]
    return applied_kernel

kernel = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]])

stride = 3

filtered_img = np.zeros((int(img.shape[0] / stride), int(img.shape[1] / stride)))

tol = 70
for i in range(0, img.shape[0], stride):
    for j in range(0, img.shape[1], stride):
        applied_kernel = apply_kernel(kernel, img, [i, j])
        filtered_img[int(i / stride)][int(j / stride)] = 1 if applied_kernel > tol else 0

plt.imshow(filtered_img)
plt.savefig('img/output/filtered_img.png')
print(filtered_img)
print(np.max(filtered_img))
