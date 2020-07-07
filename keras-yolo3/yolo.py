# -*- coding: utf-8 -*-
"""
Class definition of YOLO_v3 style detection model on image and video
"""

import colorsys
import os
from timeit import default_timer as timer

import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.layers import Input
from PIL import Image, ImageFont, ImageDraw

from yolo3.model import yolo_eval, yolo_body, tiny_yolo_body
from yolo3.utils import letterbox_image
import os
from keras.utils import multi_gpu_model
import json
import pandas as pd
import requests

class YOLO(object):
    _defaults = {
        "model_path": 'model_data/yolo.h5',
        "anchors_path": 'model_data/yolo_anchors.txt',
        "classes_path": 'model_data/coco_classes.txt',
        "score" : 0.3,
        "iou" : 0.45,
        "model_image_size" : (416, 416),
        "gpu_num" : 1,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults) # set up default values
        self.__dict__.update(kwargs) # and update with user overrides
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.sess = K.get_session()
        self.boxes, self.scores, self.classes = self.generate()
        self.good_classes = ["car","truck", "bus"]

    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

        # Load model, or construct model and load weights.
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        is_tiny_version = num_anchors==6 # default setting
        try:
            self.yolo_model = load_model(model_path, compile=False)
        except:
            self.yolo_model = tiny_yolo_body(Input(shape=(None,None,3)), num_anchors//2, num_classes) \
                if is_tiny_version else yolo_body(Input(shape=(None,None,3)), num_anchors//3, num_classes)
            self.yolo_model.load_weights(self.model_path) # make sure model, anchors and classes match
        else:
            assert self.yolo_model.layers[-1].output_shape[-1] == \
                num_anchors/len(self.yolo_model.output) * (num_classes + 5), \
                'Mismatch between model and given anchor and class sizes'

        print('{} model, anchors, and classes loaded.'.format(model_path))

        # Generate colors for drawing bounding boxes.
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))
        np.random.seed(10101)  # Fixed seed for consistent colors across runs.
        np.random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.
        np.random.seed(None)  # Reset seed to default.

        # Generate output tensor targets for filtered bounding boxes.
        self.input_image_shape = K.placeholder(shape=(2, ))
        if self.gpu_num>=2:
            self.yolo_model = multi_gpu_model(self.yolo_model, gpus=self.gpu_num)
        boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
                len(self.class_names), self.input_image_shape,
                score_threshold=self.score, iou_threshold=self.iou)
        return boxes, scores, classes

    ## CODE I WROTE TO CROP IMAGE ###
    #boxes = keeping track of boxes over time to output as json
    def crop_car_image(self, np_image, bboxes, classes, scores, cur_car_count, dataset_num, img_path):
        # print("Cropping car images...")

        #make sure dir exists
        #make new dir
        directory = './static/images/cropped_cars/' + str(dataset_num).zfill(2) + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        car_count = cur_car_count
        thickness = (np_image.size[0] + np_image.size[1]) // 300

        for i, c in reversed(list(enumerate(classes))):
            #want 200 cars per set
            if(car_count == 100):
                car_count = 0
                dataset_num += 1

                #make new dir
                if not os.path.exists(directory):
                    os.makedirs(directory)

            predicted_class = self.class_names[c]
            # print(predicted_class)

            #check if it is one of our good classes
            if(predicted_class not in self.good_classes):
                continue

            box = bboxes[i]
            score = scores[i]

            #threshold the cars we are getting
            # if(score < 0.5):
            #     continue

            # print("SCORE:")
            # print(score)

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(np_image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(np_image.size[0], np.floor(right + 0.5).astype('int32'))

            bbox = (left, top, right, bottom)

            # cropped_car = np_image[top + i:bottom - i,left + i:right - i]
            # img = Image.fromarray(cropped_car, 'RGB')
            img = np_image.crop(bbox)
            img.save(directory + str(car_count) + '.png')

            box_id = {
                "min_x": box[0],
                "max_x": box[2],
                "min_y": box[1],
                "max_y": box[3]
            }

            car_count += 1

        return car_count, dataset_num

    #Sending info to our API for each image
    def send_info(self, file_path, bboxes, classes, scores):
        print(file_path[14:])
        file_path = file_path[14:]
        cam_num = ''

        #get our camera number from this business
        for letter in file_path:
            if(letter == '/'):
                break
            else:
                cam_num += letter

        # package it all up into json???
        send_info = {
            "id": cam_num,
            "filepath": file_path[:-4] + "_detected.png",
            "boxes": bboxes.tolist(),
            "classes": classes.tolist(),
            "scores": scores.tolist(),
            "timestamp":file_path[-19:-4]
        }

        #execute post request
        return send_info

    #get most recent image downloaded in each folder
    def get_img_list(self):
        img_list = []
        #build filepath
        filepath = "static/images/"

        for path in os.listdir(filepath):
            try:
                file = sorted(os.listdir(filepath + path + "/"))[-1]
                img_list.append(filepath + path + "/" + file)
            except:
                print("Failed to use Dir...")

        return img_list

    ### MODIFIED THIS FOR OUR DATA ###
    def detect_image(self):
        # images = []
        # with open('./data/test.txt') as f:
        #    for line in f:
        #        images.append(line)
        images = self.get_img_list()
        # print(images)

        cur_cars = 0
        dataset_num = 0
        post_info = {
            "images":[]
        }
        for i, img_path in enumerate(images):
            try:
                image = Image.open(img_path)
            except Exception as e:
                print(e)
                continue
            # print(image)
            start = timer()

            if self.model_image_size != (None, None):
                assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
                assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
                boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
            else:
                new_image_size = (image.width - (image.width % 32),
                                  image.height - (image.height % 32))
                boxed_image = letterbox_image(image, new_image_size)
            image_data = np.array(boxed_image, dtype='float32')

            # print(image_data.shape)
            image_data /= 255.
            image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

            out_boxes, out_scores, out_classes = self.sess.run(
                [self.boxes, self.scores, self.classes],
                feed_dict={
                    self.yolo_model.input: image_data,
                    self.input_image_shape: [image.size[1], image.size[0]],
                    K.learning_phase(): 0
                })

            # print('Found {} boxes for {}'.format(len(out_boxes), 'img'))

            #crop image of car for color classification
            cur_cars, dataset_num = self.crop_car_image(image, out_boxes, out_classes, out_scores, cur_cars, dataset_num, img_path)

            #send the imagery to data processing (Suraj)
            post_info['images'].append(self.send_info(img_path, out_boxes, out_classes, out_scores))

            font = ImageFont.truetype(font='font/FiraMono-Medium.otf')
                        #size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
            thickness = (image.size[0] + image.size[1]) // 300

            # print(out_classes)

            for i, c in reversed(list(enumerate(out_classes))):
                predicted_class = self.class_names[c]

                if(predicted_class not in self.good_classes):
                    continue

                box = out_boxes[i]
                score = out_scores[i]

                label = '{} {:.2f}'.format(predicted_class, score)
                draw = ImageDraw.Draw(image)
                label_size = draw.textsize(label, font)

                top, left, bottom, right = box
                top = max(0, np.floor(top + 0.5).astype('int32'))
                left = max(0, np.floor(left + 0.5).astype('int32'))
                bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
                right = min(image.size[0], np.floor(right + 0.5).astype('int32'))

                #for printing out detections
                # print(label, (left, top), (right, bottom))

                if top - label_size[1] >= 0:
                    text_origin = np.array([left, top - label_size[1]])
                else:
                    text_origin = np.array([left, top + 1])

                # My kingdom for a good redistributable image drawing library.
                for i in range(thickness):
                    draw.rectangle(
                        [left + i, top + i, right - i, bottom - i],
                        outline=self.colors[c])
                draw.rectangle(
                    [tuple(text_origin), tuple(text_origin + label_size)],
                    fill=self.colors[c])
                draw.text(tuple(text_origin), label, fill=(0, 0, 0))
                del draw

            #make sure it isnt repeatedly doing detected
            if(img_path[-13:] != "_detected.png"):
                # print(img_path[-13:])
                image.save(img_path[:-4] + "_detected.png")

            end = timer()
            # print(end - start)

        #save json of bounding boxes
        post_info = json.dumps(post_info)
        print(post_info)
        requests.post("http://127.0.0.1:5000/image", json=post_info)


    def close_session(self):
        self.sess.close()

# def detect_video(yolo, video_path, output_path=""):
#     import cv2
#     vid = cv2.VideoCapture(video_path)
#     if not vid.isOpened():
#         raise IOError("Couldn't open webcam or video")
#     video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
#     video_fps       = vid.get(cv2.CAP_PROP_FPS)
#     video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
#                         int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#     isOutput = True if output_path != "" else False
#     if isOutput:
#         print("!!! TYPE:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
#         out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
#     accum_time = 0
#     curr_fps = 0
#     fps = "FPS: ??"
#     prev_time = timer()
#     while True:
#         return_value, frame = vid.read()
#         image = Image.fromarray(frame)
#         image = yolo.detect_image(image)
#         result = np.asarray(image)
#         curr_time = timer()
#         exec_time = curr_time - prev_time
#         prev_time = curr_time
#         accum_time = accum_time + exec_time
#         curr_fps = curr_fps + 1
#         if accum_time > 1:
#             accum_time = accum_time - 1
#             fps = "FPS: " + str(curr_fps)
#             curr_fps = 0
#         cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                     fontScale=0.50, color=(255, 0, 0), thickness=2)
#         cv2.namedWindow("result", cv2.WINDOW_NORMAL)
#         cv2.imshow("result", result)
#         if isOutput:
#             out.write(result)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     yolo.close_session()



#Labels for test_1.jpeg
# [1 2 2 2 2 2 9]
# traffic light 0.75 (92, 74) (113, 117)
# car 0.36 (117, 70) (132, 80)
# car 0.37 (127, 29) (136, 40)
# car 0.44 (142, 53) (156, 63)
# car 0.82 (119, 60) (142, 76)
# car 0.94 (87, 49) (105, 63)
# bicycle 0.88 (17, 47) (63, 76)
