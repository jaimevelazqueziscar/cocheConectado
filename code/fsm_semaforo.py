import connection
import time
from time import sleep
from random import randint
import definicion_clases
#Actúa como semáforo


knownCarsbySemaforo = definicion_clases.truthSemaforo()
knownCarsBySemaforo.cargarDatos()
estado = 0

addrs = []

velocidades = []

minVel = 0

hora_salida = "00:00:00"

resultados = open("resultados.txt", "w")

def recepcion_semaforo():
    global estado
    global addrs
    global minVel
    global velocidades
    global hora_salida
    global resultados
    print ("Recibiendo información")

    velocidades, addrs = connection.recepcion_semaforo(0, 300, knownCarsbySemaforo, 3)

    estado = 1


def envio_semaforo():
    global estado
    global addrs
    global minVel
    global velocidades
    global knownCarsbySemaforo
    global hora_salida
    global resultados
    print ("Enviando información")
    print (addrs)
    minVel, hora_salida = connection.envio_semaforo(addrs, velocidades, knownCarsbySemaforo, 3, resultados)
    knownCarsbySemaforo.mostrarInfo()
    print ("Velocidad mínima = ", minVel)
    estado = 2


def true_false():
    global estado
    global knownCarsbySemaforo
    global minVel
    global hora_salida

    print ("Comprobando que la información era o no verídica")

    connection.true_false(minVel, hora_salida, knownCarsbySemaforo, resultados)
    print ("Velocidad minima", minVel)
    knownCarsbySemaforo.mostrarInfo()
    knownCarsBySemaforo.guardarEvaluaciones()
    print ("\nFinished")
    minVel = 0
    estado = 0


def FSM():
    global estado
    switch = {
        0 :recepcion_semaforo,
        1 :envio_semaforo,
        2 :true_false,
    }
    func = switch.get(estado, lambda: None)
    return func()

while True:
    FSM()

