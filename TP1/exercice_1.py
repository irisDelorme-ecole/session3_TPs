from skimage import data
from PIL import Image

import skimage as sk
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def convolution_blur(image):  # flouttage de l'image
    return signal.convolve2d(image, 1 / 9 * np.ones((3, 3)))


def gradient_x(image):  # retourne image filtree avec sobel horizontalement
    # noyau sobel horizontal
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    return signal.convolve2d(convolution_blur(image), sobel_x)


def gradient_y(image):  # retourne image filtree avec sobel verticalement
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    return signal.convolve2d(convolution_blur(image), sobel_y)


def gradient_both(image):  # retourne l'amplitude des deux gradients avec les filtres de sobel
    blured = convolution_blur(image)
    return np.sqrt(gradient_x(blured) ** 2 + gradient_y(blured) ** 2)


def contours(image):  # ontours avec amplitude du gradient de sobel bidirectionnel, avec seuillage 75(permet la meilleure resolution avec camera et avec hello kitty. details perdus de camera quand plus bas, moins de clarte dans hello kitty quand plus haut)
    return gradient_both(convolution_blur(image)) > 75


def construire(image):  # traite la reponse de l'utilisateur et l'envoie a l'affichage

    affichage_final(image, convolution_blur(image), gradient_x(image), gradient_y(image), gradient_both(image),
                    contours(image))


def affichage_final(im_base, im_blur, im_gradx, im_grady, im_ampl_grad, im_contours):  # cree l'affichage
    fig, axes = plt.subplots(ncols=3, nrows=2)
    plt.setp(axes, xticks=[], yticks=[])
    axes[0][0].imshow(im_base, cmap='gray')
    axes[0][0].set_title("Image de Base", fontsize=8)
    axes[0][1].imshow(im_blur, cmap='gray')
    axes[0][1].set_title("Image Floutée", fontsize=8)
    axes[0][2].imshow(im_gradx, cmap='gray')
    axes[0][2].set_title("Gradient avec sobel horizontal", fontsize=8)
    axes[1][0].imshow(im_grady, cmap='gray')
    axes[1][0].set_title("Gradient avec sobel vertical", fontsize=8)
    axes[1][1].imshow(im_ampl_grad, cmap='gray')
    axes[1][1].set_title("Amplitude gradient avec sobel", fontsize=8)
    axes[1][2].imshow(im_contours, cmap='gray')
    axes[1][2].set_title("Contours", fontsize=8)

    plt.show()


def ask_image():  # demande quelle image est souhaitee, puis appelle un "constructeur"(pas vraiment, mais meme fonction)
    if input("image 1 (homme avec camera) ou 2 (hello kitty, aussi le default)") == '1':
        construire(data.camera())
    else:
        construire(Image.open('hello_kitty.jpg').convert('L'))


ask_image()
