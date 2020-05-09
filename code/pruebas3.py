import connection
import time

#Actúa como semáforo

knownSemaforos = []

knownCarsbyCars = []

knownCarsbySemaforo = []


def main():
    print("start")
    minVel, addrs = connection.recepcion_semaforo(7, knownCarsbySemaforo, 3)
    print (minVel)
    print (addrs)
    hora_salida = "12:40:00"
    connection.envio_semaforo(addrs, knownCarsbySemaforo, minVel, hora_salida, 3)



if __name__ == '__main__':
    main()








