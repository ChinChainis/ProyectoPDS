import numpy as np
import pandas as pd
import sys
import scipy as sc #procesamiento, para transformada fourier, interpolacion etc
from scipy import signal
from scipy.io import wavfile
import soundfile as sf
import os
import matplotlib.pyplot as plt
import math
import algorit_huella_prueba as alg
from scipy.spatial.distance import euclidean

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
   
   
def decode_dtmf(seg, Fs):
    dur_segmento=0.5
    seg = seg.astype(float)
    
    # Guardamos las frecuencias
    filtered_freqs = []

    # Se mueve cada 4000 elementos (un tono son 4000 elementos y 4000 de sonido)
    #for i in range(0, len(seg), int(Fs*dur_segmento)):
    #    # Trozo a analizar
    #    cut_sig = seg[i:i+int(Fs*dur_segmento)]

        # FFT
    #    fft_sig = np.fft.rfft(cut_sig, Fs)
    #    fft_sig = np.abs(fft_sig)

    #    freq_max_seg = np.max(fft_sig)        
    #    filtered_freqs.append(freq_max_seg)
        
    N = len(seg)

    fft = np.fft.rfft(seg)

    transform_y = 2.0 / N * np.abs(fft[0:N//2])    
    #maxfreq = np.max(filtered_freqs)
    #norm_freqs = filtered_freqs / maxfreq
    all_peaks, props = signal.find_peaks(transform_y)

    peaks, props = signal.find_peaks(transform_y, prominence=0, distance=10000)

    n_peaks = 8

    # Get the n_peaks largest peaks from the prominences

    # This is an argpartition

    # Useful explanation: https://kanoki.org/2020/01/14/find-k-smallest-and-largest-values-and-its-indices-in-a-numpy-array/

    largest_peaks_indices = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]

    largest_peaks = peaks[largest_peaks_indices]
    
    print(len(largest_peaks))
    print('frecuencias canción cada 0.5s: ', largest_peaks)
    return largest_peaks



def create_constellation(audio, Fs):

    # Parameters

    window_length_seconds = 0.5

    window_length_samples = int(window_length_seconds * Fs)

    window_length_samples += window_length_samples % 2

    num_peaks = 10

    # Pad the song to divide evenly into windows

    amount_to_pad = window_length_samples - audio.size % window_length_samples

    song_input = np.pad(audio, (0, amount_to_pad))

    # Perform a short time fourier transform

    frequencies, times, stft = signal.stft(

        song_input, Fs, nperseg=window_length_samples, nfft=window_length_samples, return_onesided=True

    )

    constellation_map = []

    for time_idx, window in enumerate(stft.T):

        # Spectrum is by default complex. 

        # We want real values only

        spectrum = abs(window)

        # Find peaks - these correspond to interesting features

        # Note the distance - want an even spread across the spectrum

        peaks, props = signal.find_peaks(spectrum, prominence=0, distance=200)

        # Only want the most prominent peaks

        # With a maximum of 15 per time slice

        n_peaks = min(num_peaks, len(peaks))

        # Get the n_peaks largest peaks from the prominences

        # This is an argpartition

        # Useful explanation: https://kanoki.org/2020/01/14/find-k-smallest-and-largest-values-and-its-indices-in-a-numpy-array/

        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]

        for peak in peaks[largest_peaks]:

            frequency = frequencies[peak]

            constellation_map.append([time_idx, frequency])

    print(constellation_map)
    return constellation_map

def comparar(frag, lista):
    distancia_min = float('inf')
    cancion = None
    pos = None
    
    for elemento in lista:
        len(elemento[1])
        # Calcula la distancia euclidiana entre las huellas digitales
        #for i in range(0,len(elemento[1]),len(frag)):
        for i in range(0,len(elemento[1]) - len(frag)):

            can_trim_actual=elemento[1][i:i+len(frag)]
            distancia = euclidean(frag,can_trim_actual)
            #print(distancia)
            # Actualiza la canción identificada si la distancia es menor que el mínimo
            if distancia < distancia_min:
                distancia_min = distancia
                cancion = elemento[0]

        print("DM: ",distancia_min)
        cancion = elemento[0]
    
    #Umbral de corte
    umbral = 0.5
    print("canc: ",cancion)
    # Si la distancia mínima está por debajo del umbral, considera que es la misma canción
    if distancia_min < umbral:
        return cancion
    else:
        return "NOT_FOUND"
    
