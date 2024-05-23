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
import time


start_time = time.time()



datoscsv = {
    'fragment': [],
    'song': []
}

resultado = []

carpeta = sys.argv[1]
fragmento = sys.argv[2]


archivos = os.listdir(carpeta)
original = os.listdir(fragmento)
numarch = len(os.listdir(carpeta))

print(numarch)

lista_canciones = []
#Algoritmo espectrograma 
# TASA DE ERROR: 72.90%
    # RESULTADOS GLOBALES:     Percentage
    # Correct (Song->Song)     28.315789
    # Correct (NF->NF)          4.000000
    # Incorrect (Song->Song)   68.736842
    # Incorrect (Song->NF)      2.947368
    # Incorrect (NF->Song)     96.000000
modo = input('1: Algoritmo básico\n2: Algoritmo Básico mejorado\n3: Búsqueda por espectograma\n4: Búsqueda por espectrograma-coseno\nOpción:') 

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

    if(modo == '1' or modo == '2'):
        vectorcanc = funOG
        elemento =[nombre,vectorcanc]
        lista_canciones.append(elemento)
    if(modo == '3' or modo == '4'):
        espectograma = alg.extraer_espectograma(funOG, Fs)
        elemento =[nombre,espectograma]
        lista_canciones.append(elemento)

    

resultado = []

df = pd.DataFrame(datoscsv)


for frag in original:
    res = "NOT_FOUND"
    nombref, extf = os.path.splitext(frag)
    #Si es .mp3, el array tiene dimensiones estéreo de x,2, lo necesitamos en mono
    if extf == ".mp3":
        funFR ,Fs  = sf.read(fragmento + '/' + '{0}.mp3'.format(nombref))
        if(funFR.ndim>1):
           funFR = funFR.mean(axis=-1)    
    #En .wav no hay problema
    else:
        Fs, funFR = wavfile.read(fragmento + '/' + frag) #Fs frecuencia de 16000 hercios 
    if(modo == '1'):
        valmintotal = 50
        for elemento in lista_canciones:
            if(nombref != elemento[0]):
                #print(frag,elemento[0])
                valmin=func.busqueda12(elemento[1],funFR)
                if(valmin < valmintotal):
                    res = elemento[0]
                    valmintotal=valmin
    if(modo == '2'):
        valmintotal = 50
        for elemento in lista_canciones:
            if(nombref != elemento[0]):
                #print(frag,elemento[0])
                valmin=func.busqueda2(elemento[1],funFR)
                if(valmin < valmintotal):
                    res = elemento[0]
                    valmintotal=valmin
                    
    if(modo == '3'):
        espectograma = alg.extraer_espectograma(funFR, Fs)
        res = alg.identificar(espectograma,lista_canciones)
        
    if(modo == '4'):
        espectograma = alg.extraer_espectograma(funFR, Fs)
        res = alg.identificar2(espectograma,lista_canciones)

    d = {'fragment':nombref, "song" : res}
    datoscsv.update(d)
    df = df._append(d, ignore_index = True)
    #resultado.append(elemento)
df.to_csv("result.csv", index=False,encoding="utf-8")
print("--- %s seconds ---" % (time.time() - start_time))


#python3 PruebasPDS.py audios audios/fragmento.wav
#python3 PruebasPDS.py songs fragments/fragment_AAIA.wav
#Ejemplo AAIA es DASU
#python3 PruebasPDS.py songs2 fragments2

