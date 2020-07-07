import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import NullFormatter
from sklearn import manifold, datasets
from time import time
from skimage.color import rgb2hsv

import cv2 as cv

import os
from PIL import Image

from sklearn.cluster import KMeans
from sklearn.datasets.samples_generator import make_blobs

def resize(path):
    print("Resizing...")
    dirs = os.listdir(path)
    # print(dirs)
    for item in dirs:
        print(path+item)
        if os.path.isfile(path + item):
            # print("HERE")
            print(path+item)
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            f = f[:28] + "resized_cars/" + f[28:]
            # print(f)
            imResize = im.resize((200,200), Image.ANTIALIAS)
            # print(f + '_resized.jpg', 'JPEG')
            imResize.save(f + '_resized.jpg', 'JPEG', quality=90)

def preprocess(image):
    new_img = rgb2hsv(image)

    new_img = cv.GaussianBlur(new_img, (5,5), 0)

    return new_img

# return the images and labels as arrays
def get_data(directory_in_str, do_preprocess=True):
    directory = os.fsencode(directory_in_str)
    labels = []
    images = []


    for file in os.listdir(os.fsdecode(directory)):
        try:
            filename = os.fsdecode(file)
            index = filename.find('_')

            #get the class and image
            color = filename[:index]
            if(color == 'white'):
                color = 6
            elif(color == 'red'):
                color = 8
            elif(color == 'green'):
                color = 5
            elif(color == 'black'):
                color = 0
            else:
                color = 4

            im = Image.open(directory_in_str + str(filename))

            if(do_preprocess):
                im = preprocess(im)

            np_im = np.array(im)

            images.append(np_im)
            labels.append(color)

        except Exception as e:
            print(e)

    images = np.array(images,dtype="float32")
    labels = np.array(labels, dtype="float64")

    #convert x to a new size
    new_X = np.empty((0,120000))
    print(new_X.shape)
    for x in images:
        new_X = np.append(new_X, [x.ravel()], axis=0)#.shape

    print(new_X.shape)
    images = new_X

    return(images, labels)

def run_tsne():
    n_samples = 300
    n_components = 2
    perplexities = [10, 100, 150, 200, 500]#[50, 75, 100, 125, 150]#[5, 30, 50, 100]
    (fig, subplots) = plt.subplots(2, len(perplexities), figsize=(15, 8))

    #resize the car images to be the same size
    # for i in range(11):
    #     if not os.path.exists("./data/test_cropped_cars/" + str(i).zfill(2) + "/resized_cars"):
    #         os.makedirs("./data/test_cropped_cars/" + str(i).zfill(2) + "/resized_cars")
    #     resize("./data/test_cropped_cars/" + str(i).zfill(2) + "/")

    # load up original data
    #TODO: Make this work for all folders
    X, y = get_data("./data/test_cropped_cars/00/resized_cars/", False)

    for i, perplexity in enumerate(perplexities):
        ax = subplots[0][i]

        t0 = time()
        tsne = manifold.TSNE(n_components=n_components, init='random',
                             random_state=0, perplexity=perplexity)
        Y = tsne.fit_transform(X)
        t1 = time()
        print("Colors, perplexity=%d in %.2g sec" % (perplexity, t1 - t0))
        ax.set_title("Perplexity=%d" % perplexity)
        vis_x = Y[:, 0]
        vis_y = Y[:, 1]
        ax.set_title("Perplexity=%d" % perplexity)
        ax.scatter(vis_x, vis_y, c=y, cmap=plt.cm.get_cmap("jet", 10))
        ax.axis('tight')

    #now for preprocessed data
    X, y = get_data("./data/test_cropped_cars/00/resized_cars/")
    test_X, test_y = get_data("./data/test_cropped_cars/resized_cars_test/")
    print(type(test_y))
    print(test_y)
    # test_y =

    for i, perplexity in enumerate(perplexities):
        ax = subplots[1][i]

        t0 = time()
        tsne = manifold.TSNE(n_components=n_components, init='random',
                             random_state=0, perplexity=perplexity)
        Y = tsne.fit_transform(X)
        t1 = time()
        print("Colors, perplexity=%d in %.2g sec" % (perplexity, t1 - t0))
        ax.set_title("Perplexity=%d" % perplexity)
        vis_x = Y[:, 0]
        vis_y = Y[:, 1]

        #add in the test data
        # tsne = manifold.TSNE(n_components=n_components, init='random',
        #                      random_state=0, perplexity=perplexity)
        # test_Y = tsne.fit_transform(test_X)
        # test_vis_x = test_Y[:, 0]
        # test_vis_y = test_Y[:, 1]
        # ax.scatter(test_vis_x, test_vis_y, c=test_y, cmap=plt.cm.get_cmap("jet", 10))

        ax.set_title("Perplexity=%d" % perplexity)
        ax.scatter(vis_x, vis_y, c=y, cmap=plt.cm.get_cmap("jet", 10))
        ax.axis('tight')

    # plt.colorbar(ticks=range(10))
    # plt.clim(-0.5, 9.5)
    plt.show()
    plt.savefig('demo_tsne.png')
    # kmeans_cluster(Y, y, test_X, test_y)

### SOURCES ###
