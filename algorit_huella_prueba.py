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
import scipy.signal as signal
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cosine


#a = open("test.txt")
#print(a.read())

#b = sys.argv



carpeta = "songs"
fragmentos = "fragments"

archivos = os.listdir(carpeta)
numarch = len(os.listdir(carpeta))

datoscsv = {
    'fragment': [],
    'song': []
}


def extraer_espectograma(x,fs):
    # Normaliza los valores de la señal
    x = x / np.max(np.abs(x))
    
    # Calcula el espectograma
    inutil, inutil2, espectograma = signal.spectrogram(x, fs)
    
    # Hacemos la media con él
    espectograma = np.mean(espectograma, axis=1)
    
    return espectograma

def identificar(espectograma, lista):
    distancia_min = float('inf')
    cancion = None
    pos = None
    
    for elemento in lista:
        len(elemento[1])
        # Calcula la distancia euclidiana entre las huellas digitales
        distancia = euclidean(espectograma,elemento[1])
        #print(distancia)
        # Actualiza la canción identificada si la distancia es menor que el mínimo
        if distancia < distancia_min:
           
            distancia_min = distancia
            pos = lista.index(elemento)
            cancion = elemento[0]
    
    #Umbral de corte
    umbral = 0.0001
    
    # Si la distancia mínima está por debajo del umbral, considera que es la misma canción
    if distancia_min < umbral:
        return cancion
    else:
        return "NOT_FOUND"

#TASA DE ERROR: 64.80%
# RESULTADOS GLOBALES:     Percentage
# Correct (Song->Song)     37.052632
# Correct (NF->NF)          0.000000
# Incorrect (Song->Song)   62.736842
# Incorrect (Song->NF)      0.210526
# Incorrect (NF->Song)    100.000000


def identificar2(espectograma, lista):
    #distancia_min = float('inf')
    similitud = 0.0
    cancion = None
    
    for elemento in lista:
        len(elemento[1])
        # Calcula la distancia euclidiana entre las huellas digitales
        #distancia = euclidean(espectograma,elemento[1])
        #print(distancia)
        a_real =espectograma.real.flatten()
        a_imag =espectograma.imag.flatten()
        a = np.concatenate((a_real, a_imag))
        b_real=elemento[1].real.flatten()
        b_imag=elemento[1].imag.flatten()
        b = np.concatenate((b_real, b_imag))
        coseno_similaridad = 1 - cosine(a,b)
        #print(coseno_similaridad)
        # Actualiza la canción identificada si la distancia es menor que el mínimo
        if coseno_similaridad > similitud:
       
            similitud = coseno_similaridad
            cancion = elemento[0]

    #Umbral de corte
    umbral = 0.8

    # Si la distancia mínima está por debajo del umbral, considera que es la misma canción
    if similitud > umbral:
        return cancion
    else:
        return "NOT_FOUND"
