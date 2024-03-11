#para activar anaconda $conda config --set auto_activate_base True
#y volver a abrir el terminal
import numpy as np
import pandas
import sys
import scipy as sc #procesamiento, para transformada fourier, interpolacion etc
import soundfile as sf
import os
import pydub as pd #se usa para tener la función de transformar mp3 en wav
import matplotlib.pyplot as plt

#a = open("test.txt")
#print(a.read())

#b = sys.argv
c = sys.argv[1]
destino = "test.wav"
#a = open(c)

#print(c)
#dst_path = "test.wav"
#cwav = pd.AudioSegment.from_file(c)
#cwav.export(dst_path,format="wav")


ej, samplerate = sf.read(c)


print(ej.shape)
x = np.linspace(0, 1, 106148)
plt.plot(x,ej)
plt.axis([0,1,0,2])
plt.show()



