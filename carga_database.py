#para activar anaconda $conda config --set auto_activate_base True
#y volver a abrir el terminal
import numpy as np
import pandas as pd
import sys
import scipy as sc #procesamiento, para transformada fourier, interpolacion etc
from scipy.io import wavfile
import soundfile as sf
import os
import matplotlib.pyplot as plt
import math
import algorit_huella_prueba as alg
import funciones as func
import pickle
from typing import List, Dict, Tuple

resultado = []

carpeta = sys.argv[1]


archivos = os.listdir(carpeta)
numarch = len(os.listdir(carpeta))

print(numarch)

lista_canciones = []
database: Dict[int, List[Tuple[int, int]]] = {}

for canc in archivos:
    nombre, ext = os.path.splitext(canc)
    
    #Si es .mp3, el array tiene dimensiones estéreo de x,2, lo necesitamos en mono
    if ext == ".mp3":
       funOG ,Fs  = sf.read(carpeta + '/' + '{0}.mp3'.format(nombre))
       if(funOG.ndim>1):
            funOG = funOG.mean(axis=-1)    
    #En .wav no hay problema
    else:
        Fs, funOG = wavfile.read(carpeta + '/' + canc) #Fs frecuencia de 16000 hercios 
            
    constelacion = func.create_constellation(funOG, Fs)
    hashes = func.create_hashes(constelacion, canc)
    for hash, time_index_pair in hashes.items():
        if hash not in database:
            database[hash] = []
        database[hash].append(time_index_pair)
        
with open("database.pickle", 'wb') as db:
    pickle.dump(database, db, pickle.HIGHEST_PROTOCOL)



#python3 carga_database.py songs