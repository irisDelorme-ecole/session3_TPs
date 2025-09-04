import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def convolution(original,noyau):
    pass

def afficher(img0,img1, img2):
    fig, axes = plt.subplots(ncols=3)
    axes[0].imshow(img0, cmap=plt.get_cmap('gray'))
    axes[0].set_title("Image Originale")
    axes[1].imshow(img1, cmap=plt.get_cmap('gray'))
    axes[1].set_title("Ma convolution")
    axes[2].imshow(img2, cmap=plt.get_cmap('gray'))
    axes[2].set_title("Convolution SciPy")

    plt.show()



# Image 15x15 fond noir (valeur 0)
image_dessin = np.full((15, 15), 0, dtype=np.float32)

# On dessine un carré gris (valeur 128) au centre
image_dessin[3:12, 3:12] = 128

# On peut aussi ajouter une croix blanche (valeur 255) à l'intérieur du carré
image_dessin[7, 5:10] = 255
image_dessin[5:10, 7] = 255

#Noyau utilisé pour la convolution
noyau  = 1/9 * np.ones((3,3))

#Appliquer ka convolution
sortie = convolution(image_dessin,noyau)

#Appliquer ka convolution de Scipy.signal
sortie2 = signal.convolve2d(image_dessin,noyau, mode='same', boundary='fill', fillvalue=255)

#Afficher les trois images
afficher(image_dessin,sortie,sortie2)

