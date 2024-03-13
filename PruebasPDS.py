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

#a = open("test.txt")
#print(a.read())

#b = sys.argv
cancionbuscar = sys.argv[1]
fragmento = sys.argv[2]
#a = open(c)

#print(c)
#dst_path = "test.wav"
#cwav = pd.AudioSegment.from_file(c)
#cwav.export(dst_path,format="wav")


#ej, samplerate = sf.read(c)
print(cancionbuscar)

Fs, funOG = wavfile.read(cancionbuscar) #Fs frecuencia de 16000 hercios 
Fs, funFR = wavfile.read(fragmento)

print(funFR.shape)

fig, (ax, ax2) = plt.subplots(1,2)

x = np.linspace(0, 1, 106148)
x2 = np.linspace(0, 1, 32000)
ax.plot(x,funOG, label="Funcion Cancion")
ax2.plot(x2,funFR, label="Funcion Fragmento",  color="Green")

ax.axis([0,1,0,30000])
ax2.axis([0,1,0,30000])

ax.legend(loc=0)
ax2.legend(loc=0)

plt.show()



