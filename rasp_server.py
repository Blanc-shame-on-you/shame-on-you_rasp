from flask import Flask,send_file,make_response
import cv2
import base64
import json
import numpy as np
from threading import Thread

app=Flask(__name__)
frame=None
class ImageGrabber(Thread):
    def __init__(self, ID):
        Thread.__init__(self)
        self.ID=ID
        self.cam=cv2.VideoCapture(ID)

    def run(self):
        global frame
        while True:
            ret,frame=self.cam.read()

@app.route('/',methods=['GET'])
def return_img():
    global frame
    print(type(frame))
    #byte_img=base64.b64encode(cv2.imencode('.jpg',frame)[1]).decode()
    byte_img=cv2.imencode('.jpg',frame)[1].tobytes()
    response=make_response(byte_img)
    response.headers.set('Content-Type', 'image/jpeg')
    #print(type(byte_img))
    #img={'frame': str(frame)}
    #return json.dumps(img)
    return response
    '''decoded = cv2.imdecode(np.frombuffer(byte_img, np.uint8), -1)
    cv2.imshow("234",decoded)
    cv2.waitKey()'''
    #return byte_img
    #return frame

if __name__=="__main__":
    grabber=ImageGrabber(0)
    grabber.start()
    app.run(host='0.0.0.0', debug=False,threaded=True)

