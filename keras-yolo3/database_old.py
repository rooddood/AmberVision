import requests
import json
import hashlib
import os
import urllib
import gevent
from datetime import datetime
from pymongo import MongoClient
from bson import json_util

from gevent import monkey, socket
from gevent.pool import Pool

# System ID: gwu
# Key: 2177402e13f68215c3381fdf328170d7

# monkey.patch_socket()
# pool = Pool(30)

# md5 hash for cameras to check if a camera has not been updated
def md5(fname):
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	# hexdigest is the string value of the hash
	return hash_md5.hexdigest()


def mongo_download():

	client = MongoClient('localhost', 27017)
	db = client['ambervision']

	trafficland_api = 'http://api.trafficland.com/v2.0/json/video_feeds?system=gwu&key=2177402e13f68215c3381fdf328170d7'
	response = requests.get(trafficland_api)

	data = json_util.loads(response.text)

	for index, camera in enumerate(data, 1):

		print('Downloading image for camera', index)
		url = camera['content']['hugeJpeg']
		dt = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
		filename = os.path.basename(dt)

		date_formatted = str(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

		# setting up filepath for file structure to download
		filepath = f"{index}/{index}_{filename}.png"
		directory = f"static/images/{index}"
		os.makedirs(directory, exist_ok=True)

		# downloading image
		urllib.request.urlretrieve(url, 'static/images/' + filepath)





# client = MongoClient('localhost', 27017)
# db = client['ambervision']

# trafficland_api = 'http://api.trafficland.com/v2.0/json/video_feeds?system=gwu&key=2177402e13f68215c3381fdf328170d7'
# response = requests.get(trafficland_api)

# data = json_util.loads(response.text)

# jobs = [pool.spawn(mongo_download, index, camera) for index, camera in enumerate(data, 1)]

# mongo_download()
#
# print('Downloaded images')
