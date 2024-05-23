import numpy as np
import pandas as pd
import os
import time
from scipy.io import wavfile
import soundfile as sf
from python_speech_features import mfcc
from scipy.spatial.distance import euclidean
from concurrent.futures import ProcessPoolExecutor, as_completed
import pickle

def calcular_mfcc(audio, sample_rate, num_ceps=13, hop_length=512):
    mfcc_feat = mfcc(audio, sample_rate, numcep=num_ceps, winstep=hop_length / sample_rate)
    return mfcc_feat

def comparar_mfcc(mfcc1, mfcc2):
    min_len = min(len(mfcc1), len(mfcc2))
    mfcc1 = mfcc1[:min_len]
    mfcc2 = mfcc2[:min_len]
    error = np.sum([euclidean(mfcc1[i], mfcc2[i]) for i in range(min_len)])
    return error

def leer_audio(file_path):
    if file_path.endswith('.mp3'):
        audio, sample_rate = sf.read(file_path)
    else:
        sample_rate, audio = wavfile.read(file_path)
    if audio.ndim > 1:
        audio = audio.mean(axis=-1)  # Convertir a mono si es estéreo
    return audio, sample_rate

def procesar_combinacion(archivo_fragmento, archivo_cancion, carpeta_fragmentos, carpeta_canciones, umbral, mfcc_canciones_cache):
    resultados = []
    frag_path = os.path.join(carpeta_fragmentos, archivo_fragmento)
    funFR, Fs_frag = leer_audio(frag_path)
    mfccFR = calcular_mfcc(funFR, Fs_frag)

    if archivo_cancion in mfcc_canciones_cache:
        mfcc_cancion, Fs = mfcc_canciones_cache[archivo_cancion]
    else:
        cancion_path = os.path.join(carpeta_canciones, archivo_cancion)
        audio, Fs = leer_audio(cancion_path)
        mfcc_cancion = calcular_mfcc(audio, Fs)
        mfcc_canciones_cache[archivo_cancion] = (mfcc_cancion, Fs)

    mejor_disparidad = float('inf')
    mejor_segmento = None

    ventana_tamaño = len(mfccFR)
    ventana_paso = Fs // 5  # Desplazamiento de 0.2 segundos

    for i in range(0, len(mfcc_cancion) - ventana_tamaño, ventana_paso):
        segmento_mfcc = mfcc_cancion[i:i + ventana_tamaño]
        val_disparidad = comparar_mfcc(mfccFR, segmento_mfcc)
        if val_disparidad < mejor_disparidad:
            mejor_disparidad = val_disparidad
            mejor_segmento = segmento_mfcc

    if mejor_segmento is not None and mejor_disparidad < umbral:
        resultados.append((archivo_cancion, archivo_fragmento, mejor_disparidad))
    else:
        resultados.append(("NOT_FOUND", archivo_fragmento, mejor_disparidad))

    return resultados

def main():
    start_time = time.time()
    print("Iniciando comparación de fragmentos de audio...")

    umbral = 20400
    carpeta_canciones = "songs"
    carpeta_fragmentos = "fragments2"

    datoscsv = {'Canción': [], 'Fragmento': [], 'Valor disparidad': []}
    mfcc_canciones_cache = {}

    archivos_fragmentos = [f for f in os.listdir(carpeta_fragmentos) if f.endswith('.wav')]
    archivos_canciones = [f for f in os.listdir(carpeta_canciones) if f.endswith(('.mp3', '.wav'))]

    # Precalcular y guardar los MFCC de todas las canciones
    for archivo_cancion in archivos_canciones:
        cancion_path = os.path.join(carpeta_canciones, archivo_cancion)
        audio, Fs = leer_audio(cancion_path)
        mfcc_cancion = calcular_mfcc(audio, Fs)
        mfcc_canciones_cache[archivo_cancion] = (mfcc_cancion, Fs)

    # Guardar los MFCC precalculados en un archivo para uso futuro
    with open("mfcc_canciones_cache.pkl", "wb") as f:
        pickle.dump(mfcc_canciones_cache, f)

    # Paralelización del procesamiento de fragmentos
    with ProcessPoolExecutor() as executor:
        futuros = []
        for archivo_fragmento in archivos_fragmentos:
            print(f"Procesando fragmento {archivo_fragmento}...")
            for archivo_cancion in archivos_canciones:
                futuros.append(executor.submit(procesar_combinacion, archivo_fragmento, archivo_cancion, carpeta_fragmentos, carpeta_canciones, umbral, mfcc_canciones_cache))

        for futuro in as_completed(futuros):
            resultado = futuro.result()
            if resultado:
                for archivo_cancion, archivo_fragmento, val_disparidad in resultado:
                    datoscsv['Canción'].append(archivo_cancion)
                    datoscsv['Fragmento'].append(archivo_fragmento)
                    datoscsv['Valor disparidad'].append(val_disparidad)

    df = pd.DataFrame(datoscsv)

    fragmentos_unicos = df['Fragmento'].unique()
    resultados_probables = {'Fragmento': [], 'Canción Probable': [], 'Valor disparidad': []}

    for fragmento in fragmentos_unicos:
        df_fragmento = df[df['Fragmento'] == fragmento]
        cancion_probable = df_fragmento.loc[df_fragmento['Valor disparidad'].idxmin()]
        resultados_probables['Fragmento'].append(fragmento)
        resultados_probables['Canción Probable'].append(cancion_probable['Canción'])
        resultados_probables['Valor disparidad'].append(cancion_probable['Valor disparidad'])

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time} segundos.")

    df_final = pd.DataFrame(resultados_probables)
    df_final.to_csv("result_dist.csv", index=False, encoding="utf-8")

    print("Comparaciones completadas y resultados guardados en 'result_dist.csv'.")

if __name__ == "__main__":
    main()
