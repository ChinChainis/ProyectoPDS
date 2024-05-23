import numpy as np
import pandas as pd
import sys
from scipy.io import wavfile
import soundfile as sf
import os
from scipy.ndimage import maximum_filter
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures
from collections import defaultdict
import time

start_time = time.time()

# Función para calcular el espectrograma usando la Transformada de Fourier
def calcular_espectrograma(audio, sample_rate, n_fft=4096, hop_length=512):
    espectrograma = np.abs(np.fft.rfft(audio, n=n_fft, axis=0))
    espectrograma = np.log1p(espectrograma)  # Escalado logarítmico para mayor claridad

    # Asegúrate de que 'espectrograma' es un array 2D
    if espectrograma.ndim == 1:
        espectrograma = np.expand_dims(espectrograma, axis=1)

    return espectrograma

# Función para detectar picos en el espectrograma
def detectar_picos(espectrograma, amp_min):
    # Asegúrate de que 'espectrograma' es un array 2D
    if espectrograma.ndim != 2:
        raise ValueError(f"Espectrograma debe ser un array 2D, pero tiene {espectrograma.ndim} dimensiones")

    maxima = maximum_filter(espectrograma, size=(3, 3)) == espectrograma
    detected_peaks = maxima & (espectrograma > amp_min)
    j, i = np.where(detected_peaks)
    peaks = list(zip(i, j, espectrograma[detected_peaks]))
    return peaks

# Función para generar huellas digitales
def generar_huellas(peaks, fan_value=15):
    hash_list = []
    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):
                freq1 = peaks[i][1]
                freq2 = peaks[i + j][1]
                t1 = peaks[i][0]
                t2 = peaks[i + j][0]
                t_delta = t2 - t1
                if t_delta <= 200:
                    hash_list.append((freq1, freq2, t_delta, t1))
    return hash_list

# Función para comparar huellas digitales
def comparar_huellas(hashes1, hashes2):
    hash_dict = defaultdict(int)
    for hash in hashes1:
        hash_dict[hash[:3]] += 1
    matches = sum([hash_dict[hash[:3]] for hash in hashes2])
    return matches

# Función para procesar una combinación de fragmento y canción
def procesar_combinacion(archivo_fragmento, archivo_cancion, carpeta_fragmentos, carpeta_canciones, amp_min):
    resultados = []
    Fs_frag, funFR = wavfile.read(os.path.join(carpeta_fragmentos, archivo_fragmento))
    if funFR.ndim > 1:
        funFR = funFR.mean(axis=-1)  # Convertir a mono si es estéreo
    espectroFR = calcular_espectrograma(funFR, Fs_frag)
    peaksFR = detectar_picos(espectroFR, amp_min)
    huellasFR = generar_huellas(peaksFR)

    nombre, ext = os.path.splitext(archivo_cancion)
    if ext == ".mp3" or ext == ".wav":
        # Leer archivo de audio
        if ext == ".mp3":
            audio, Fs = sf.read(os.path.join(carpeta_canciones, archivo_cancion))
            if audio.ndim > 1:
                audio = audio.mean(axis=-1)  # Convertir a mono si es estéreo
        else:
            Fs, audio = wavfile.read(os.path.join(carpeta_canciones, archivo_cancion))

        if len(audio) >= len(funFR):
            espectroOG = calcular_espectrograma(audio, Fs)
            peaksOG = detectar_picos(espectroOG, amp_min)
            huellasOG = generar_huellas(peaksOG)

            val_disparidad = comparar_huellas(huellasFR, huellasOG)
            resultados.append((archivo_cancion, archivo_fragmento, val_disparidad))

    return resultados

def main():
    # Parámetros
    umbral = 1000
    amp_min = 10  # umbral de amplitud para los picos
    carpeta_canciones = "songs"
    carpeta_fragmentos = "fragments"

    # Preparar el dataframe para los resultados
    datoscsv = {'Canción': [], 'Fragmento': [], 'Valor disparidad': []}

    # Procesar cada archivo en la carpeta de fragmentos y canciones en paralelo
    archivos_fragmentos = [f for f in os.listdir(carpeta_fragmentos) if f.endswith('.wav')]
    archivos_canciones = [f for f in os.listdir(carpeta_canciones) if f.endswith(('.mp3', '.wav'))]

    with ProcessPoolExecutor() as executor:
        futuros = []
        for archivo_fragmento in archivos_fragmentos:
            for archivo_cancion in archivos_canciones:
                futuros.append(executor.submit(procesar_combinacion, archivo_fragmento, archivo_cancion, carpeta_fragmentos, carpeta_canciones, amp_min))

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
        cancion_probable = df_fragmento.loc[df_fragmento['Valor disparidad'].idxmax()]
        resultados_probables['Fragmento'].append(fragmento)
        resultados_probables['Canción Probable'].append(cancion_probable['Canción'])
        resultados_probables['Valor disparidad'].append(cancion_probable['Valor disparidad'])

    # Crear el dataframe final y guardar los resultados en un archivo CSV
    end_time = time.time()
    print(f"Tiempo total: {end_time - start_time} segundos")

    df_final = pd.DataFrame(resultados_probables)
    df_final.to_csv("result_picos.csv", index=False, encoding="utf-8")

    print("Comparaciones completadas y resultados guardados en 'result.csv'.")

if __name__ == '__main__':
    main()
