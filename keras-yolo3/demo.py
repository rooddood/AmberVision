from database import *
from yolo import *
from sk_tsne import *

import requests
import json
import hashlib
import json
import os
import requests
import pymongo
from pprint import pprint
from datetime import datetime
import urllib.request
from PIL import Image

# trafficland_api = 'http://api.trafficland.com/v2.0/json/video_feeds?system=gwu&key=2177402e13f68215c3381fdf328170d7'
#grab images using database
# mongo_download()
# print('Downloaded images!')

#initialize yolo
print('Running YOLO...')
yolo = YOLO()

#run yolo on our image
yolo.detect_image()
# r_image.show()

#TODO: DELETE train.txt, boxes?

#run tsne on results
# print("Getting tSNE...")
# run_tsne()



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

            #Save to new directory for oter training
            im.save("../Color-Classification-CNN/train/" + str(color) + "/" + str(file[:-4]) + ".jpg")

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




##Load in SFM Images
#load in csv
# data = pd.read_csv("./data/sfm_labeled_cars.csv").set_index('dataset_num')
# print(data)

#get images and labels
# print("Getting data...")
# images, labels = get_data("./data/sfm_images/", data)
# test_X, test_y = [images[501]], labels[501]
#
# print(images)
# print(labels)

# for image, label in zip(images, labels):
    # i
