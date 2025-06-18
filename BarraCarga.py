import time
import sys

def barra_de_carga(duracion, longitud_barra=50):
    for i in range(longitud_barra + 1):
        #Calcular el porcentaje completo
        porcentaje = (i / longitud_barra) * 100

        #Crea la barra de carga
        barra = '[' + '=' *i+''*(longitud_barra - i) + ']'

        # Impreme la barra y el porcentaje
        sys.stdout.write(f"\r{barra}{porcentaje:.1f}%")
        sys.stdout.flush()

        #Espera un tiempo para simular la carga
        time.sleep(duracion / longitud_barra)

    #Imprime una nueva linea al final
    print()

#Durasion de carga de barra (segundos)
duracion_total = 50 # se puede ajustar

#llamar la funcion 
barra_de_carga(duracion_total)
