# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import cv2


cap=cv2.VideoCapture("rtsp://192.168.1.10/color")
#cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M","J","P","G"))
#cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
#
#-------------------------
#http://192.168.1.10/configurations
#fuer camera aufloesung
#-------------------------
if not cap.isOpened():
    print("test1")
    
while True:
    ret,frame=cap.read()
    frame=cv2.resize(frame,(1280,720)) 
    if not ret:
        print("test2")
        break
    cv2.imshow("name",frame)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()