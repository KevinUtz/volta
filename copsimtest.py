# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 20:15:53 2025

@author: cedri
"""
"""
#hier alle dependencies

pip install numpy
pip install opencv-python
pip install coppeliasim_zmqremoteapi_client 

#simulationsdatei im verzeichnis ablegen:
#Pfad: C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\scenes\
#Ordner "Test" erstellen und "TEST_3_cam.ttt" darin hinterlegen

coppeliasim öffnen, dann copsimtest.py ausfuehren
"""
#import time

import numpy as np
import cv2

from coppeliasim_zmqremoteapi_client import RemoteAPIClient


print('Program started')

client = RemoteAPIClient()
sim = client.require('sim')

sim.loadScene(sim.getStringParam(sim.stringparam_scenedefaultdir) + '/Test/TEST_3_cam.ttt')

visionSensorHandle = sim.getObject('/visionSensor')
#passiveVisionSensorHandle = sim.getObject('/PassiveVisionSensor')

# Run a simulation in stepping mode:
sim.setStepping(True)
sim.startSimulation()

fourcc = cv2.VideoWriter_fourcc(*'XVID')
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#fourcc = cv2.VideoWriter_fourcc(*'AMPG')
img, [resX, resY] = sim.getVisionSensorImg(visionSensorHandle)
out = cv2.VideoWriter('C:/Users/cedri/Desktop/output.avi',fourcc, 24.0, (resX,resY))
#out = cv2.VideoWriter('output.avi', -1, 20.0, (256,256))


#while (t := sim.getSimulationTime()) < 10:
while True:
    img, [resX, resY] = sim.getVisionSensorImg(visionSensorHandle)
    img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)

    # In CoppeliaSim images are left to right (x-axis), and bottom to top (y-axis)
    # (consistent with the axes of vision sensors, pointing Z outwards, Y up)
    # and color format is RGB triplets, whereas OpenCV uses BGR:
    img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
   

    cv2.imshow('', img)
    out.write(img)
    cv2.waitKey(1)
    sim.step()  # triggers next simulation step

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

sim.stopSimulation()
out.release()
cv2.destroyAllWindows()

print('Program ended')