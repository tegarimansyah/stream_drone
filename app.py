#!/usr/bin/env python

from flask import Flask, render_template, Response, request

'''
Camera Option
'''
# from camera import Camera # emulated camera
from camera import VideoCamera # Video camera
# from camera_pi import Camera # Raspberry Pi camera module (requires picamera package)
# from receive_images import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    global savestate
    global filestate
    savestate = False
    filestate = False
    print('Init variable')
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        # print(savestate)

        frame = camera.get_frame(savestate)    
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""

    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/config', methods=['GET','POST'])
def saving():
    global savestate
    global filestate

    if request.method == "POST":
        print('From AJAX: ' + str(request.form))
        if 'save' in request.form:
            savestate = not savestate
        if 'files' in request.form:
            filestate = not filestate
        print('savestate : ' + str(savestate))
        print('filestate : ' + str(filestate))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
