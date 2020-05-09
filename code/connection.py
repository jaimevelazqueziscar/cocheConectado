from bluetooth import *
from time import *
import numpy as np
import socket
from datetime import datetime, timedelta, date
import math
import io
import sys
import os
import definicion_clases

#Zona de envío de información

def search_available_devices(time):
    addrs = []
    nearby_devices = discover_devices(lookup_names = True, duration = time)
    for addr, name in nearby_devices:
        if name == "indigo-quill":	#el nombre de nuestro semáforo
            addrs += [addr]
    return addrs

def send_info(addr, message, port):

    client_socket=BluetoothSocket( RFCOMM )
    nTimes = 0
    nTimesMax = 20

    while nTimes < nTimesMax:
        try:
            print ("Intentando conectar a ", addr)
            client_socket.connect((addr, port))
            print ("Conectado al dispositivo ", addr)
            client_socket.send(message)
            return client_socket

        except btcommon.BluetoothError as e:
            if str(e) == "[Errno 111] Connection refused":
                print ("Conexión rechazada. Reintentar...")
                nTimes += 1
            elif str(e) == "[Errno 104] Connection reset by peer":
                print ("Fallo en la conexión. Reintentar...")
                sleep(0.1)
                client_socket=BluetoothSocket( RFCOMM )
                client_socket.connect((addr, port))
                client_socket.send(message)
                print ("Problema solucionado")
                return client_socket
                nTimes += 1
            else:
                print ("No es posible enviar la información")
                print (e)
                break
        except Exception as e:
            print ("No es posible enviar la información")
            print (e)
            break
        else:
            break

#Zona de recepción de información


def receive_info(port):

    server_socket=BluetoothSocket( RFCOMM )

    server_socket.bind((socket.gethostname(), port))
    server_socket.listen(5)

    client_socket, address = server_socket.accept()

    while True:
        data = client_socket.recv(1024)
        print ("Recibido: [%s]" % data.decode())
        #client_socket.close()
        #server_socket.close()
        if data:
            break

    return data.decode(), address[0], client_socket, server_socket


def receive_info_timeout(port, timeout):

    server_socket=BluetoothSocket( RFCOMM )

    server_socket.bind((socket.gethostname(), port))
    try:
        server_socket.settimeout(timeout)
        server_socket.listen(5)
        client_socket, address = server_socket.accept()
        data = client_socket.recv(1024)

        print ("Recibido: [%s]" % data.decode())
        return data.decode(), address[0], client_socket, server_socket

    except:
        print ("Tiempo de espera cumplido. Pasamos al envío de información")
        server_socket.close()
        data = 0
        addr = 0
        server_socket = 0
        client_socket = 0
        return data, addr, client_socket, server_socket

    #server_socket.listen(5)

    #client_socket, address = server_socket.accept()

    #data = client_socket.recv(1024)

    #print ("received [%s]" % data.decode())

    #return data.decode(), address[0], client_socket, server_socket


def close_sockets(client_socket, server_socket):

    client_socket.close()
    server_socket.close()

#ZONA DE IMPLEMENTACIÓN DE FUNCIONES

#Gestión del tráfico en un semáforo


def solicitud_semaforo(maxVel, port):
    while True:
        addrs = search_available_devices(3)
        if len(addrs) > 0:
            break
    print ("Found semaforo")
    client_socket = send_info(addrs[0], maxVel, port)
    client_socket.close()
    print ("Info sent to semaforo")
    return addrs[0]


def recepcion_semaforo(umbralCoches, umbralTiempo, known_devices, port):
    velocidades = []
    addrs = []
    t = time()
    while True:
        data, address, client_socket, server_socket = receive_info(port)
        close_sockets(client_socket, server_socket)
        print ("Información recibida de: ", address)
        velocidades += [data]
        addrs += [address]
        print (velocidades)
        print (addrs)
        known = False
        for device in known_devices.evaluaciones:
            if device.id == address:
                known = True
        if known == False:
            dev = definicion_clases.EvalSemaforo(address, 0, 0, 1, timedelta(seconds = 0), 0, 0.5)
            known_devices.agregarEvaluaciones(dev)

        if len(velocidades) > umbralCoches or time() - t > umbralTiempo:
            break

    return velocidades, addrs



def envio_semaforo(addrs, velocidades, known_devices, port, resultados):
    t1 = time()

    minVel = int(velocidades[0])
    for v in velocidades:
        if int(v) < int(minVel):
            minVel = v

    now = datetime.now() + timedelta(seconds=5)
    moment = now.strftime("%H, %M, %S")
    cont = 0

    for addr in addrs:
        for device in known_devices.evaluaciones:
            if addr == device.id:
                rep = reputation(device)
                if trust(rep, device.truth) >= 0.5:
                    vel_device = calculo_velocidad(minVel, device)
                    momento = calculo_momento(now, device)
                    message = str(vel_device) + "/" + str(momento)
                   # device[5] == 0
                   # device[4] == 0
                    print ("Last truth: ", device.truth)
                    print ("Reputation: ", rep)
                    print ("Trust:", trust(rep, device.truth))
                    resultados.write(str(rep) + "\t" + str(trust(rep, device.truth)))
                    client_socket = send_info(addr, message, port)
                    print ("Información enviada a: ", addr)
                    data, address, client_socket, server_socket = receive_info(port)
                    close_sockets(client_socket, server_socket)
                    print ("Confirmación recibida de: ", address)


                else:
                    cont += 1
                    print ("Truth: ", device.truth)
                    print ("nTimes: ", device.nTimes)
                    print ("Reputation: ", rep)
                    print ("Trust:", trust(rep, device.truth))
                    break

            else:
                continue

    if cont != 0:
        for addr in addrs:
            message = "ABORT"
            client_socket = send_info(addr, message, port)
            print ("Información enviada a: ", addr)
            data, address, client_socket, server_socket = receive_info(port)
            close_sockets(client_socket, server_socket)
            print ("Confirmación recibida de: ", address)

    addrs = []
    velocidades = []
    return minVel, str(moment)


def confirmacion_semaforo(port, addrSemaforo):
    data, address, client_socket, server_socket = receive_info(port)
    print ("Info received from semaforo")
    t1 = time()
#    while True:
 #       if time()-t1 > 2:
  #          break
    client_socket = send_info(addrSemaforo, "OK", port)
    close_sockets(client_socket, server_socket)
    print ("Confirmation sent to semaforo")
    if data == "ABORT":
       return 0, 0
    else:
        info = data.split("/")
        velocidad = info[0]
        momento = info[1]
        print (velocidad)
        print (momento)
        print ("Communication finished")
        return velocidad, momento







#Zona de funciones de reputación y confianza

def truth_vel(theoricalData, realData, device):
    dif = int(theoricalData) - int(realData)
    if dif == 0:
        return 1
    else:
        if dif > 0:
            #print ("Valor de dif vel = ", dif)
            device.difVel == device.difVel - dif
            return 0
        else:
            #print ("Valor de dif vel = ", dif)
            device.difVel == device.difVel + dif
            return 0

def update_vel(theoricalData, realData, device):
    dif = int(theoricalData) - int(realData)
    if dif > 0:
        #print ("Valor de dif vel = ", dif)
        return -dif
    else:
        #print ("Valor de dif vel = ", dif)
        return dif


def truth_moment(theorical_moment, real_moment, device):
    momento_real = datetime.strptime(real_moment, "%H, %M, %S")
    momento_teorico = datetime.strptime(theorical_moment, "%H, %M, %S")
    dif = abs(momento_real - momento_teorico)
    if dif.seconds == 0:
        return 1
    else:
        return 0


def update_moment(theorical_moment, real_moment, device):
    momento_real = datetime.strptime(real_moment, "%H, %M, %S")
    momento_teorico = datetime.strptime(theorical_moment, "%H, %M, %S")
    dif = momento_teorico - momento_real
    #print ("Valor de dif days = ", dif.days)
    #print (dif)
    dif2 = dif.days*86400+dif.seconds
    if dif.days >= 0:
        return dif
    else:
        return -timedelta(seconds = -dif2)




def reputation(device):
    alpha = 0.5
    initialReputation = 0.5
    r1 = initialReputation + device.sumTruth
    #print ("Sumatorio de truth_i anteriores ", device[1])
    #print ("Último valor de truth ", device[6])
    #print ("Valor de r1 = ", r1)
    #print ("Último valor de reputation = ", device[2])
    #print ("Número de veces = ", device[3])

    if device.truth >= alpha:
        device.repAnt = r1
        return r1/device.nTimes
    else:
        r2 = r1 - device.repAnt/(device.nTimes-1) + math.exp(-(1-device.truth)*device.nTimes)
        device.repAnt = r2
        return r2/device.nTimes

def trust(reputation, truth):
    gamma = 0.3
    return gamma*truth + (1-gamma)*reputation


def true_false(velocidad_teorica, momento_teorico, arrayFiabilidad, resultados):
    for device in arrayFiabilidad.evaluaciones:
        print ("Introducir velocidad real de salida: ")
        velocidad_real = input()
        print ("Introducir momento real de salida: ")
        momento_real = input()
        #print ("Device antes de comprobación")
        #print (device)
        print ("Velocidad teórica = ", velocidad_teorica)
        print ("Velocidad real = ", velocidad_real)
        #print ("Array fiabilidad index = ", arrayFiabilidad.index(device))
        truth_v = truth_vel(velocidad_teorica, velocidad_real, device)
        truth_m = truth_moment(momento_teorico, momento_real, device)
        dif_v = update_vel(velocidad_teorica, velocidad_real, device)
        dif_m = update_moment(momento_teorico, momento_real, device)
        device.difTime = device.difTime + dif_m
        device.difVel = device.difVel + dif_v
        truth = (truth_v + truth_m)/2
        device.truth = truth
        device.sumTruth = device.sumTruth + truth
        device.nTimes = device.nTimes + 1
        print ("Truth_v = ", truth_v)
        print ("Truth_m = ", truth_m)
        print ("Truth = ", truth)
        resultados.write("\t" + str(truth) + "\n")
    #print ("Finished")


def calculo_velocidad(minVel, device):
    print ("Calculamos a velocidad mínima de arranque para cada coche")
    return int(minVel) + int(device.difVel)



def calculo_momento(moment, device):
    print ("Calculamos el momento de arranque para cada coche")
    return moment + device.difTime




