# -*- coding: utf-8 -*-
"""
Created on Wed May 14 12:38:28 2025

@author: cedri
"""

# receiver.py
import numpy as np
from multiprocessing import shared_memory
import time

def receive_Array():
    # Shared Memory Namen (müssen mit dem Sender übereinstimmen)
    array_name = "shared_array_123"
    ack_name = "ack_flag_123"

    shape = (1,8)  # Muss bekannt sein
    dtype = np.int32

    try:
        # Shared Memory Blöcke verbinden
        shm_array = shared_memory.SharedMemory(name=array_name)
        shm_ack = shared_memory.SharedMemory(name=ack_name)

        shared_array = np.ndarray(shape, dtype=dtype, buffer=shm_array.buf)
        
        liste=shared_array.tolist()# Bei dem Versuch ein np.array als vaiable zu uebermitteln stirbt der kernel
        # Daten ausgeben
        print("[RECEIVER] Empfangenes Array:")
        print(shared_array)
        # Empfangsbestätigung setzen
        shm_ack.buf[0] = 1
        print("[RECEIVER] Empfangsbestätigung gesendet.")
        
    except FileNotFoundError:
        print("[RECEIVER] Shared Memory wurde nicht gefunden.")
        liste=None
    finally:
        # Speicher freigeben (aber nicht unlinken!)
        try:
            shm_array.close()
            shm_ack.close()
        except:
            pass
    return liste # liste anstelle von shared_array wegen kernel problemen
        



if __name__ == "__main__":
    Empfangen=receive_Array()
    
