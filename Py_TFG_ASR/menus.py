import keyboard

def Menu():
    done=False
    print()
    print()
    print("Menu de opciones principales:")
    print("\t1)Grabar nueva muestra")
    print("\t2)Crear modelo")
<<<<<<< HEAD
    print("\t3)Cargar modelo")
=======
    print("\t3)Cargar modelo")#Entrenar modelo(Deprecated)
>>>>>>> 5ffa6296f64dc8bc0fb74aeee802443b12dd9c5e
    print("\t4)Predecir muestra")
    print("\t5)Ejecutar programa")
    print("\t6)Ejecucion continua (TODO)")
    print("\t0)Salir")

    while(not done):
        k=keyboard.read_key()

        if(k=='1'):
            done=True
            return 1
        elif(k=='2'):
            done=True
            return 2
        elif(k=='3'):
            done=True
            return 3
        elif(k=='4'):
            done=True
            return 4
        elif(k=='5'):
            done=True
            return 5
        elif(k=='8'):
            done=True
            return 8
        elif(k=='9'):
            done=True
            return 9
        elif(k=='0'):
            done=True
            return 0
            
            


    