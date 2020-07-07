import pandas as pd
import json
import requests


response = requests.get("http://127.0.0.1:5000/camera")
cameras = json.loads(response.text)


for cam in cameras:
    print("{")
    print("\tid: "+str(cam["id"]-1)+",")
    print("\tcamId: "+"\'"+str(cam["id"])+"\',")
    print("\tname: "+"\'"+str(cam["name"])+"\',")
    print("\ttype: \'marker\',")
    print("\tcoords: ["+str(cam["location"]["latitude"])+", "+str(cam["location"]["longitude"])+"],")
    print("\torientation: "+"\""+str(cam["orientation"])+"\",")
    print("},")
