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
#importar lo del  segmento de audio
from pydub import AudioSegment


#conda install -c conda-forge ffmpeg
#o añadir desde el anaconda navigator enviroments el ffmpeg


def mp3awav(ubicacion):
    path = os.getcwd()
    os.chdir(path + '/' + ubicacion)
    for archivo in  os.listdir(os.getcwd()):
        nombre, ext = os.path.splitext(archivo)
        if ext == ".mp3":
                mp3_sound = AudioSegment.from_mp3(archivo)
                mp3_sound.export("{0}.wav".format(nombre), format="wav")
    os.chdir(path)


mp3awav("audios")
archivos= os.listdir("audios")
for archivo in os.listdir("audios"):
    nombre, ext = os.path.splitext(archivo)
    if ext == ".mp3":
        archivos.remove(nombre+".mp3")
print(len(archivos))
