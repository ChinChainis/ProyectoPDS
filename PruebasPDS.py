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
    error=0
    sumerror = 0
    pos = 0
    valmin = 0
    listavalmin = 0
    print(fun1.shape[0] / fun2.shape[0])
    for i in range(0, fun1.shape[0]):
        sumerror += math.sqrt( (fun2[pos] - fun1[i])**2 )
        if (pos == fun2.shape[0]-1):
            #print("fun2 pos",fun2[pos])
            #print("fun1 i",fun1[i])
            #print("sumerror uni",(fun2[pos] - fun1[i])**2)
            if (valmin==0):
                valmin = sumerror
            if (sumerror < valmin):
                valmin = sumerror
            print("Val min actual: ",sumerror)
            sumerror = 0
            pos = 0
        else:
            pos+=1
    print("Valor minimo",valmin)
    np.append(listavalmin,valmin/100)
    print("lista total: ",listavalmin)
    

for i in range(0,numarch-1):
    print(archivos[i])
    Fs, funOG = wavfile.read(carpeta + '/' + archivos[i]) #Fs frecuencia de 16000 hercios 
    Fs, funFR = wavfile.read(fragmento)

    comparar(funOG,funFR)


#print(os.listdir("audios")[1])


