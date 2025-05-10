# -*- coding: utf-8 -*-
"""
Created on Sat May 10 16:22:12 2025

@author: kevin
"""

import cv2
from flask import Flask, request, jsonify, Response #Response = Klasse zum senden von HTTP-Stream
import atexit

app = Flask(__name__)  # Erstellen des Servers
shared_data = {}  # Interner Speicher


# Globale Kamera-Initialisierung
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Überprüfen, ob der Stream geöffnet werden konnte
if not cap.isOpened():
    print("Fehler beim Öffnen des Streams")
    exit()

## Bild aus Webcam

def get_frame():
    ret, frame = cap.read()
    if not ret:
        print("Fehler beim Abrufen des Frames")
        return None

    # Bild in JPEG umwandeln
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        return None

    # Bild als Byte-Daten zurückgeben
    return buffer.tobytes()

##Bildübergabe an Client noch ohne client funktion
@app.route("/image")
def image():
  ret, frame = cap.read()
  if not ret:
       return "Fehler beim Abrufen des Frames", 500

  ret, buffer = cv2.imencode('.jpg', frame)
  if not ret:
       return "Fehler beim Kodieren des Bildes", 500

  return Response(buffer.tobytes(), mimetype='image/jpeg')

## Speichern von Anfragen als Bsp. Name und deren Ausgabe
@app.route("/data", methods=["POST"])
def write_data():
    incoming = request.get_json()
    if incoming:
        shared_data.update(incoming)
        return "Daten gespeichert", 200
    return "Ungültige Anfrage", 400

@app.route("/data", methods=["GET"])  # Bekommen von Daten
def read_data():
    return jsonify(shared_data), 200

@app.route("/hello", methods=["POST"])  # Hallo Welt
def hello():
    data = request.get_json()
    name = data.get("name", "Unbekannt")
    return jsonify({"message": f"Hallo, {name}!"})

# Starten des Servers mit Waitress
if __name__ == "__main__":
    from waitress import serve  # Servertypus
    print("Starte API auf http://127.0.0.1:5000 ...")  # Ausgabe im Terminal
   
    serve(app, host="127.0.0.1", port=5000)  # Serverstart
       
@atexit.register #Richtiges Freigeben der Cam
def cleanup():
    if cap.isOpened():
        cap.release()