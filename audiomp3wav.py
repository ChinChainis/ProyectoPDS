#para activar anaconda $conda config --set auto_activate_base True
#y volver a abrir el terminal
import numpy as np
import pandas
import sys
import scipy as sc #procesamiento, para transformada fourier, interpolacion etc
from scipy.io import wavfile
#import soundfile as sf
import os
import pydub as pd #se usa para tener la función de transformar mp3 en wav
import matplotlib.pyplot as plt
import math
#IMPORTANTE
#importar solo el segmento de audio
from pydub import AudioSegment

#IMPORTANTE
#si no os funciona seguramente sea por ffmpeg
#conda install -c conda-forge ffmpeg
#o añadir desde el anaconda navigator => enviroments => el ffmpeg


src = "kieran.mp3"
dst = "test.wav"

# convert mp3 to wav                                                            
sound = AudioSegment.from_mp3(src) 
sound.export(dst, format="wav")
