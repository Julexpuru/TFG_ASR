import os
from pathlib import Path

import keras
from keras.models import Sequential
from keras.layers import Dense, Activation,Bidirectional,LSTM,CuDNNLSTM

import sounddevice as sd
import soundfile as sf

import numpy as np
# np.set_printoptions(threshold='inf')
import scipy
from scipy.io import wavfile
from scipy import signal
import python_speech_features as psf
import matplotlib.pyplot as plt
from pandas import DataFrame

from recorder import gestor_muestras as gest


def obtener_muestra(path):
    sample= np.loadtxt(path)

    return sample

def crear_modelo():
    
    #################################################### Opcion Conv
    #print("Creating Model...")
    #model= Sequential()
    #model.add(Dense(100,input_shape=(161,157)))
    #model.add(Flatten())
    #model.add(Dense(1))
    #model.add(Activation('sigmoid'))


    ################################################### Opcion LSTM

    #Modificar para probar distintos modelos
    hidden_size=100
    epochs=25
    activation="tanh"

    if(activation=="tanh"):
        valida=1
        novalida=0
    elif(activation=="sigmoid"):
        valida=1
        novalida=0

    print("Creando Modelo...")
    model= Sequential()
    #model.add(Bidirectional(CuDNNLSTM(hidden_size,input_shape=[199,13],return_sequences=True)))
    model.add(CuDNNLSTM(hidden_size,input_shape=[199,13],return_sequences=True))
    model.add(CuDNNLSTM(hidden_size,input_shape=[199,13],return_sequences=True))
    model.add(CuDNNLSTM(hidden_size,input_shape=[199,13],return_sequences=True))
    #model.add(Bidirectional(CuDNNLSTM(hidden_size,input_shape=[199,13])))
    model.add(CuDNNLSTM(hidden_size,input_shape=[199,13]))
    model.add(Dense(1,activation=activation))

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    ###################################################training samples
    print("Obteniendo muestras disponibles")
    grupo="muestras2/"
    inputs=[]
    results=[]

    vh,vm,nh,nm,_=gest(grupo+"gestor_muestras.txt")

    for i in range(vh+1):
        if(i>0):
            inputs.append(obtener_muestra(grupo+"validas/vh"+str(i)))
            #if(i==((i*6)+1) or i==1):
            results.append(valida)  #Ponderacion de las muestras reales
            #else:
            #    results.append(0.75)    #Ponderacion de las muestras artificiales
    for i in range(vm+1):
        if(i>0):
            inputs.append(obtener_muestra(grupo+"validas/vm"+str(i)))
            #if(i==((i*6)+1) or i==1):
            results.append(valida)  #Ponderacion de las muestras reales
            #else:
            #    results.append(0.75)    #Ponderacion de las muestras artificiales
    for i in range(nh+1):
        if(i>0):
            inputs.append(obtener_muestra(grupo+"novalidas/nh"+str(i)))
            results.append(novalida)
    for i in range(nm+1):
        if(i>0):
            inputs.append(obtener_muestra(grupo+"novalidas/nm"+str(i)))
            results.append(novalida)

    ###################################################training
    print("Entrenando el modelo")
    inputs=np.array(inputs)
    results=np.array(results)
    history=model.fit(inputs,results,validation_split=0.3,epochs=epochs)

    ###################################################validation


    ps=obtener_muestra("muestras/test/test1")
    pn=obtener_muestra("muestras/test/test2")
    print("Prueba comando", model.predict(np.expand_dims(ps,axis=0)))
    print("Prueba no comando", model.predict(np.expand_dims(pn,axis=0)))

    # stored history
    train = DataFrame()
    val = DataFrame()
    train[str(i)] = history.history['loss']
    val[str(i)] = history.history['val_loss']

    # plot train and validation loss across multiple runs
    plt.plot(train, color='blue', label='train')
    plt.plot(val, color='orange', label='validation')
    plt.title('model train vs validation loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.show()

    model.save("modelo_comando")
    print("Modelo guardado")
    return model;

def entrenar_modelo(path,correct):
    print("Procediendo a entrenar modelo...")
    
    if (not Path("modelo_comando").is_file()):
        print("No existe modelo")
        crear_modelo()
        entrenar_modelo(path)
    else:
        model=keras.models.load_model("modelo_comando");
        
        while not (Path("muestras/"+path).is_file()):
            print("El archivo indicado no existe, introduzca uno valido")
            path=input()
        train=obtener_muestra("muestras/"+path)
        model.train_on_batch(np.expand_dims(train,axis=0),[correct])
        model.save("modelo_comando")
        print("Modelo entrenado")
    
def obtener_prediccion(path):
    model=keras.models.load_model("modelo_comando")
    print("Procesando prediccion...")
    
    candidate= obtener_muestra("muestras/"+path)
    result= model.predict(np.expand_dims(candidate,axis=0))
    
    if result[0] >0.66 :
        print("COMANDO ", result[0])
    else:
        print("NO COMANDO ", result[0])

def insta_pred(mel):
    model=keras.models.load_model("modelo_comando")
    print("Procesando prediccion...")
    
    result= model.predict(np.expand_dims(mel,axis=0))
    if result[0] >0.66 :
        print("COMANDO ", result[0])
    else:
        print("NO COMANDO ", result[0])
    
    return model
    