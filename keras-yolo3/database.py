import requests
import json
import hashlib
import os
import urllib
# import gevent
import time
from datetime import datetime
from pymongo import MongoClient
from bson import json_util

from gevent import monkey, socket
from gevent.pool import Pool

# System ID: gwu
# Key: 2177402e13f68215c3381fdf328170d7

monkey.patch_socket()
pool = Pool(30)

# md5 hash for cameras to check if a camera has not been updated
def md5(fname):
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	# hexdigest is the string value of the hash
	return hash_md5.hexdigest()


def mongo_download(index, camera):

	url = camera['content']['hugeJpeg']
	# print(urllib.parse.quote(url))
	dt = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
	filename = os.path.basename(dt)

	date_formatted = str(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
	# setting up filepath for file structure to download
	filepath = f"{index}/{index}_{filename}.jpg"
	directory = f"static/images/{index}"
	os.makedirs(directory, exist_ok=True)

	f = open('static/images/' + filepath,'wb')
	f.write(requests.get(url).content)
	f.close()

	# downloading image

	# # getting individual camera in mongoDB and then checking hash
	query = db.test.find({'id': index})

	try:
		camId = json.loads(json_util.dumps(query))[0]

	except IndexError as e:
		camId = json.loads(json_util.dumps(query))

	if not camId:
		db.test.insert_one(
			{
				'id': index,
				'filepath': filepath,
				'timestamp': dt,
				'datetime_readable': date_formatted,
				'mhash': md5(f'static/images/{filepath}')
			}
		)
	else:
		if camId['mhash'] == md5(f'static/images/{filepath}'):
			print(f"Camera {index} image has not been updated, skipping...")
		else:
			print(f"Camera {index} image is being added to database...")
			db.test.insert_one(
				{
					'id': index,
					'filepath': filepath,
					'timestamp': dt,
					'datetime_readable': date_formatted,
					'mhash': md5(f'static/images/{filepath}')
				}
			)


	# update camera after every run to prevent change of url for the traffic camera
	db.cameras.update_one(
		{'id': index},
		{
			'$set': {
				'name': camera['name'],
				'orientation': camera['orientation'],
				'location': {
					'cityCode': camera['location']['cityCode'],
					'cityName': camera['location']['cityName'],
					'stateCode': camera['location']['stateCode'],
					'stateName': camera['location']['stateName'],
					'countryCode': camera['location']['countryCode'],
					'countryName': camera['location']['countryName'],
					'zipCode': camera['location']['zipCode'],
					'latitude': camera['location']['latitude'],
					'longitude': camera['location']['longitude']
				},
				'status': {
					'isDisabled': camera['status']['isDisabled'],
					'hasQualityWarning': camera['status']['hasQualityWarning'],
					'quality': {
						'uptime1Day': camera['status']['quality']['uptime1Day'],
						'uptime1Week': camera['status']['quality']['uptime1Week'],
						'uptime1Month': camera['status']['quality']['uptime1Month']
						}
					},
					'content': {
						'hugeJpeg': camera['content']['hugeJpeg']
					},
					'createdAt': camera['createdAt'],
					'updatedAt': camera['updatedAt']
				}
			},
		upsert=True
	)




client = MongoClient('localhost', 27017)
db = client['ambervision']

trafficland_api = 'http://api.trafficland.com/v2.0/json/video_feeds?system=gwu&key=2177402e13f68215c3381fdf328170d7'
response = requests.get(trafficland_api)

data = json_util.loads(response.text)

start_time = time.time()

jobs = [pool.spawn(mongo_download, index, camera) for index, camera in enumerate(data, 1)]

print('Downloaded images')

print("--- %s seconds ---" % (time.time() - start_time))
