# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import cv2


cap=cv2.VideoCapture("rtsp://192.168.1.10/color")
   
if not cap.isOpened():
    print("test1")
    
while True:
    ret,frame=cap.read()
    
    if not ret:
        print("test2")
        break
    cv2.imshow("name",frame)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()