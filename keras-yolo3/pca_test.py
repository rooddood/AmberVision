import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects

from sklearn.decomposition import PCA

import os
from PIL import Image

from sklearn.cluster import KMeans
from sklearn.datasets.samples_generator import make_blobs
from sklearn.metrics import accuracy_score
from skimage.color import rgb2hsv
import cv2 as cv


import seaborn as sns
sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5,
                rc={"lines.linewidth": 2.5})
RS = 123

def preprocess(image):
    new_img = rgb2hsv(image)
    new_img = cv.GaussianBlur(new_img, (5,5), 0)
    return new_img

# return the images and labels as arrays
def get_data(directory_in_str, data):
    directory = os.fsencode(directory_in_str)
    labels = []
    images = []


    for folder in os.listdir(os.fsdecode(directory)):
        cur_folder = os.fsdecode(directory) + folder + "/"
        print(cur_folder)

        if(folder == '17'):
            continue

        for file in os.listdir(cur_folder):
            # try:
            #get the color label from the csv
            data_row = data.loc[int(folder)]

            if(file == "resized_cars"):
                continue

            try:
                color = str(data_row[str(file)])
            except:
                color = color.values[0]

            #get the class and image
            if(color == 'Red'):
                color = 0
            elif(color == 'Green'):
                color = 1
            elif(color == 'Blue'):
                color = 2
            elif(color == 'Black'):
                color = 3
            elif(color == 'White'):
                color = 4
            elif(color == 'Yellow'):
                color = 5
            elif(color == 'None'):
                color = 6
            else:
                color = 7

            #get actual image label
            im = Image.open(directory_in_str + folder + "/resized_cars/" + str(file[:-4]) + "_resized.jpg")

            im = preprocess(im)

            np_im = np.array(im)

            #append to ourput array
            images.append(np_im)
            labels.append(color)
            # except Exception as e:
            #     print(e)

    images = np.array(images,dtype="float32")
    labels = np.array(labels, dtype="float64")

    #convert x to a new size
    new_X = np.empty((0,120000))
    for x in images:
        new_X = np.append(new_X, [x.ravel()], axis=0)#.shape

    images = new_X

    return(images, labels)


# Utility function to visualize the outputs of PCA and t-SNE
def fashion_scatter(x, colors):
    # choose a color palette with seaborn.
    num_classes = len(np.unique(colors))
    palette = np.array(sns.color_palette("hls", num_classes))

    # create a scatter plot.
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    print(colors.astype(np.int))
    sc = ax.scatter(x[:,0], x[:,1], lw=0, s=40, c=palette[colors.astype(np.int)])
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    ax.axis('off')
    ax.axis('tight')

    # add the labels for each digit corresponding to the label
    txts = []

    for i in range(num_classes):
        # Position of each label at median of data points.

        xtext, ytext = np.median(x[colors == i, :], axis=0)
        txt = ax.text(xtext, ytext, str(i), fontsize=24)
        txt.set_path_effects([
            PathEffects.Stroke(linewidth=5, foreground="w"),
            PathEffects.Normal()])
        txts.append(txt)

    plt.show()
    return f, ax, sc, txts

def kmeans_cluster(X, labels_true, test_X, test_labels):
    #get number of clusters
    n_clusters = len(np.unique(labels_true))

    print(X.shape)

    k_means = KMeans(init='k-means++', n_clusters=n_clusters, n_init=10)
    k_means.fit(X)

    #save model
    # dump(k_means, 'kmeans_checkpoint.joblib')
    # #load model
    # k_means = load('kmeans_checkpoint.joblib')

    y_km = k_means.fit_predict(X)
    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    k_means_labels_unique = np.unique(k_means_labels)


    ##############################################################################
    # Plot result

    # plot the 8 clusters
    colors = ['#FF0000', '#00FF00', '#0000FF', '#000000', '#FFFFFF', '#F0000F', '#0FFFF0', '#000FFF']

    #only get as many clusters as there should be
    colors = colors[:n_clusters]
    plt.figure()
    for k, col in zip(range(n_clusters), colors):
        plt.scatter(
            X[y_km == k, 0], X[y_km == k, 1],
            s=50, c=col,
            marker='o', edgecolor='black',
            label='cluster ' + str(k)
        )


    # plt.scatter(X[:, 0], X[:, 1], c=y_km)

    # plot the centroids
    plt.scatter(
        k_means.cluster_centers_[:, 0], k_means.cluster_centers_[:, 1],
        s=250, marker='*',
        c='red', edgecolor='black',
        label='centroids'
    )
    plt.legend(scatterpoints=1)
    plt.grid()
    plt.title("PCA")
    plt.show()

    #Print Accuracy
    acc=accuracy_score(labels_true, k_means.labels_)
    print("k-means Accuracy: " + str(acc))

#load data
data = pd.read_csv("./data/sfm_labeled_cars.csv").set_index('dataset_num')
images, labels = get_data("./data/sfm_images/", data)
test_X, test_y = [images[501]], labels[501]

print(np.unique(labels))

time_start = time.time()

pca = PCA(n_components=2)
# pca_result = pca.fit_transform(images[:-1])
pca_fit = pca.fit(images[:-1])

print('PCA done! Time elapsed: {} seconds'.format(time.time()-time_start))

pca_transformed = pca_fit.transform(images)
pca_df = pd.DataFrame(columns = ['pca1','pca2','pca3','pca4'])
pca_df['pca1'] = pca_result[:,0]
pca_df['pca2'] = pca_result[:,1]
# pca_df['pca3'] = pca_result[:,2]
# pca_df['pca4'] = pca_result[:,3]

top_two_comp = pca_df[['pca1','pca2']] # taking first and second principal component

fashion_scatter(top_two_comp.values,labels[:-1]) # Visualizing the PCA output


#then use a test value
pca_result = pca_transformed.inverse_transform(images[:-1])
pca_fit = pca_result.fit(images[-1])
pca_df = pd.DataFrame(columns = ['pca1','pca2','pca3','pca4'])

pca_df['pca1'] = pca_fit[:,0]
pca_df['pca2'] = pca_fit[:,1]
# pca_df['pca3'] = pca_result[:,2]
# pca_df['pca4'] = pca_result[:,3]

top_two_comp = pca_df[['pca1','pca2']] # taking first and second principal component

fashion_scatter(top_two_comp.values,labels) # Visualizing the PCA output

# print(pca_result.shape)
#
# test_X, test_y = [pca_result[0]], labels[0]
# kmeans_cluster(pca_result, labels, test_X, test_y)
