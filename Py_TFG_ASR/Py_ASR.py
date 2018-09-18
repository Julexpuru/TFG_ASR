import reconocimiento as recon
import recorder as rec
import menus as ui
import re

done=False

#rec.espectrograma("muestras/novalidas/nh21.wav")

print()
print("Herramienta de gestion del modelo STT")
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
        vh,vm,nh,nm,t =rec.gestor_muestras("muestras/gestor_muestras.txt");
        if(re.match("[sS]",vn) and re.match("[hH]",hm)):
            path="muestras/validas/vh"+str(vh+1)
            rec.mod_gestor(vh+1,vm,nh,nm,t,"muestras/gestor_muestras.txt")
        elif(re.match("[sS]",vn) and re.match("[mM]",hm)):
            path="muestras/validas/vm"+str(vm+1)
            rec.mod_gestor(vh,vm+1,nh,nm,t,"muestras/gestor_muestras.txt")
        elif(re.match("[nN]",vn) and re.match("[hH]",hm)):
            path="muestras/novalidas/nh"+str(nh+1)
            rec.mod_gestor(vh,vm,nh+1,nm,t,"muestras/gestor_muestras.txt")
        elif(re.match("[nN]",vn) and re.match("[mM]",hm)):
            path="muestras/novalidas/nm"+str(nm+1)
            rec.mod_gestor(vh,vm,nh,nm+1,t,"muestras/gestor_muestras.txt") 
            
        rec.guardar_audio(path,fs,grab)
        opt= ui.Menu()

    ### Crear Modelo
    elif(opt==2): 
        recon.crear_modelo()
        opt= ui.Menu()

    ### Entrenar Modelo
    elif(opt==3): 
        print("Introduzca una muestra valida")
        
        muestra=input()
        while not re.match("[a-zA-Z0-9]*$",muestra):
           print("Introduzca una muestra valido (una palabra, sin wav)")
           muestra=input()

        print("Indique el resultado de la prueba (0 o 1)")
        correct=input()
        while not re.match("[0-1]?$",correct):
           print("Introduzca un resultado valido")
           correct=input()
        
        recon.entrenar_modelo(muestra,float(correct))
        opt= ui.Menu()

    ### Realizar Prediccion
    elif(opt==4): 
        print("Introduzca una muestra valida")
        
        muestra=input()
        
        recon.obtener_prediccion(muestra)
        opt= ui.Menu()

    ### Ejecutar Prediccion
    elif(opt==5): 
        print("Reconocimiento de una palabra")

        grab,fs,_=rec.grabar(None)
        print("Procesando")
        sample=rec.instaMel(grab,fs)
        recon.insta_pred(sample)
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

        vh,vm,nh,nm,t =rec.gestor_muestras("muestras/gestor_muestras.txt");
        for i in range(vh+1):
            if(i>0):
                rec.mod_muestra("validas/vh"+str(i))
        for i in range(vm+1):
            if(i>0):
                rec.mod_muestra("validas/vm"+str(i))
        for i in range(nh+1):
            if(i>0):
                rec.mod_muestra("novalidas/nh"+str(i))
        for i in range(nm+1):
            if(i>0):
                rec.mod_muestra("novalidas/nm"+str(i))
        
        print("Muestras artificiales generadas correctamente")
        opt= ui.Menu()

    elif(opt==0):
        done=True
           

#print("empieza a grabar")
#rec.grabar()
#rec.melFeatures("muestras/pcomando.wav")
#rec.espectrograma("muestras/pcomando.wav")
