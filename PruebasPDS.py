#para activar anaconda $conda config --set auto_activate_base True
#y volver a abrir el terminal
import numpy as np
import pandas
import sys
import scipy as sc #procesamiento, para transformada fourier, interpolacion etc
from scipy.io import wavfile
import soundfile as sf
import os
import matplotlib.pyplot as plt
import math


umbral = 100000
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
    print("Valor minimo",valmin)
    return valmin
    #np.append(listavalmin,valmin/100)
    #print("lista total: ",listavalmin)
    
#lista de valores mínimos de cada canción de la carpeta a analizar
listavaldef = []
listanombres = []

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
        valmin = 1000000000
    print("Valor minimo",valmin)
    return valmin
   


for i in range(0,numarch):
    print(archivos[i],' Y ',fragmento[7:])

    nombre, ext = os.path.splitext(archivos[i])
    if ext == ".mp3":
       funOG ,Fs  = sf.read(carpeta + '/' + '{0}.mp3'.format(nombre))
       if(funOG.ndim>1):
            funOG = funOG.mean(axis=-1)    
    else:
        Fs, funOG = wavfile.read(carpeta + '/' + archivos[i]) #Fs frecuencia de 16000 hercios 

    Fs, funFR = wavfile.read(fragmento)
    print("tam",funOG.shape[0])
    nom = archivos[i]
    if(funOG.shape[0] >= funFR.shape[0]):
        if(archivos[i] != fragmento[7:]):
            valtemp = busqueda2(funOG,funFR)
            #Se añade valor mínimo de una canción concreta a la lista de valores mínimos de cada canción a comparar
            listavaldef.append(valtemp)
            print(listavaldef)
            listanombres.append(archivos[i])
        else:
            print('Es el mismo archivo: ',archivos[i],' y ',fragmento[7:])
    else:
        print('Fragmento más grande que la canción, no es posible')
valmintotaldef = listavaldef[np.argmin(listavaldef)]
nomcanciondef = 'NOT_FOUND'
if (valmintotaldef < umbral):
    #Como guarda la posición del valor mínimo, pues corresponderá a esa canción coincidente
    nomcanciondef = listanombres[np.argmin(listavaldef)]
    
print("Resultado: ",nomcanciondef, ". Valor: ",valmintotaldef)
#print(os.listdir("audios")[1])



#python3 PruebasPDS.py audios audios/fragmento.wav
