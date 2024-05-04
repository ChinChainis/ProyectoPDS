# -*- coding: utf-8 -*-
"""
Created on Fri May  3 19:37:30 2024

@author: migue
"""

# -*- coding: utf-8 -*-

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


#a = open("test.txt")
#print(a.read())

#b = sys.argv


carpeta = "songs"
fragmentos = "fragments"

archivos = os.listdir(carpeta)
numarch = len(os.listdir(carpeta))




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
    
    for elemento in lista:
        len(elemento[1])
        # Calcula la distancia euclidiana entre las huellas digitales
        distancia = euclidean(espectograma,elemento[1])
        #print(distancia)
        # Actualiza la canción identificada si la distancia es menor que el mínimo
        if distancia < distancia_min:
           
            distancia_min = distancia
            cancion = elemento[0]
    
    #Umbral de corte
    umbral = 0.0001
    
    # Si la distancia mínima está por debajo del umbral, considera que es la misma canción
    if distancia_min < umbral:
        return cancion
    else:
        return "NOT_FOUND"


lista_de_listas = []

for i in range(0,numarch):
    nombre, ext = os.path.splitext(archivos[i])
    
    #Si es .mp3, el array tiene dimensiones estéreo de x,2, lo necesitamos en mono
    if ext == ".mp3":
       funOG ,Fs  = sf.read(carpeta + '/' + '{0}.mp3'.format(nombre))
       if(funOG.ndim>1):
            funOG = funOG.mean(axis=-1)    
    #En .wav no hay problema
    else:
        Fs, funOG = wavfile.read(carpeta + '/' + archivos[i]) #Fs frecuencia de 16000 hercios 
        
    espectograma = extraer_espectograma(funOG, Fs)
    elemento =[archivos[i],espectograma]
    lista_de_listas.append(elemento)

archivos2 = os.listdir(fragmentos)
numarch2 = len(os.listdir(fragmentos))
resultado = []


for i in range(0,numarch2):
    Fs, funFR = wavfile.read(fragmentos + '/' + archivos2[i])
    espectograma = extraer_espectograma(funFR, Fs)
    res = identificar(espectograma,lista_de_listas)
    elemento = [archivos2[i],res]
    resultado.append(elemento)

print(resultado)