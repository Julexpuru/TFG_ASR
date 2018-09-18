# coding: utf-8
import shutil
from pathlib import Path
import numpy as np
# np.set_printoptions(threshold='inf')
import sounddevice as sd
import scipy
from scipy.io import wavfile
from scipy import signal
import python_speech_features as psf
import soundfile as sf
import matplotlib.pyplot as plt
import random

def grabar(path):
    if(path==None):
        path='muestras/nada.wav'
    else:
        path= "muestras/"+ path +".wav"

    print("Grabando")
    duration = 2
    fs = 16000
    rec = sd.rec(duration * fs, samplerate=fs,channels=1, dtype='int16')
    sd.wait()

    return rec, fs, path

def guardar_audio(path,frecuencia,grab):
    path=path+".wav"
    wavfile.write(path,frecuencia,grab)
    melFeatures(path)
    print("Muestra guardada")

def espectrograma(wav):
    sample_rate, samples = wavfile.read(wav)
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate, nperseg=320, noverlap=16)
    dBS = 10 * np.log10(spectrogram)  # convert to dB

    plt.subplot(2,1,1)
    plt.grid(True)
    plt.plot(samples)

    plt.subplot(2,1,2)
    plt.pcolormesh(times, frequencies, dBS,cmap='jet')
    #plt.imshow(dBS,aspect='auto',origin='lower',cmap='rainbow')
    plt.ylabel('Frecuencia [Hz]')
    plt.xlabel('Tiempo[s]')
    plt.colorbar()
    plt.show()

def melFeatures(wav):
    sample_rate, samples = wavfile.read(wav)
    features= psf.mfcc(samples, sample_rate)

    dir= wav.split(".")[0]
    np.savetxt(dir,features)

def instaMel(grab,fs):
    return psf.mfcc(grab, fs)

def gestor_muestras(path):
    file= open(path)
    lines= file.readlines()
    vh=int (lines[2])
    vm=int (lines[4])
    nh=int (lines[7])
    nm=int (lines[9])
    t=int(lines[11])
    file.close()

    return vh,vm,nh,nm,t

def mod_gestor(vh,vm,nh,nm,t,path):
    file=open(path,"w")
    file.write("Valida\nHombre\n"+str (vh)+"\nMujer\n"+str (vm)+"\nNo valida\nHombre\n"+str (nh)+"\nMujer\n"+str (nm)+"\nTest\n"+str (t))
    file.close()

def mod_muestra(path):    
    vh,vm,nh,nm,t =gestor_muestras("muestras2/gestor_muestras.txt");
    s=wavfile.read("muestras/"+path +".wav")
    
    #obtener el numero independientemente del formato
    if not(len(path.split("vh"))<2):
        format=path.split("vh")[0]
        case="vh"
        n=int(path.split("vh")[1])
    elif not(len(path.split("vm"))<2):
        format=path.split("vm")[0]
        case="vm"
        n=int(path.split("vm")[1])
    elif not(len(path.split("nh"))<2):
        format=path.split("nh")[0]
        case="nh"
        n=int(path.split("nh")[1])
    elif not(len(path.split("nm"))<2):
        format=path.split("nm")[0]
        case="nm"
        n=int(path.split("nm")[1])

    index=n+(5*(n-1))
    shutil.copyfile("muestras/"+ format +case + str(n), "muestras2/"+ format +case +str(index))

    m=instaMel(s[1],16000)

    for i in range(index+1,index+6):
        rand=random.uniform(0.9,1.1)
        mm=m*rand
        np.savetxt("muestras2/"+format +case +str(i),mm)
    if(case=="vh"):
        mod_gestor(vh+6,vm,nh,nm,t,"muestras2/gestor_muestras.txt")
    elif(case=="vm"):
        mod_gestor(vh,vm+6,nh,nm,t,"muestras2/gestor_muestras.txt")
    elif(case=="nh"):
        mod_gestor(vh,vm,nh+6,nm,t,"muestras2/gestor_muestras.txt")
    if(case=="nm"):
        mod_gestor(vh,vm,nh,nm+6,t,"muestras2/gestor_muestras.txt")