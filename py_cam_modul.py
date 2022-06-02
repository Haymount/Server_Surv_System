#!/usr/bin/env python
from picamera import PiCamera 
from time import sleep
from datetime import datetime

class Picam():
    
    
    def __init__(self):
        a = 0

    def takePic(self,usrID):
        
        now = datetime.now()
        
        camera = PiCamera()
        camera.start_preview()
        sleep(5)
        name = "/home/pi/usrpics/userID" + str(usrID) + str(now)
        filename =  "%s.jpg" % name

        camera.capture(filename)
        camera.stop_preview()
        print("click")

usrID = 2

takepic = Picam.takePic(None, usrID)

takepic
    
