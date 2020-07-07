from PIL import Image
from skimage.color import rgb2hsv
import matplotlib.pyplot as plt
import cv2
import numpy as np

def get_hsv(image):
    hsv_img = rgb2hsv(image)
    hue_img = hsv_img[:, :, 0]
    value_img = hsv_img[:, :, 2]

    fig, (ax0, ax1, ax2) = plt.subplots(ncols=3, figsize=(8, 2))

    ax0.imshow(image)
    ax0.set_title("RGB image")
    ax0.axis('off')
    ax1.imshow(hue_img, cmap='hsv')
    ax1.set_title("Hue channel")
    ax1.axis('off')
    ax2.imshow(value_img)
    ax2.set_title("Value channel")
    ax2.axis('off')

    fig.tight_layout()
    plt.show()

def return_intersection(hist_1, hist_2):
    minima = np.minimum(hist_1, hist_2)
    intersection = np.true_divide(np.sum(minima), np.sum(hist_2))

    return intersection

def get_histogram(image_name):
    # load an image in grayscale mode
    img = cv2.imread(image_name,0)

    # calculate frequency of pixels in range 0-255 --> opencv version
    histg = cv2.calcHist([img],[0],None,[256],[0,256])

    #numpy version
    histg, _ = np.histogram(img)#, bins=100, range=[-15, 15])

    return histg

def display_intersection(hist1, hist2):
    plt.hist(hist1, bins='auto', alpha=0.5, label='x')
    plt.hist(hist2, bins='auto', alpha=0.5, label='y')
    plt.legend(loc='upper right')
    plt.show()

name = "./test_cropped_cars/0_0.7593065.png"
hist1 = get_histogram(name)

# name = "./test_cropped_cars/0_0.7637045.png"
name = "./test_cropped_cars/1_0.5236358.png"
hist2 = get_histogram(name)

#get intersection and display
intersection = return_intersection(hist1, hist2)
print(intersection)

display_intersection(hist1, hist2)
