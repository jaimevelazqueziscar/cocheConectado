import info_coches
import numpy as np
import datetime
from time import time
import time
import random
import connection
import definicion_clases

print("start")

estado = 'i'

datos = definicion_clases.datos()
datos.cargarDatos()
array_carretera = []
array_destinos = []
truthtable = definicion_clases.truthtable()
truthtable.cargarDatos()

now = datetime.datetime.now()
hora = now.hour
momento = None


carretera = None
carretera_ant = None
destino = None

message = ""
addr = ""
data = ""
client_socket = ""
server_socket = ""

momento = 0
nCoches = 0
tiempo1 = 0
n = 0
def start():
    print ("Estado inicial")
    global datos
    global array_carretera
    global array_destinos
    global hora
    global carretera
    global carretera_ant
    global destino
    global estado
    global momento
    global message
    global addr
    global data
    global client_socket
    global server_socket
    global n
    global nCoches
    global t1
    global truthtable
    n = 0

    now = datetime.datetime.now()
    hora = now.hour
    #datos.mostrarInfo()
    print ("Tiempo de almacenamiento, verdad y alerta = ", time.time() - momento)
    t1 = time.time()
    print (t1)
    archivo = open('nCoches.txt', 'w')
    archivo.write(str(0))
    archivo.close()


    prioridad_bt = np.loadtxt('prioridad_bt.txt', dtype = "str")
    if prioridad_bt == "semaforo":
        archivo = open('prioridad_bt.txt', 'w')
        archivo.write("OK")
        archivo.close()
        print ("Prioridad concedida al semáforo")

        while True:
            prioridad_bt = np.loadtxt('prioridad_bt.txt', dtype="str")
            if prioridad_bt == "comunicacion":
                print ("El semáforo me devuelve la prioridad")
                break
            time.sleep(0.1)

    carretera_ant = carretera

    print ("Introducir carretera actual:")
    carretera = input()
    print ("Introducir destino:")
    destino = input()
    momento = time.time()

    print ("Carretera anterior: ", carretera_ant)
    print ("Carretera actual: ", carretera)

    estado = 0

def recibir_comunicacion():

    global datos
    global array_carretera
    global array_destinos
    global hora
    global carretera
    global destino
    global estado
    global message
    global addr
    global data
    global client_socket
    global server_socket
    global truthtable

    print ("ESTADO RECIBIR COMUNICACIÓN")
    print ("Antes de recibir info = ", time.time()-momento)
    data, addr, client_socket, server_socket = info_coches.receive_communication()
    #datos.mostrarInfo()
    print ("Despues de recibir info = ", time.time()-momento)
    if data == 0 and addr == 0 and client_socket == 0 and server_socket == 0:
        estado = 1

    else:
        connection.close_sockets(client_socket, server_socket)
        estado = 2

def buscar_dispositivos():

    global datos
    global array_carretera
    global array_destinos
    global hora
    global carretera
    global destino
    global estado
    global message
    global addr
    global data
    global client_socket
    global server_socket
    global t1
    global truthtable
    global momento

    print ("ESTADO BUSCAR DISPOSITIVOS")
    print ("Tiempo hasta salir de la recepcion = ", time.time() - momento)
    momento = time.time()
    message, addr = info_coches.search_devices(datos, carretera)

    umbral1 = 30
    umbral2 = 60
    umbral3 = 120

    congestion = info_coches.carretera_congestionada(datos, carretera, hora)

    if addr == 0:
        if congestion < 0.25 and time.time() - t1 > umbral1:
            estado = 4
        elif congestion > 0.25 and congestion < 0.5 and time.time() - t1 > umbral2:
            estado = 4
        elif congestion > 0.5 and time.time() - t1 > umbral3:
            estado = 4
        else:
            estado = 0
    else:
        print ("Tiempo hasta que se encontró un dispositivo = ", time.time() - momento)
        momento = time.time()
        estado = 3


def procesar_informacion():

    global datos
    global array_carretera
    global array_destinos
    global hora
    global carretera
    global destino
    global estado
    global momento
    global message
    global addr
    global data
    global client_socket
    global server_socket
    global truthtable

    print ("ESTADO PROCESAR INFORMACIÓN")
    print ("Antes de procesar = ", time.time()-momento)

    message = info_coches.process_information(datos, carretera, hora, destino, array_carretera, array_destinos, data, addr)
    print ("Despues de procesar = ", time.time()-momento)
    if message == "CLOSE SOCKETS":
        estado = 4
    else:
        estado = 3


def enviar_comunicacion():

    global datos
    global array_carretera
    global array_destinos
    global hora
    global carretera
    global destino
    global estado
    global momento
    global message
    global addr
    global data
    global client_socket
    global server_socket
    global n
    global tiempo1
    print ("ESTADO ENVIAR COMUNICACIÓN")
    global truthtable
    print ("Antes de conectarse = ", time.time()-momento)
    info_coches.send_communication(message, addr)
    print ("Después de enviar = ", time.time()-momento)
    print (time.time())
    print ("Tiempo hasta que se consiguió conectar al dispositivo detectado = ", time.time() - momento)
    if n == 0:
        tiempo1 = time.time()
        print ("Tiempo1 =", tiempo1)

    n += 1

    if message == "NO" or message == "DESTINO CONGESTIONADO" or message == "DESTINO NO CONGESTIONADO":
        estado = 4
    else:
        try:
            m1, m2 = message.split("/")
            if m1 == "MI DESTINO" or m1 == "MI CONGESTIÓN":
                estado = 4
            else:
                estado = 0
        except:
            print ("Mensaje de un solo elemento")
            estado = 0


def almacenar_array_principal():

    global datos
    global array_carretera
    global array_destinos
    global hora
    global carretera
    global destino
    global nCoches
    global estado
    global momento
    global message
    global addr
    global data
    global client_socket
    global server_socket
    global nCoches
    global tiempo1
    global truthtable
    global t1

    print ("ESTADO ALMACENAR ARRAY PRINCIPAL")
    print ("Tiempo1 = ", tiempo1)
    print ("time = ", time.time())
    print ("Se ha tardado en efectuar la comunicación " + str(time.time() - momento) + "segundos")
    momento = time.time()

    #print ("Introducir el número de coches detectados (se hará con la cámara)")
    #nCoches = input()
    nCoches = np.loadtxt('nCoches.txt')
    print ("Se han detectado %d coches en este tramo" % int(nCoches))
    info_coches.almacenamiento_array_principal(datos, carretera, array_destinos, array_carretera, nCoches, t1, truthtable, addr)

    truthtable.mostrarInfo()
    array_destinos = []

    estado = 5

def calcular_factor_verdad():

    global datos
    global array_carretera
    global array_destinos
    global hora
    global carretera
    global destino
    global estado
    global message
    global addr
    global data
    global client_socket
    global server_socket
    global truthtable

    print ("ESTADO CALCULAR FACTOR VERDAD")

    truthtable.mostrarInfo()
    info_coches.true_false_carretera(datos, carretera, hora, array_carretera, truthtable, addr)
    array_carretera = []
    truthtable.mostrarInfo()

    estado = 6


def alerta():

    global datos
    global array_carretera
    global array_destinos
    global hora
    global carretera
    global destino
    global estado
    global message
    global addr
    global data
    global client_socket
    global server_socket
    global truthtable


    print ("ESTADO ALERTA")

    #print ("Array de datos:", datos.mostrarInfo())
    print ("Carretera actual: ", carretera)
    print ("Destino actual: ", destino)
    print ("Hora actual: ", hora)
    conozco_destino, dest_congestionado, cong = info_coches.destino_congestionado(datos, carretera, hora, destino)
    nTimes = info_coches.get_nTimes(datos, carretera, hora)

    if dest_congestionado == 1 and nTimes > 5:
        print ("DESTINO CONGESTIONADO, CAMBIAR LA RUTA")

    congestion = info_coches.carretera_congestionada(datos, carretera, hora)

    if congestion > 0.7:
        print ("CARRETERA CONGESTIONADA, CAMBIAR DE RUTA EN CUANTO SEA POSIBLE")

    print ("Tiempo de almacenamiento, verdad y alerta = ", time.time() - momento)
    datos.guardarCarreteras()
    truthtable.guardarCarreteras()
    estado = 'i'


def FSM():

    global estado
    switch = {
        'i':start,
         0 :recibir_comunicacion,
         1 :buscar_dispositivos,
         2 :procesar_informacion,
         3 :enviar_comunicacion,
         4 :almacenar_array_principal,
         5 :calcular_factor_verdad,
         6 :alerta,
    }
    func = switch.get(estado, lambda: None)
    return func()

while True:
    FSM()




