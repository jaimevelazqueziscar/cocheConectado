from bluetooth import *
from time import time
import numpy as np
import socket


port_SEMAFORO = 3

#Zona de envío de información

def search_devices(number_of_devices):
    while True:
    nearby_devices = discover_devices(lookup_names = True, duration = 1)
    if (len(nearby_devices) > number_of_devices):
        break
    return nearby_devices

def match_nearby_devices(allowed_devices, nearby_devices):
    list = np.genfromtxt(allowed_devices, dtype='str')
    for addr, name in nearby_devices:
        for listed_names in list:
            if name == listed_names:
                return addr

def send_info(addr, message):

    client_socket=BluetoothSocket( RFCOMM )

    client_socket.connect((addr, 3))
    client_socket.send(message)
    print ("Finished")
    client_socket.close()


#Zona de recepción de información


def receive_info(port):

    server_socket=BluetoothSocket( RFCOMM )

    server_socket.bind((socket.gethostname(), port))
    server_socket.listen(1)

    client_socket, address = server_socket.accept()

    data = client_socket.recv(1024)

    print ("received [%s]" % data.decode())

    client_socket.close()
    server_socket.close()
    return data.decode(), address[0]


#Zona de implementación de funciones


def arranque_semaforo():

    data, address = receive_info(port_SEMAFORO)
    send_info(address, "OK")
    return data

