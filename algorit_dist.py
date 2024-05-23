import numpy as np
import pandas as pd
import sys
from scipy.io import wavfile
import soundfile as sf
import os
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import time
start_time = time.time()

# Función para calcular el espectrograma usando la Transformada de Fourier
def calcular_espectrograma(audio, sample_rate, n_fft=2048, hop_length=512):
    espectrograma = np.abs(np.fft.rfft(audio, n=n_fft))
    return espectrograma

# Función para comparar dos espectrogramas
def comparar_espectrogramas(espectro1, espectro2):
    min_len = min(len(espectro1), len(espectro2))
    espectro1 = espectro1[:min_len]
    espectro2 = espectro2[:min_len]
    error = np.sum((espectro1 - espectro2) ** 2)
    return error

# Función para procesar una combinación de fragmento y canción
def procesar_combinacion(archivo_fragmento, archivo_cancion, carpeta_fragmentos, carpeta_canciones, umbral):
    resultados = []
    Fs_frag, funFR = wavfile.read(os.path.join(carpeta_fragmentos, archivo_fragmento))
    if funFR.ndim > 1:
        funFR = funFR.mean(axis=-1)  # Convertir a mono si es estéreo
    espectroFR = calcular_espectrograma(funFR, Fs_frag)

    nombre, ext = os.path.splitext(archivo_cancion)
    if ext == ".mp3" or ext == ".wav":
        # Leer archivo de audio
        if ext == ".mp3":
            audio, Fs = sf.read(os.path.join(carpeta_canciones, archivo_cancion))
            if audio.ndim > 1:
                audio = audio.mean(axis=-1)  # Convertir a mono si es estéreo
        else:
            Fs, audio = wavfile.read(os.path.join(carpeta_canciones, archivo_cancion))

        # Solo procesar si la canción es más larga que el fragmento
        if len(audio) >= len(funFR):
            espectroOG = calcular_espectrograma(audio, Fs)
            val_disparidad = comparar_espectrogramas(espectroOG, espectroFR)
            resultados.append((archivo_cancion, archivo_fragmento, val_disparidad))

    return resultados

def main():
    # Parámetros
    umbral = 1000
    carpeta_canciones = "songs"
    carpeta_fragmentos = "fragments2"

    # Preparar el dataframe para los resultados
    datoscsv = {'Canción': [], 'Fragmento': [], 'Valor disparidad': []}

    # Procesar cada archivo en la carpeta de fragmentos y canciones en paralelo
    archivos_fragmentos = [f for f in os.listdir(carpeta_fragmentos) if f.endswith('.wav')]
    archivos_canciones = [f for f in os.listdir(carpeta_canciones) if f.endswith(('.mp3', '.wav'))]

    with ProcessPoolExecutor() as executor:
        futuros = []
        for archivo_fragmento in archivos_fragmentos:
            for archivo_cancion in archivos_canciones:
                futuros.append(executor.submit(procesar_combinacion, archivo_fragmento, archivo_cancion, carpeta_fragmentos, carpeta_canciones, umbral))

        for futuro in concurrent.futures.as_completed(futuros):
            resultado = futuro.result()
            if resultado:
                for archivo_cancion, archivo_fragmento, val_disparidad in resultado:
                    datoscsv['Canción'].append(archivo_cancion)
                    datoscsv['Fragmento'].append(archivo_fragmento)
                    datoscsv['Valor disparidad'].append(val_disparidad)

    # Crear el dataframe
    df = pd.DataFrame(datoscsv)

    # Encontrar la canción más probable para cada fragmento
    fragmentos_unicos = df['Fragmento'].unique()
    resultados_probables = {'Fragmento': [], 'Canción Probable': [], 'Valor disparidad': []}

    for fragmento in fragmentos_unicos:
        df_fragmento = df[df['Fragmento'] == fragmento]
        cancion_probable = df_fragmento.loc[df_fragmento['Valor disparidad'].idxmin()]
        resultados_probables['Fragmento'].append(fragmento)
        resultados_probables['Canción Probable'].append(cancion_probable['Canción'])
        resultados_probables['Valor disparidad'].append(cancion_probable['Valor disparidad'])

    # Crear el dataframe final y guardar los resultados en un archivo CSV
    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time} segundos.")

    df_final = pd.DataFrame(resultados_probables)
    df_final.to_csv("result_dist.csv", index=False, encoding="utf-8")

    

    print("Comparaciones completadas y resultados guardados en 'result1.csv'.")
    

if __name__ == '__main__':
    main()
