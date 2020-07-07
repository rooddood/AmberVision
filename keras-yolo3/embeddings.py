import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.ticker import NullFormatter
from sklearn import manifold, datasets
from time import time
from skimage.color import rgb2hsv, hsv2rgb
from sklearn.metrics import accuracy_score

import cv2 as cv

import os
from PIL import Image

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA, IncrementalPCA
from sklearn.datasets.samples_generator import make_blobs

from joblib import dump, load

from sklearn import manifold
from sklearn.decomposition import PCA
from scipy.spatial import distance


def resize(path):
    print("Resizing...")
    dirs = os.listdir(path)
    # print(dirs)
    for item in dirs:
        print(path+item)
        if os.path.isfile(path + item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            print(f[29:31])
            f = f[:31] + "/resized_cars/" + f[31:]
            print(f)
            imResize = im.resize((200,200), Image.ANTIALIAS)
            # print(f + '_resized.jpg', 'JPEG')
            imResize.save(f + '_resized.png', 'PNG', quality=90)

def preprocess(image):
    image = rgb2hsv(image)
    image = hsv2rgb(image)
    new_img = cv.GaussianBlur(image, (5,5), 0)

    return new_img

# return the images and labels as arrays
def get_data(directory_in_str, data, limit=None):
    directory = os.fsencode(directory_in_str)
    labels = []
    images = []


    for folder in os.listdir(os.fsdecode(directory)):
        #check on the limit, this is used because I only have one dataset
        if(limit is not None and limit != int(folder)):
            continue

        cur_folder = os.fsdecode(directory) + folder + "/"
        print(cur_folder)

        if(folder == '17'):
            continue

        #check that it is a dir
        if(not os.path.isdir(cur_folder)):
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
            try:
                im = Image.open(directory_in_str + folder + "/resized_cars/" + str(file[:-4]) + "_resized.png")
            except:
                im = Image.open(directory_in_str + folder + "/resized_cars/" + str(file[:-4]) + "_resized.jpg")

            im = preprocess(im)

            np_im = np.array(im)

            #append to ourput array
            images.append(np_im)
            labels.append(color)
            # except Exception as e:
            #     print(e)

    images = np.array(images,dtype="float32")
    original_X = images
    labels = np.array(labels, dtype="float64")

    #convert x to a new size
    new_X = np.empty((0,120000))
    for x in images:
        new_X = np.append(new_X, [x.ravel()], axis=0)#.shape

    images = new_X

    return(images, labels, original_X)

#MY START OF 40% --> kmeans is one method of clsutering, going to try others (KNN and such)
def kmeans_cluster(X, labels_true, test_X, test_labels, perplexity):
    #get number of clusters
    n_clusters = len(np.unique(labels_true))

    # print(X.shape)

    k_means = KMeans(init='k-means++', n_clusters=n_clusters, n_init=10)
    k_means.fit(X)

    #save model
    dump(k_means, 'kmeans_perplex_' + str(perplexity) + '.joblib')
    #load model
    k_means = load('kmeans_perplex_' + str(perplexity) + '.joblib')

    y_km = k_means.fit_predict(X)
    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    k_means_labels_unique = np.unique(k_means_labels)


    ##############################################################################
    # Plot result

    # plot the 8 clusters
    colors = ['#FF0000', '#00FF00', '#0000FF', '#000000', '#FFFFFF', '#F0000F', '#0FFFF0', '#000FFF']

    #only get as many clusters as there should be
    # colors = colors[:n_clusters]
    # plt.figure()
    # for k, col in zip(range(n_clusters), colors):
    #     plt.scatter(
    #         X[y_km == k, 0], X[y_km == k, 1],
    #         s=50, c=col,
    #         marker='o', edgecolor='black',
    #         label='cluster ' + str(k)
    #     )


    # plt.scatter(X[:, 0], X[:, 1], c=y_km)

    # plot the centroids
    # plt.scatter(
    #     k_means.cluster_centers_[:, 0], k_means.cluster_centers_[:, 1],
    #     s=250, marker='*',
    #     c='red', edgecolor='black',
    #     label='centroids'
    # )
    # plt.legend(scatterpoints=1)
    # plt.grid()
    # plt.show()
    # plt.savefig("/home/kyle/Desktop/40_percent_imgs/all_samples/tsne_kmeans_perplex=" + str(perplexity) + ".png")

    #Print Accuracy
    acc=accuracy_score(labels_true, k_means.labels_)
    print("k-means Accuracy: " + str(acc))

def run_tsne(X, y):
    n_samples = 300
    n_components = 2
    perplexities = [1, 2, 5, 10, 100, 150, 200, 500]#[50, 75, 100, 125, 150]#[5, 30, 50, 100]
    (fig, subplots) = plt.subplots(1, len(perplexities), figsize=(15, 8))

    for i, perplexity in enumerate(perplexities):
        ax = subplots[i]

        # #train tsne model
        t0 = time()
        tsne = manifold.TSNE(n_components=n_components, init='random',
                             random_state=0, perplexity=perplexity)

        # #save tsne model
        dump(tsne, 'tsne_perplex=' + str(perplexity) + '.joblib')
        #load model
        # tsne = load('tsne_perplex=' + str(perplexity) + '.joblib')
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

        ax.scatter(vis_x, vis_y, c=y, cmap=plt.cm.get_cmap("jet", 10))
        ax.axis('tight')

        #for running kmeans each time
        test_X, test_y = [Y[0]], Y[0]
        kmeans_cluster(Y, y, test_X, test_y, perplexity)

    # plt.colorbar(ticks=range(10))
    # plt.clim(-0.5, 9.5)
    # plt.show()
    # plt.savefig('new_tsne.png')
    # test_X, test_y = [Y[0]], Y[0]
    # kmeans_cluster(Y, y, test_X, test_y)

#another embedding technique
def run_isomap(X, y):
    iso = manifold.Isomap(n_neighbors=6, n_components=2)
    iso.fit(df)
    manifold_2Da = iso.transform(df)
    manifold_2D = pd.DataFrame(manifold_2Da, columns=['Component 1', 'Component 2'])

    # Left with 2 dimensions
    # manifold_2D.head()

    fig = plt.figure()
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot(111)
    ax.set_title('2D Components from Isomap of Facial Images')
    ax.set_xlabel('Component: 1')
    ax.set_ylabel('Component: 2')

    # Show 40 of the images ont the plot
    x_size = (max(manifold_2D['Component 1']) - min(manifold_2D['Component 1'])) * 0.08
    y_size = (max(manifold_2D['Component 2']) - min(manifold_2D['Component 2'])) * 0.08
    for i in range(40):
        img_num = np.random.randint(0, num_images)
        x0 = manifold_2D.loc[img_num, 'Component 1'] - (x_size / 2.)
        y0 = manifold_2D.loc[img_num, 'Component 2'] - (y_size / 2.)
        x1 = manifold_2D.loc[img_num, 'Component 1'] + (x_size / 2.)
        y1 = manifold_2D.loc[img_num, 'Component 2'] + (y_size / 2.)
        img = df.iloc[img_num,:].values.reshape(pixels_per_dimension, pixels_per_dimension)
        ax.imshow(img, aspect='auto', cmap=plt.cm.gray,
                  interpolation='nearest', zorder=100000, extent=(x0, x1, y0, y1))

    # Show 2D components plot
    ax.scatter(manifold_2D['Component 1'], manifold_2D['Component 2'], marker='.',alpha=0.7)

    # ax.set_ylabel('Up-Down Pose')
    # ax.set_xlabel('Right-Left Pose')

    plt.show()

# Utility function to visualize the outputs of PCA and t-SNE
def fashion_scatter(x, colors):
    # choose a color palette with seaborn.
    num_classes = len(np.unique(colors))
    palette = np.array(sns.color_palette("hls", num_classes))

    # create a scatter plot.
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
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

def run_incremental_pca(X, y):
    n_samples = 300
    n_components = 2

    ipca = IncrementalPCA(n_components=2)
    ipca = ipca.partial_fit(X)
    # X_ipca = ipca.fit_transform(X)

    # #save tsne model
    dump(ipca, 'incremental_pca_base.joblib')

def plot_kmeans(k_means, X, n_clusters):
    y_km = k_means.fit_predict(X)
    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    k_means_labels_unique = np.unique(k_means_labels)

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


    plt.scatter(X[:, 0], X[:, 1], c=y_km)

    # plot the centroids
    plt.scatter(
        k_means.cluster_centers_[:, 0], k_means.cluster_centers_[:, 1],
        s=250, marker='*',
        c='red', edgecolor='black',
        label='centroids'
    )
    plt.legend(scatterpoints=1)
    plt.grid()
    plt.savefig("./kmeans.png")
    plt.show()

def test_models(X, y, image, label, perplexity, n_clusters):
    print(image)
    print(label)

    #load in models
    tsne = load('tsne_perplex=' + str(perplexity) + '.joblib')
    k_means = load('kmeans_perplex_' + str(perplexity) + '.joblib')
    ipca = load('incremental_pca.joblib')

    #first display kmeans of original data
    plot_kmeans(k_means, X, n_clusters)

    #TODO
    #get new embedding from iPCA


    #get new prediction from kmeans




### CODE for PCA METHOD ###
#untransforms and retransforms it
def retransform(pca, X, new_X):
    new_transform = pca.inverse_transform(X)
    new_transform = pca.fit(new_X)
    new_transform = pca.transform(new_X)
    return new_transform

def run(components, X, original_X, y, new_X, original_new_X, new_y):
    #TODO: Test value into IPCA/KMeans and Observe output
    # test_models(images, labels, test_X, test_y, 500, 8)
    colors = ['red', 'green', 'blue', 'black', 'white', 'yellow', '#FF69B4', '#32CD32']
    names = ['red', 'green', 'blue', 'black', 'white', 'yellow', 'none', 'NAC']

    ##first embed everything
    pca = PCA(n_components=components)
    pca.fit(X)
    pca.transform(X)
    # dump(pca, './saved_models/pca_base.joblib')
    # pca_base = load('./saved_models/pca_base.joblib')


    #then use original set again as test images
    test_fit = pca.fit(new_X)
    test_transform = test_fit.transform(new_X)
    # test_transform = retransform(pca, X, new_X) #figure this out once I make sure this is working

    #set up columns for pca dataframe
    cols = []
    for i in range(components):
        cols.append('pca' + str(i))

    new_pca_df = pd.DataFrame(columns = cols)

    #get each component for both new and old PCA embedding
    for i, col in enumerate(cols):
        new_pca_df[col] = test_transform[:,i]

    #Get distances between all dots and test dot
    #nearest neighbor is the color we choose
    distances = []
    new_points = []
    for i, row in new_pca_df.iterrows():
        point = row.tolist()
        new_points.append(point)

    #get each distance
    for p1 in new_points:
        row = []
        for p2 in new_points:
            d = distance.euclidean(p1, p2)

            #make sure 0 is never the mindistance
            if(d == 0):
                d = 99999
            row.append(d)
        distances.append(row)

    #get the index of the item which has mindistance
    results_df = pd.DataFrame(columns = ['img_num', 'closest_img', 'predicted_color', 'actual_color'])
    for index, row in enumerate(distances):
        df2 = pd.DataFrame([index, row.index(min(row)), colors[int(y[row.index(min(row))])], new_y[index]], columns = ['img_num', 'closest_img', 'predicted_color', 'actual_color'])
        results_df.append(df2, ignore_index = True)
        # print(index, row.index(min(row)), colors[int(y[row.index(min(row))])]) #current index, index of closest partner, color of closest partner
        # plt.imshow(original_new_X[index])
        # plt.show()

    print(results_df.head())

    # for color, i, target_name in zip(colors, [0, 1, 2, 3, 4, 5, 6, 7], names):
    #     # print(visual_transform[y == i, 0], visual_transform[y == i, 1])
    #     plt.scatter(visual_transform[y == i, 0], visual_transform[y == i, 1],
    #                 color=color, lw=2, label=target_name)
    #
    #     plt.legend(loc="best", shadow=False, scatterpoints=1)
    #     # plt.axis([-4, 4, -1.5, 1.5])
    #     plt.savefig("./ipca_result.png")
    #     plt.show()


#RESIZING the car images to be the same size
# for i in range(18): #number of folders
#     if not os.path.exists("./data/sfm_images/" + str(i).zfill(2) + "/resized_cars"):
#         os.makedirs("./data/sfm_images/" + str(i).zfill(2) + "/resized_cars")
#     resize("./data/sfm_images/" + str(i).zfill(2) + "/")

##NEWER VERSION
# for i in range(7): #number of folders
#     if not os.path.exists("./static/images/cropped_cars/" + str(i).zfill(2) + "/resized_cars/"):
#         os.makedirs("./static/images/cropped_cars/" + str(i).zfill(2) + "/resized_cars/")
#     resize("./static/images/cropped_cars/" + str(i).zfill(2) + "/")

#load in csv
print("Getting original data...")
data = pd.read_csv("./data/sfm_labeled_cars.csv").set_index('dataset_num')
#get images and labels --> original_X is the images not unrolled,
X, y, original_X = get_data("./data/sfm_images/", data)

print("Getting test data...")
test_data = pd.read_csv(os.fsdecode("./data/test_cars.csv")).set_index('dataset_num')
test_X, test_y, original_test_X = get_data("./static/images/cropped_cars/", test_data, 0)

components = 100
run(components, X, original_X, y, test_X, original_test_X, test_y)


##IPCA CODE##
#print("Running k-Means")
# kmeans_cluster(images[:500], labels[:500], test_X, test_y)

# print("Running TSNE...")
# run_tsne(images, labels)

#Incremental PCA
# run_incremental_pca(X, y)
#
# ipca_base = load('incremental_pca_base.joblib')
# ipca = ipca_base.partial_fit(test_X, test_y)
#
# # #save tsne model
# dump(ipca, 'incremental_pca_partial.joblib')
# ipca_partial = load('incremental_pca_partial.joblib')
#
# #Transform ipca
# ipca_transformed = ipca.transform(X)
# ipca = ipca_transformed
#
# # plot the 8 clusters
# colors = ['red', 'green', 'blue', 'black', 'white', 'yellow', '#FF69B4', '#32CD32']
# names = ['red', 'green', 'blue', 'black', 'white', 'yellow', 'none', 'NAC']
#
# print(ipca)
# visualize = True
# if(visualize):
#     plt.figure(figsize=(8, 8))
#     for color, i, target_name in zip(colors, [0, 1, 2, 3, 4, 5, 6, 7], names):
#         print(ipca[y == i, 0], ipca[y == i, 1])
#         plt.scatter(ipca[y == i, 0], ipca[y == i, 1],
#                     color=color, lw=2, label=target_name)
#
#
#     plt.legend(loc="best", shadow=False, scatterpoints=1)
#     plt.axis([-4, 4, -1.5, 1.5])
#     plt.savefig("./ipca_result.png")
#     plt.show()
