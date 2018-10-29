import os
from pathlib import Path

import reconocimiento as recon
import recorder as rec
import menus as ui
import re

import keras
import numpy as np

done=False
model=None

#rec.espectrograma("muestras44/novalidas/nh5.wav")

#Area de trabajo
area="muestras"
#area="muestras2"
#area="muestras44"
#area="muestras442"

def pred(model,sample):
    print("Procesando prediccion...")
    
    result= model.predict(np.expand_dims(sample,axis=0))
    if result[0] >0.66 :
        print("COMANDO ", result[0])
    else:
        print("NO COMANDO ", result[0])


print()
print("Herramienta de gestion del modelo ASR")
opt= ui.Menu()

while (not done):
     ### Nueva Muestra
    if (opt==1):
        grab,fs,_=rec.grabar(None) ###Grabacion

        ###Datos de la muestra
        print("¿Es una muestra valida?(s/n)")
        vn=input()
        while not re.match("[sSnN]$",vn):
           print("Introduzca una respuesta valida (s/n)")
           vn=input()
        print("¿Es una muestra de hombre o mujer?(h/m)")
        hm=input()
        while not re.match("[hHmM]$",hm):
           print("Introduzca una respuesta valida (h/m)")
           hm=input()

        ###comprobacion de muestras existentes para establecer id de la nueva
        vh,vm,nh,nm,t =rec.gestor_muestras(area+"/gestor_muestras.txt");
        if(re.match("[sS]",vn) and re.match("[hH]",hm)):
            path=area+"/validas/vh"+str(vh+1)
            rec.mod_gestor(vh+1,vm,nh,nm,t,area+"/gestor_muestras.txt")
        elif(re.match("[sS]",vn) and re.match("[mM]",hm)):
            path=area+"/validas/vm"+str(vm+1)
            rec.mod_gestor(vh,vm+1,nh,nm,t,area+"/gestor_muestras.txt")
        elif(re.match("[nN]",vn) and re.match("[hH]",hm)):
            path=area+"/novalidas/nh"+str(nh+1)
            rec.mod_gestor(vh,vm,nh+1,nm,t,area+"/gestor_muestras.txt")
        elif(re.match("[nN]",vn) and re.match("[mM]",hm)):
            path=area+"/novalidas/nm"+str(nm+1)
            rec.mod_gestor(vh,vm,nh,nm+1,t,area+"/gestor_muestras.txt") 
            
        rec.guardar_audio(path,fs,grab)
        opt= ui.Menu()

    ### Crear Modelo
    elif(opt==2): 
        model=recon.crear_modelo()
        opt= ui.Menu()

    #### Cargar modelo
    elif(opt==3):
        print("¿Quiere cargar el ultimo modelo disponible?")
        sn=input()
        while not re.match("[sSnN]$",sn):
           print("Introduzca una respuesta valida (s/n)")
           sn=input()
        if(re.match("[sS]",sn)):
           print("Cargando modelo")
           model=keras.models.load_model("modelo_comando")
           print("Modelo cargado: modelo_comando")
        else:
            print("Introduzca el nombre de modelo que desee")
            md=input()
            while not (Path("modelosFuncionales/"+md).is_file()):
                print("Introduzca un modelo valido")
                md=input()
            print("Cargando modelo")
            model=keras.models.load_model("modelosFuncionales/"+md)
            print("Modelo cargado: "+md)

        opt= ui.Menu()
    #### Entrenar Modelo (Deprecated) 
    #    print("Introduzca una muestra valida")
        
    #    muestra=input()
    #    while not re.match("[a-zA-Z0-9]*$",muestra):
    #       print("Introduzca una muestra valido (una palabra, sin wav)")
    #       muestra=input()

    #    print("Indique el resultado de la prueba (0 o 1)")
    #    correct=input()
    #    while not re.match("[0-1]?$",correct):
    #       print("Introduzca un resultado valido")
    #       correct=input()
        
    #    recon.entrenar_modelo(muestra,float(correct))
    #    opt= ui.Menu()

    ### Realizar Prediccion
    elif(opt==4): 
        print("Introduzca una muestra valida")
        
        muestra=input()
        while not (Path("muestras/"+muestra).is_file()):
            print("El archivo indicado no existe, introduzca uno valido")
            muestra=input()
        if(model==None):
            recon.obtener_prediccion(muestra)
        else:
            candidate=recon.obtener_muestra("muestras/"+muestra)
            pred(model,candidate)
        opt= ui.Menu()

    ### Ejecutar Prediccion
    elif(opt==5): 
        print("Reconocimiento de una palabra")

        if(model==None):
            grab,fs,_=rec.grabar(None)
            print("Procesando")
            sample=rec.instaMel(grab,fs)
            model=recon.insta_pred(sample)
        else:
            grab,fs,_=rec.grabar(None)
            print("Procesando")
            sample=rec.instaMel(grab,fs)
            pred(model,sample)
        opt= ui.Menu()

    ###Opcion oculta: Ampliar muestras
    elif(opt==8):
        print("¿Seguro que quiere ampliar las muestras actuales?")
        yn=input()
        while not re.match("[sSnN]$",yn):
           print("Introduzca una respuesta valida (s/n)")
           yn=input()
        if(re.match("[nN]$",yn)):
            done=True
            break

        print("Procediendo a multiplicar muestras existentes")

        vh,vm,nh,nm,t =rec.gestor_muestras(area+"/gestor_muestras.txt");
        for i in range(vh+1):
            if(i>0):
                rec.mod_muestra("/validas/vh"+str(i))
        for i in range(vm+1):
            if(i>0):
                rec.mod_muestra("/validas/vm"+str(i))
        for i in range(nh+1):
            if(i>0):
                rec.mod_muestra("/novalidas/nh"+str(i))
        for i in range(nm+1):
            if(i>0):
                rec.mod_muestra("/novalidas/nm"+str(i))
        
        print("Muestras artificiales generadas correctamente")
        opt= ui.Menu()

    ###Opcion oculta: Muestras test
    elif(opt==9):
        grab,fs,_=rec.grabar(None) ###Grabacion

        ###comprobacion de muestras existentes para establecer id de la nueva
        vh,vm,nh,nm,t =rec.gestor_muestras("muestras/gestor_muestras.txt");
        path="muestras/test/test"+str(t+1)
        rec.mod_gestor(vh,vm,nh,nm,t+1,"muestras/gestor_muestras.txt")
            
        rec.guardar_audio(path,fs,grab)
        opt= ui.Menu()

    ###Opcion oculta: Procesar audios
    elif(opt=='p'):
        print("Introduzca un audio valido")
        
        muestra=input()
        while not (Path("audios/procesar/"+muestra+".wav").is_file()):
            print("El archivo indicado no existe, introduzca uno valido")
            muestra=input()
        
        rec.procesar_audios("audios/procesar/"+muestra+".wav")

        opt= ui.Menu()

    ###Opcion oculta: Cepstrales de los audios externos
    elif(opt=='c'):
        print("Obteniendo cepstrales de las muestras actuales")

        vh,vm,nh,nm,t=rec.gestor_muestras(area+"/gestor_muestras.txt")

        for i in range(vh+1):
            if(i>0):
                rec.melFeatures(area+"/validas/vh"+str(i)+".wav")
        for i in range(vm+1):
            if(i>0):
                rec.melFeatures(area+"/validas/vm"+str(i)+".wav")
        for i in range(nh+1):
            if(i>0):
                rec.melFeatures(area+"/novalidas/nh"+str(i)+".wav")
        for i in range(nm+1):
            if(i>0):
                rec.melFeatures(area+"/novalidas/nm"+str(i)+".wav")
        for i in range(t+1):
            if(i>0):
                rec.melFeatures(area+"/test/test"+str(i)+".wav")

        print("Cepstrales obtenidos")
        opt=ui.Menu()

    elif(opt==0):
        done=True
           

#print("empieza a grabar")
#rec.grabar()
#rec.melFeatures("muestras/pcomando.wav")
#rec.espectrograma("muestras/pcomando.wav")
