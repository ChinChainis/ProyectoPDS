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

umbral = 50


def representar(fun1,fun2):
    fig, (ax, ax2) = plt.subplots(1,2)

    x = np.linspace(0, 1, fun1.shape[0])
    x2 = np.linspace(0, 1, 32000)
    ax.plot(x,fun1, label="Funcion Cancion")
    ax2.plot(x2,fun2, label="Funcion Fragmento",  color="Green")

    ax.axis([0,1,0,30000])
    ax2.axis([0,1,0,30000])

    ax.legend(loc=0)
    ax2.legend(loc=0)
    
    plt.show()
    
    
    
def comparar(fun1,fun2):
    #fun1 canción a comparar, fun2 fragmento que comparamos
    sumerror = 0
    #sumerror sumatoria del algoritmo básico
    pos = 0
    #valor mínimo actual, indicaría qué canción tiene el menos error de comparación
    valmin = 0
    #Indica el número de veces que es de grande la canción en comparación con el fragmento
    #print(fun1.shape[0] / fun2.shape[0])
    #recorref1 array de tamaño del fragmento para reducir tamaño de comparación
    recorref1 = np.zeros(fun2.shape[0])
    #print(fun1.shape[0]-fun2.shape[0])
    #lista total de los valores obtenidos de recorrer una canción, se escoje el mínimo. 
    #En teoría si es la misma canción el mínimo es 0
    listavalores = np.zeros(fun1.shape[0]-fun2.shape[0])
    #el bucle va desde el principio de la canción (0) hasta el final menos el tamaño del fragmento, dado que comparamos en trozos
    #del tamaño de fragmentos pues acabaría terminando en 32000 |_32000_|_32000_|_32000_|
    for i in range(0, fun1.shape[0]-fun2.shape[0]):
        #recorref1 empieza de 0 hasta el tamaño del fragmento 2, si es 32000 es un vector del 0 al 31999
        recorref1 = fun1[i:fun2.shape[0]+i]
        #resta todos los elementos de ambos arrays
        restaarrays = np.int64(np.subtract(fun2,recorref1))
        #eleva cada elemento de los arrays a potencia de 2
        potarrays = np.power(restaarrays,2)
        #obtiene la sumatoria de todos los elementos del array
        sumerror = np.sum(potarrays)
        listavalores[i]=sumerror
        sumerror = 0
    #print('lista',listavalores)
    #Sacamos el valor mínimo obtenido de recorrer la canción
    valmin = listavalores[np.argmin(listavalores)]
    #print("Valor minimo",valmin)
    return valmin
    #np.append(listavalmin,valmin/100)
    #print("lista total: ",listavalmin)
    
    
def busqueda2(fun1,fun2):
    #buscar en fun1 donde coincida el primer valor
    #Cuando coincida empezar comparación y anotar error en lista
    #He puesto un valor  temporal de error de 1000000000 por si no encuentra un valor similar, 
    #este debería ser como el umbral
    #mismo proceso que antes, seleccionar la canción con menor error
    
    valorini = fun2[0]
    listavalores =[]
    sumerror=0
    for i in range(0,fun1.shape[0]):
        if(fun1[i] == valorini):
            if(fun1.shape[0]-i > fun2.shape[0]):
                recorref1 = fun1[i:fun2.shape[0]+i]
                restaarrays = np.int64(np.subtract(fun2,recorref1))
                potarrays = np.power(restaarrays,2)
                sumerror = np.sum(potarrays)
                listavalores.append(sumerror)
                sumerror = 0
    if(listavalores != []):
        valmin = listavalores[np.argmin(listavalores)]
    else:
        valmin = umbral
    #print("Valor minimo",valmin)
    return valmin
   