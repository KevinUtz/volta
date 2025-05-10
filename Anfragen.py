# -*- coding: utf-8 -*-
"""
Created on Sat May 10 16:50:12 2025

@author: kevin
"""

import requests
import cv2
import numpy as np
import time

payload = {"name": "Max"}
response = requests.post("http://127.0.0.1:5000/hello", json=payload)

if response.status_code == 200:
    print("Antwort vom Server:", response.json())
else:
    print("Fehler:", response.status_code)
    



cv2.destroyAllWindows()