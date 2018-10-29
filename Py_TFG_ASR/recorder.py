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
import pydub
import ffmpeg
import matplotlib.pyplot as plt
import random

#Area de trabajo
area="muestras"
#area="muestras"

#Zona de volcado
zona="muestras2"
#zona="muestras2"

def grabar(path):

    print("Grabando")
    duration = 2
    if(area=="muestras"):
        fs = 16000
    else:
        fs = 44100
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
    if(area=="muestras"):
        features= psf.mfcc(samples,sample_rate,winlen=0.02,winstep=0.003,winfunc= lambda x:np.hamming(320),numcep=13)
        #features=psf.mfcc(samples,sample_rate)
    else:
        features= psf.mfcc(samples, sample_rate,nfft=2048)
    dir= wav.split(".")[0]
    np.savetxt(dir,features)

def instaMel(grab,fs):
    if(area=="muestras"):
        return psf.mfcc(grab,fs,winlen=0.02,winstep=0.003,winfunc= lambda x:np.hamming(320),numcep=13)
    else:
        return psf.mfcc(grab, fs,nfft=2048)

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

    vh,vm,nh,nm,t =gestor_muestras(zona+"/gestor_muestras.txt");
    s=wavfile.read(area+path +".wav")
    
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
    shutil.copyfile(area+"/"+ format +case + str(n), zona+"/"+ format +case +str(index))

    if (area=="muestras"):
        m=instaMel(s[1],16000)
    else:
        m=instaMel(s[1],44100)

    for i in range(index+1,index+6):
        rand=random.uniform(0.98,1.02)
        mm=m*rand
        np.savetxt(zona+"/"+format +case +str(i),mm)
    if(case=="vh"):
        mod_gestor(vh+6,vm,nh,nm,t,zona+"/gestor_muestras.txt")
    elif(case=="vm"):
        mod_gestor(vh,vm+6,nh,nm,t,zona+"/gestor_muestras.txt")
    elif(case=="nh"):
        mod_gestor(vh,vm,nh+6,nm,t,zona+"/gestor_muestras.txt")
    if(case=="nm"):
        mod_gestor(vh,vm,nh,nm+6,t,zona+"/gestor_muestras.txt")

def procesar_audios(file):
    
    #pydub.AudioSegment.converter="C:/Users/Julen/AppData/Roaming/Python/Python36/site-packages/ffmpeg/ffmpeg-4.0.2-win64-static/bin/ffmpeg.exe"
    audio= pydub.AudioSegment.from_wav(file)

    audio_chunks = pydub.silence.split_on_silence(audio, 
    # must be silent for at least half a second
    min_silence_len=50,

    # consider it silent if quieter than -16 dBFS
    silence_thresh=-80
    )

    for i, chunk in enumerate(audio_chunks):
        if(len(chunk)<2000):
            chunk2=rellenar_audio(chunk);
            out_file = "audios/procesados/chunk{0}.wav".format(i)
            print ("exporting " + out_file)
            chunk2.export(out_file, format="wav")

def rellenar_audio(chunk):
    silence=2000-len(chunk)
    silence_audio= pydub.AudioSegment.silent(duration=(silence/2),frame_rate=16000)
    return silence_audio+chunk+silence_audio