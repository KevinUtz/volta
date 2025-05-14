# -*- coding: utf-8 -*-
"""
Created on Wed May 14 12:37:23 2025

@author: cedri
"""
# sender.py
import numpy as np
import time
from multiprocessing import shared_memory

def send_Array(array_to_send):
    data = array_to_send
    # Shared Memory Namen (müssen mit dem Empfänger übereinstimmen)
    array_name = "shared_array_123"
    ack_name = "ack_flag_123"

    # Shared Memory für Daten und Rückmeldeflag anlegen
    shm_array = shared_memory.SharedMemory(name=array_name, create=True, size=data.nbytes)
    shm_ack = shared_memory.SharedMemory(name=ack_name, create=True, size=1)  # 1 Byte

    try:
        # Array schreiben
        shared_array = np.ndarray(data.shape, dtype=data.dtype, buffer=shm_array.buf)
        shared_array[:] = data[:]

        # Rückmelde-Flag initialisieren
        shm_ack.buf[0] = 0

        print("[SENDER] Daten gesendet. Warte auf Empfangsbestätigung...")

        # Warten auf Bestätigung (Busy-Wait mit kurzer Pause)
        while shm_ack.buf[0] != 1:
            time.sleep(0.1)

        print("[SENDER] Empfang wurde bestätigt.")

    finally:
        shm_array.close()
        shm_array.unlink()
        shm_ack.close()
        shm_ack.unlink()
        print("[SENDER] Speicher freigegeben.")

if __name__ == "__main__":
    zu_senden= np.arange(0,8,1, dtype=int)
    send_Array(zu_senden)

