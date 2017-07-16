# Raspi menjadi server untuk mengirim data
# PC menjadi client untuk meminta dan monitoring data

import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time
import base64
import json
import os.path

# IP = "192.168.43.229" # Hostspot Android
IP = "192.168.0.100" # Hotspot TRC

def receive_frame(r):
	print('\n=================\n')
	loaded_r = json.loads(r)
	uid, img_b64, gps = loaded_r['uid'], loaded_r['img'], loaded_r['gps']
	image = decode(img_b64)
	print('Uid: ' + str(uid))
	display(image,display=True)

def decode(img_b64):
	nparr = np.fromstring(img_b64.decode('base64'), np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	return img

def display(image,save=True,display=False):
	now = time.strftime('%Y%m%d%H%M%S')
	name = now + '.jpg'
	if save and not os.path.isfile(name):
		cv2.imwrite(name,image)

	if (display):
		# cv2.imshow('images',image)
		# cv2.waitKey(1)
		# cv2.destroyAllWindows()
		ret, jpeg = cv2.imencode('.jpg', image)
		return jpeg.tobytes()

## The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
	print("Connected to broker with result code "+str(rc))
	client.subscribe("image")
	# client.subscribe("gps")

## The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	millisStart = int(round(time.time() * 1000))
	if msg.topic == "image":
		receive_frame(msg.payload)
	millisStop = int(round(time.time() * 1000))
	print('Start: ' + str(millisStart) + '\nStop: ' + str(millisStop) + '\nReceived Time: ' + str(millisStop-millisStart) + ' ms')

	# if msg.topic == "gps":
	# 	print("GPS data: "+str(msg.payload))

# cv2.namedWindow('images', cv2.WINDOW_NORMAL)
# cv2.resizeWindow("images", 640, 480)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(IP, 1883, 60)

## Blocking call that processes network traffic, dispatches callbacks and
## handles reconnecting.
## Other loop*() functions are available that give a threaded interface and a
## manual interface.
client.loop_forever()