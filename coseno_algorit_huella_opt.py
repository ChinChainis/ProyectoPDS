# -*- coding: utf-8 -*-
"""
Created on Fri May  3 19:37:30 2024

@author: migue y cambiado por rub
"""

import numpy as np
import pandas as pd
import sys
import scipy as sc
from scipy.io import wavfile
import soundfile as sf
import os
import matplotlib.pyplot as plt
import scipy.signal as signal
from sklearn.metrics import accuracy_score

carpeta = "songs"
fragmentos = "fragments"

archivos = os.listdir(carpeta)
numarch = len(os.listdir(carpeta))
original = os.listdir(fragmentos)

datoscsv = {
    'fragment': [],
    'song': []
}

def extraer_espectograma(x, fs):
    x = x / np.max(np.abs(x))
    _, _, espectograma = signal.spectrogram(x, fs)
    espectograma = np.mean(espectograma, axis=1)
    return espectograma

def identificar(espectograma, lista, umbral):
    similitud = 0.0
    cancion = None
    
    for elemento in lista:
        punto_producto = np.dot(espectograma, elemento[1])
        magnitud_A = np.linalg.norm(espectograma)
        magnitud_B = np.linalg.norm(elemento[1])
        coseno_similaridad = punto_producto / (magnitud_A * magnitud_B)
        
        if coseno_similaridad > similitud:
            similitud = coseno_similaridad
            cancion = elemento[0]
    
    if similitud > umbral:
        return cancion
    else:
        return "NOT_FOUND"

def calcular_tasa_error(umbral):
    print(f"Calculando tasa de error para umbral: {umbral}")
    
    lista_de_listas = []
    df = pd.DataFrame(datoscsv)

    for i in range(0, numarch):
        nombre, ext = os.path.splitext(archivos[i])
        if ext == ".mp3":
            funOG, Fs = sf.read(carpeta + '/' + '{0}.mp3'.format(nombre))
            if funOG.ndim > 1:
                funOG = funOG.mean(axis=-1)
        else:
            Fs, funOG = wavfile.read(carpeta + '/' + archivos[i])
        
        espectograma = extraer_espectograma(funOG, Fs)
        elemento = [archivos[i], espectograma]
        lista_de_listas.append(elemento)

    archivos2 = os.listdir(fragmentos)
    numarch2 = len(os.listdir(fragmentos))
    datoscsv_temp = {
        'fragment': [],
        'song': []
    }

    for i, frag in enumerate(original):
        nombref, extf = os.path.splitext(frag)
        Fs, funFR = wavfile.read(fragmentos + '/' + archivos2[i])
        espectograma = extraer_espectograma(funFR, Fs)
        res = identificar(espectograma, lista_de_listas, umbral)
        nombreres, extres = os.path.splitext(res)
        d = {'fragment': nombref, "song": nombreres}
        datoscsv_temp['fragment'].append(nombref)
        datoscsv_temp['song'].append(nombreres)

    df_temp = pd.DataFrame(datoscsv_temp)
    df_temp.to_csv("result_temp.csv", index=False, encoding="utf-8")

    error_rate, _ = calculate_error_rate('fragments.csv', 'result_temp.csv', 'relative')
    print(f"Tasa de error para umbral {umbral}: {error_rate * 100:.2f}%")
    return error_rate

def custom_confusion_matrix(ground_truth, predicted, confusion_matrix_type='relative'):
    confusion_matrix = np.zeros(5)
    confusion_matrix[0] = np.sum((ground_truth == predicted) & (ground_truth.str.startswith('song_')))
    confusion_matrix[1] = np.sum((ground_truth == predicted) & (ground_truth == 'NOT_FOUND'))
    confusion_matrix[2] = np.sum((ground_truth.str.startswith('song_')) & (predicted.str.startswith('song_')) & (ground_truth != predicted))
    confusion_matrix[3] = np.sum((ground_truth.str.startswith('song_')) & (predicted == 'NOT_FOUND'))
    confusion_matrix[4] = np.sum((ground_truth == 'NOT_FOUND') & (predicted.str.startswith('song_')))

    if confusion_matrix_type == 'relative':
        num_fragment_songs = np.sum(ground_truth.str.startswith('song_'))
        num_fragment_nf = np.sum(ground_truth == 'NOT_FOUND')
        norm_factor = np.zeros(5)
        norm_factor[0] = num_fragment_songs
        norm_factor[1] = num_fragment_nf
        norm_factor[2] = num_fragment_songs
        norm_factor[3] = num_fragment_songs
        norm_factor[4] = num_fragment_nf
    else:
        norm_factor = len(ground_truth)

    return (100.0 * confusion_matrix) / norm_factor

def calculate_error_rate(ground_truth_file, results_file, confusion_matrix_type='relative'):
    ground_truth_df = pd.read_csv(ground_truth_file)
    results_df = pd.read_csv(results_file)

    merged_df = pd.merge(ground_truth_df, results_df, on='fragment', suffixes=('_truth', '_predicted'))
    error_rate = 1 - accuracy_score(merged_df['song_truth'], merged_df['song_predicted'])
    confusion = custom_confusion_matrix(merged_df['song_truth'], merged_df['song_predicted'], confusion_matrix_type)
    confusion_matrix = pd.DataFrame(confusion, columns=['Percentage'])
    confusion_matrix.index = ['Correct (Song->Song)', 'Correct (NF->NF)', 'Incorrect (Song->Song)', 'Incorrect (Song->NF)', 'Incorrect (NF->Song)']

    return error_rate, confusion_matrix

def optimizar_umbral():
    umbrales = np.linspace(0.8, 0.99, 9)
    mejor_umbral = 0
    menor_error = float('inf')

    total_umbrales = len(umbrales)
    print(f"Total de umbrales a probar: {total_umbrales}")

    for idx, umbral in enumerate(umbrales):
        print(f"Probando umbral {idx + 1}/{total_umbrales} ({umbral:.2f})")
        error = calcular_tasa_error(umbral)
        print(f"Tasa de error con umbral {umbral:.2f}: {error * 100:.2f}%")
        if error < menor_error:
            menor_error = error
            mejor_umbral = umbral
    
    print(f"Mejor umbral encontrado: {mejor_umbral} con una tasa de error de {menor_error * 100:.2f}%")
    return mejor_umbral, menor_error

mejor_umbral, menor_error = optimizar_umbral()
print(f"Mejor umbral final: {mejor_umbral}")
print(f"Menor tasa de error final: {menor_error * 100:.2f}%")

GROUND_TRUTH_FILE = 'fragments.csv'
RESULTS_FILE = 'result_temp.csv'

error_rate, confusion_df = calculate_error_rate(GROUND_TRUTH_FILE, RESULTS_FILE, 'relative')
print(f"TASA DE ERROR: {100 * error_rate:.2f}%")
print("RESULTADOS GLOBALES: ", confusion_df)

confusion_df.plot.bar(legend=False)
plt.title('Resultados globales', fontsize=16)
plt.ylabel('%', fontsize=14)
plt.xticks(rotation=0, fontsize=6)
plt.yticks(fontsize=12)
plt.ylim(0, 100)
plt.tight_layout()
plt.show()

#El mejor umbral encontrado es 0.895 con una tasa de error de 64.60%
#He probado distintas formas de optmizarlo pero todas eran peores que esta
#Desde cambiar la forma en la que se hacen las medias hasta cambiar la forma en la que se calcula la similitud
#también formas de calcular el espectograma y valores de la ventana