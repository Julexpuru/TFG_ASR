# 1. Import library of functions
import numpy as np
import tflearn
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
import tensorflow as tf


## 2. Logical OR operator / the data
input = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
YOR = np.array([[0.], [1.], [1.], [1.]])
YAND=np.array([[0.], [0.], [0.], [1.]])
YNOT=np.array([[0.], [1.], [1.], [0.]])



def redTF():
    #####   VERSION TFLEARN     #####
    # 3. Building our neural network/layers of functions 
    neural_net = tflearn.input_data(shape=[None, 2])
    neural_net = tflearn.fully_connected(neural_net, 1, activation='sigmoid')
    neural_net = tflearn.regression(neural_net, optimizer='sgd', learning_rate=2, loss='mean_square')

    ## 4. Train the neural network / Epochs
    model = tflearn.DNN(neural_net,tensorboard_verbose=0)
    model.fit(input, YOR, n_epoch=1000, snapshot_epoch=False)

    #model.save('test_modelo')

    # 4.5 Prueba solo cargando un modelo guardado previamente
    #model.load("test_modelo")

    # 5. Testing final prediction
    print("Testing OR operator")
    print("0 or 0:", model.predict([[0., 0.]]))
    print("0 or 1:", model.predict([[0., 1.]]))
    print("1 or 0:", model.predict([[1., 0.]]))
    print("1 or 1:", model.predict([[1., 1.]]))

def redKeras():
    ######   VERSION KERAS    #####
    # 3. Building our neural network/layers of functions 
    model= Sequential()
    model.add(Dense(100,input_shape=[2,]))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # 4. Train the neural network / Epochs
    model.fit(input,YOR,epochs=10000,verbose=1)

    # 4.5 Prueba solo cargando un modelo guardado previamente

    # 5. Testing final prediction
    print("Testing OR operator")
    print("0 or 0:", model.predict(np.array([[0., 0.]])))
    print("0 or 1:", model.predict(np.array([[0., 1.]])))
    print("1 or 0:", model.predict(np.array([[1., 0.]])))
    print("1 or 1:", model.predict(np.array([[1., 1.]])))

    #pruebas para guardar json que importar a tf
    #model_json=model.to_json()
    #with open("model.json", "w") as json_file:
    #    json_file.write(model_json)
    #keras.models.save_model(model,"modeloprueba")

#Actualmente probando
redKeras()