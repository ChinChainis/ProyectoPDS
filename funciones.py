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
    
    
    
def busqueda1(fun1,fun2):
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
    
def busqueda12(fun1,fun2):
    #buscar en fun1 donde coincida el primer valor
    #Cuando coincida empezar comparación y anotar error en lista
    #He puesto un valor  temporal de error de 1000000000 por si no encuentra un valor similar, 
    #este debería ser como el umbral
    #mismo proceso que antes, seleccionar la canción con menor error
    listavalores =[]
    sumerror=0
    for i in range(0,fun1.shape[0]):
        if(fun1.shape[0]-i > fun2.shape[0]):
            recorref1 = fun1[i:fun2.shape[0]+i]
            restaarrays = np.int64(np.subtract(fun2,recorref1))
            potarrays = np.power(restaarrays,2)
            sumerror = np.sum(potarrays)
            listavalores.append(sumerror)
            sumerror = 0
    if(listavalores != []):
        valmin = np.min(listavalores)
    else:
        valmin = umbral
    #print("Valor minimo",valmin)
    return valmin
    
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
        valmin = np.min(listavalores)
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
    
    #print(len(largest_peaks))
    #print('frecuencias canción cada 0.5s: ', largest_peaks)
    return largest_peaks

def comparar(frag, lista):
    distancia_min = float('inf')
    cancion = None
    pos = None
    
    for elemento in lista:
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

        #print("DM: ",distancia_min)
        cancion = elemento[0]
    
    #Umbral de corte
    umbral = 0.5
    #print("canc: ",cancion)
    # Si la distancia mínima está por debajo del umbral, considera que es la misma canción
    if distancia_min < umbral:
        return cancion
    else:
        return "NOT_FOUND"
    

def create_constellation(audio, Fs):

    dur_segmento = 0.5
    #44100*0.5=22050 digitos por array
    window_length_samples = int(dur_segmento * Fs)
    window_length_samples += window_length_samples % 2

    num_picos = 10

    #Dividir la canción en segmentos de igual tamaño según el tiempo especificado

    divisiones = window_length_samples - audio.size % window_length_samples

    #rellena el array de la canción con 0
    song_input = np.pad(audio, (0, divisiones))

    #Transformada de fourier en tiempo discreto según 
    # el array padeado de antes, la frecuencia y las ventanas de tiempo del principio de la función
    frequencias, times, stft = signal.stft(song_input, Fs, nperseg=window_length_samples, nfft=window_length_samples, return_onesided=True)

    #Aquí contredremos la constelación que es el agrupamiento de las frecuencias extraidas de una canción, 
    #solo cogeremos un número reducido de picos para analizar
    constellation_map = []

    for time_idx, window in enumerate(stft.T):

        #Solo valores reales del espectro

        spectrum = abs(window)

        #picos son las frecuencias mayores encontradas en una distancia especificada
        picos, props = signal.find_peaks(spectrum, prominence=0, distance=200)
        n_picos = min(num_picos, len(picos))

        #Obtener los n mayores picos de la secuencia cada 10 picos como mínimo

        largest_peaks = np.argpartition(props["prominences"], -n_picos)[-n_picos:]

        for pico in picos[largest_peaks]:
            freq = frequencias[pico]
            #generamos constelación
            constellation_map.append([time_idx, freq])

    #print('aa',constellation_map)
    return constellation_map

def create_hashes(constellation_map, song_id=None):
    hashes = {}
    #la frecuencia de las canciones es 44,1 KHz pero ponemos un poco más para tener un poco de offset
    upper_frequency = 44_200
    frequency_bits = 10
    
    #Recorremos la constelación dada siendo idx el nombre, time el segundo y freq la frencuencia en ese punto
    for idx, (time, freq) in enumerate(constellation_map):
        # Compara cada 100 valores de la constelación
        for other_time, other_freq in constellation_map[idx : idx + 100]:
            diff = other_time - time
            # Si la diferencia de tiempo es muy grande obvia este emparejamiento
            if diff <= 1 or diff > 10:
                continue

            #Coloca las frecuencias en hercios en 'contenedores' de 1024bits
            freq_binned = freq / upper_frequency * (2 ** frequency_bits)
            other_freq_binned = other_freq / upper_frequency * (2 ** frequency_bits)

            #Y ahora hacemos los hash de 32 bits, la database queda un poco grande pero solo hay que hacerla una vez
            hash = int(freq_binned) | (int(other_freq_binned) << 10) | (int(diff) << 20)
            hashes[hash] = (time, song_id)
    return hashes


def comparar2(hashes,database):
    matches_por_canc = {}
    #recorremos los hashes y vemos las coincidencias y creamos una nueva lista de coincidencias con canciones, 
    #para luego concretar cuál es el mejor matching
    for hash, (sample_time, _) in hashes.items():
        if hash in database:
            matching_occurences = database[hash]
            for source_time, song_index in matching_occurences:
                if song_index not in matches_por_canc:
                    matches_por_canc[song_index] = []
                matches_por_canc[song_index].append((hash, sample_time, source_time))

    #lista de puntuaciones
    puntuaciones = {}
    #puntuación máxima --> nos servirá de umbral
    #0 -> 5.2%
    #250 -> 2.5%
    #300 -> 2.1%
    #350 -> 2.6%
    #500 -> 4.7%
    #1000 ->17.20%
    punt_max = 300
    #nombre de la canción ganadora --> lo igualamos a NOT_FOUND por defecto
    res_cancion = "NOT_FOUND"
    #song_index es el nombre de la canción
    for song_index, matches in matches_por_canc.items():
        puntuaciones_por_offset = {}
        for hash, sample_time, source_time in matches:
            #vemos la diferencia de tiempo para escoger las frecuencias que encajen
            delta = source_time - sample_time
            if delta not in puntuaciones_por_offset:
                puntuaciones_por_offset[delta] = 0
            #empezamos a añadir el valor de puntuación
            puntuaciones_por_offset[delta] += 1

        max = (0, 0)
        #seleccionamos la puntuación máxima
        for offset, score in puntuaciones_por_offset.items():
            if score > max[1]:
                max = (offset, score)
        
        puntuaciones[song_index] = max
        if (punt_max < max[1]):
            punt_max = max[1]
            res_cancion = song_index
    
    return res_cancion