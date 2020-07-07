import flask
from flask import request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

client = MongoClient('localhost', 27017)
db = client['ambervision']


@app.route('/', methods=['GET'])
def home():
	return '''<h1>Amber Vision API</h1>
<p>A prototype API for image collection and machine learning training.</p>'''


@app.route('/camera', methods=['GET'])
def cameras():

	if 'id' in request.args:
		id = int(request.args['id'])
		cam = db.cameras.find({'id': str(id)})
		page_sanitized = json.loads(json_util.dumps(cam))
		return jsonify(page_sanitized)
	else:
		all_cams = db.cameras.find()
		page_sanitized = json.loads(json_util.dumps(all_cams))
		return jsonify(page_sanitized)

@app.route('/test', methods=['GET'])
def test():
	fp = './demo_bb2_pic.png'
	# sample_response = {'cameras':[{'id':'1'},{'id':'2'}]}
	return jsonify(fp)


@app.route('/query', methods=['GET', 'POST'])
def query():

	if request.method == "POST":
		pass


# {"id": "40", "filepath": "40/40_20191214_121527_detected_detected_detected_detected.png", "cars:": [{"box": [260.35333251953125, 244.84683227539062, 314.5198974609375, 267.124267578125], "class": [0], "color": "string"},


@app.route('/image', methods=['GET', 'POST'])
def images():

	if request.method == "GET":
		if 'id' in request.args:
			id = int(request.args['id'])
			img = db.images.find({'id': id})
			print(img)
			page_sanitized = json.loads(json_util.dumps(img))
			print(page_sanitized)
			return jsonify(page_sanitized)
		elif 'all' in request.args:
			img = db.images.find().sort([("timestamp",-1)])
			page_sanitized = json.loads(json_util.dumps(img))
			print(page_sanitized)
			return jsonify(page_sanitized)
		else:
			return "Please provide a camera id to see the images for it."

	if request.method == "POST":

		# sample_json = '''{"images": [{"id": "37", "filepath": "37/37_20191214_121526_detected_detected_detected_detected.png", "boxes": [[405.4546203613281, 366.08294677734375, 478.4617919921875, 486.1227111816406], [280.2525634765625, 262.5606994628906, 328.7887268066406, 284.8843688964844], [341.454833984375, 220.49505615234375, 366.71240234375, 232.54232788085938]], "classes": [7, 9, 9], "scores": [0.5062538385391235, 0.963388979434967, 0.4700457453727722]}, {"id": "58", "filepath": "58/58_20191214_121534_detected_detected_detected_detected.png", "boxes": [[130.2920379638672, 259.81072998046875, 142.85780334472656, 276.609619140625], [118.4750747680664, 397.0426940917969, 129.49044799804688, 404.8941650390625], [160.77447509765625, 222.5028839111328, 187.36436462402344, 231.27137756347656], [119.3160400390625, 325.9137268066406, 129.4978485107422, 332.61187744140625], [138.04849243164062, 309.4292907714844, 151.9659423828125, 318.39935302734375], [159.38504028320312, 208.0611572265625, 186.04457092285156, 219.28781127929688], [119.87620544433594, 330.4806823730469, 129.76026916503906, 339.04833984375]], "classes": [9, 9, 9, 9, 9, 9, 9], "scores": [0.872340202331543, 0.770513653755188, 0.7095876336097717, 0.5281589031219482, 0.4854539930820465, 0.4801640510559082, 0.4568455219268799]}, {"id": "39", "filepath": "39/39_20191214_121527_detected_detected_detected_detected.png", "boxes": [], "classes": [], "scores": []}, {"id": "7", "filepath": "7/7_20191214_121515_detected_detected_detected_detected.png", "boxes": [], "classes": [], "scores": []}, {"id": "2", "filepath": "2/2_20191214_121513_detected_detected_detected_detected.png", "boxes": [], "classes": [], "scores": []}, {"id": "6", "filepath": "6/6_20191214_121515_detected_detected_detected_detected.png", "boxes": [[313.5224914550781, 263.5370178222656, 344.1451416015625, 272.26995849609375], [312.0425720214844, 578.0835571289062, 353.00335693359375, 623.0489501953125]], "classes": [0, 9], "scores": [0.4301641583442688, 0.5314797759056091]}, {"id": "40", "filepath": "40/40_20191214_121527_detected_detected_detected_detected.png", "boxes": [[260.35333251953125, 244.84683227539062, 314.5198974609375, 267.124267578125], [271.626708984375, 614.6727294921875, 324.02239990234375, 634.113525390625], [255.46292114257812, 309.9502868652344, 315.15130615234375, 327.46234130859375], [260.06396484375, 555.6226196289062, 301.58367919921875, 571.317138671875], [160.46937561035156, 325.6271057128906, 201.8762664794922, 346.27642822265625], [171.31893920898438, 170.89901733398438, 216.55108642578125, 190.63865661621094], [233.27362060546875, 185.93667602539062, 252.7972412109375, 203.42042541503906], [193.6310577392578, 584.1288452148438, 231.39859008789062, 636.6364135742188]], "classes": [0, 0, 0, 0, 9, 9, 9, 9], "scores": [0.8443766236305237, 0.5799102783203125, 0.5494356751441956, 0.36131301522254944, 0.8467427492141724, 0.7508227229118347, 0.6128215789794922, 0.594504714012146]}, {"id": "18", "filepath": "18/18_20191214_121520_detected_detected_detected_detected.png", "boxes": [], "classes": [], "scores": []}, {"id": "105", "filepath": "105/105_20191214_121552_detected_detected_detected_detected.png", "boxes": [[241.33929443359375, 527.9241333007812, 299.4132080078125, 550.5498657226562], [170.0068817138672, 96.06747436523438, 207.06285095214844, 118.33644104003906], [215.7429656982422, 312.734130859375, 293.4521789550781, 383.06689453125], [127.0321044921875, 187.84747314453125, 243.80332946777344, 448.6425476074219], [163.94862365722656, 456.2919921875, 201.89610290527344, 475.90106201171875], [215.28880310058594, 467.7429504394531, 234.89988708496094, 481.4919738769531], [215.4560089111328, 316.4737243652344, 296.0764465332031, 381.92822265625]], "classes": [0, 0, 5, 6, 9, 9, 9], "scores": [0.9728093147277832, 0.7026160359382629, 0.3587568402290344, 0.984961986541748, 0.7059154510498047, 0.6103623509407043, 0.5878627300262451]}, {"id": "8", "filepath": "8/8_20191214_121516_detected_detected_detected_detected.png", "boxes": [[362.0382995605469, 361.9378967285156, 470.1620788574219, 504.7748107910156]], "classes": [7], "scores": [0.7251837253570557]}]}'''

		# real_json = json.loads(sample_json)


		# To POST, the structure is:
		# {
		# 	id: id
		# 	filepath: filepath,
		# 	boxes: {
		# 		box_id: {
		# 			min_x: min_x,
		# 			min_y: min_y,
		# 			max_x: max_x,
		# 			max_y: max_y,
		# 			size: (car, truck),
		# 			color: color,
		# 			confidence: confidence
		# 		}
		# 	}
		# }

		#getting images from machine learning post
		# images = request.json["images"]
		images = json.loads(request.json)["images"]
		for image in images:
			db.images.insert_one(image)
		return "Successfully posted"


if __name__ == '__main__':
   app.run()
