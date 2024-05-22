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
import funciones as func
import pickle
from typing import List, Dict, Tuple
import time


start_time = time.time()

datoscsv = {
    'fragment': [],
    'song': []
}

resultado = []
fragmento = sys.argv[1]
original = os.listdir(fragmento)


database = pickle.load(open('database.pickle', 'rb'))


resultado = []

df = pd.DataFrame(datoscsv)


for frag in original:
    nombref, extf = os.path.splitext(frag)
    #Si es .mp3, el array tiene dimensiones estéreo de x,2, lo necesitamos en mono
    if extf == ".mp3":
        print(original + '/' + '{0}.mp3'.format(nombref))
        funFR ,Fs  = sf.read(fragmento + '/' + '{0}.mp3'.format(nombref))
        if(funFR.ndim>1):
           funFR = funFR.mean(axis=-1)    
    #En .wav no hay problema
    else:
        Fs, funFR = wavfile.read(fragmento + '/' + frag)

    frag_a_comp = func.create_constellation(funFR,Fs)
    hash = func.create_hashes(frag_a_comp,frag)
    
    res = func.comparar2(hash,database)
    nombreres, extres = os.path.splitext(res)

    d = {'fragment':nombref, "song" : nombreres}

    datoscsv.update(d)
    df = df._append(d, ignore_index = True)
df.to_csv("result.csv", index=False,encoding="utf-8")
print("--- %s seconds ---" % (time.time() - start_time))


#python3 PruebasPDS.py audios audios/fragmento.wav
#python3 PruebasPDS.py songs fragments/fragment_AAIA.wav
#Ejemplo AAIA es DASU
#python3 main_constelacion.py fragments
#--- 622.4353518486023 seconds ---
# TASA DE ERROR: 2.10%
# RESULTADOS GLOBALES:          Percentage
# Correct (Song->Song)          98.0
# Correct (NF->NF)              96.0
# Incorrect (Song->Song)         0.0
# Incorrect (Song->NF)           2.0
# Incorrect (NF->Song)           4.0

