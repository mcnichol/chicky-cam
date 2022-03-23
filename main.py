#!/usr/bin/env python3

#Modified by mcnichol
#Date: 22.03.23
#Desc: Web app streaming RPI camera
# main.py

from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import threading
import os
import errno
import socket


app = Flask(__name__)
host = socket.gethostbyname(socket.gethostname())
port = 5000

@app.route('/')
def index():
    return render_template('index.html') 

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def is_port_open(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.close()
    except socket.error as e:
        print("Unable to start server with error {}".format(e))
        print("Check if running at http://{}:{}".format(host,port))
        return False
    
    return True

if __name__ == '__main__':
    if is_port_open(port):
        pi_camera = VideoCamera(flip=False) 
        app.run(host=host, port=port, debug=False)
    else:
        print("Server not started.")
    


