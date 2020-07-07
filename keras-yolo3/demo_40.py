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
