#para activar anaconda $conda config --set auto_activate_base True
#y volver a abrir el terminal
import numpy as np
import pandas
import sys
import scipy as sc #procesamiento, para transformada fourier, interpolacion etc
from scipy.io import wavfile
import soundfile as sf
import os
import pydub as pd #se usa para tener la función de transformar mp3 en wav
import matplotlib.pyplot as plt
import math

#a = open("test.txt")
#print(a.read())

#b = sys.argv
carpeta = sys.argv[1]
fragmento = sys.argv[2]
valmintotal = 0

#a = open(c)

#print(c)
#dst_path = "test.wav"
#cwav = pd.AudioSegment.from_file(c)
#cwav.export(dst_path,format="wav")


#ej, samplerate = sf.read(c)
archivos = os.listdir(carpeta)
numarch = len(os.listdir(carpeta))

print(numarch)

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
    print(fun1.shape[0] / fun2.shape[0])
    #recorref1 array de tamaño del fragmento para reducir tamaño de comparación
    recorref1 = np.zeros(fun2.shape[0])
    print(fun1.shape[0]-fun2.shape[0])
    #el bucle va desde el principio de la canción (0) hasta el final menos el tamaño del fragmento, dado que comparamos en trozos
    #del tamaño de fragmentos pues acabaría terminando en 32000 |_32000_|_32000_|_32000_|
    for i in range(0, fun1.shape[0]-fun2.shape[0]):
        #recorref1 empieza de 0 hasta el tamaño del fragmento 2, si es 32000 es un vector del 0 al 31999
        recorref1 = fun1[i:fun2.shape[0]+i]
        #resta todos los elementos de ambos arrays
        restaarrays = np.subtract(fun2,recorref1)
        #eleva cada elemento de los arrays a potencia de 2
        potarrays = np.power(restaarrays,2)
        #obtiene la sumatoria de todos los elementos del array
        sumerror = np.sum(potarrays)
        #for pos in range(0,fun2.shape[0]):
            #sumatoria
            #sumerror += (fun2[pos] - recorref1[pos])**2
        #print(sumerror)
        if (valmin==0): 
            valmin = sumerror
        if (sumerror < valmin):
            valmin = sumerror
        #print("valmin: ",valmin)
            #print("Val min actual: ",sumerror)
        sumerror = 0
    print("Valor minimo",valmin)
    return valmin
    #np.append(listavalmin,valmin/100)
    #print("lista total: ",listavalmin)
    

for i in range(0,numarch-1):
    print(archivos[i])
    Fs, funOG = wavfile.read(carpeta + '/' + archivos[i]) #Fs frecuencia de 16000 hercios 
    Fs, funFR = wavfile.read(fragmento)
    nomcancion = ""
    valtemp = comparar(funOG,funFR)
    if(valmintotal==0):
        nomcancion = "Canción: "+archivos[i]
        valmintotal=valtemp
    elif(valtemp < valmintotal):
        nomcancion = "Canción: "+archivos[i]
        valmintotal=valtemp

print("Canción coincidente: ",nomcancion, ". Valor: ",valmintotal)
#print(os.listdir("audios")[1])


