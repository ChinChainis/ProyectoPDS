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




datoscsv = {
    'fragment': [],
    'song': []
}

resultado = []
umbral = 50
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
original = os.listdir(fragmento)
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
   

lista_de_listas = []

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
        
    espectograma = alg.extraer_espectograma(funOG, Fs)
    elemento =[nombre,espectograma]
    lista_de_listas.append(elemento)

resultado = []

df = pd.DataFrame(datoscsv)


for frag in original:
    nombref, extf = os.path.splitext(frag)
    #Si es .mp3, el array tiene dimensiones estéreo de x,2, lo necesitamos en mono
    if extf == ".mp3":
        print(carpeta + '/' + '{0}.mp3'.format(nombref))
        funFR ,Fs  = sf.read(fragmento + '/' + '{0}.mp3'.format(nombref))
        if(funFR.ndim>1):
           funFR = funFR.mean(axis=-1)    
    #En .wav no hay problema
    else:
        Fs, funFR = wavfile.read(fragmento + '/' + frag) #Fs frecuencia de 16000 hercios 
        
    espectograma = alg.extraer_espectograma(funFR, Fs)
    res = alg.identificar(espectograma,lista_de_listas)
    elemento = [frag,res]
    d = {'fragment':nombref, "song" : res}
    datoscsv.update(d)
    df = df._append(d, ignore_index = True)
    #resultado.append(elemento)
df.to_csv("result.csv", index=False,encoding="utf-8")


#python3 PruebasPDS.py audios audios/fragmento.wav
#python3 PruebasPDS.py songs fragments/fragment_AAIA.wav
#Ejemplo AAIA es DASU
#python3 PruebasPDS.py songs2 fragments2

