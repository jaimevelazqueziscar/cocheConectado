import connection
import datetime
import random
from bluetooth import *
from time import time
import math
import definicion_clases

#CÁLCULO Y ALMACENAMIENTO DE PARÁMETROS

def calcular_congestion_carretera(nCoches, momento_entrada):
    nCochesMax = 80
    now = time()
    dif = int(now) - int(momento_entrada)
    nCochesSeg = int(nCoches)/dif
    return nCochesSeg/nCochesMax


def calcular_congestion_destino(nCoches, nTimes):
    return nCoches/nTimes

def conozco_carretera(datos, carretera):
    cont = 0
    if len(datos.carreteras) == 0:
        return False
    else:
        for c in datos.carreteras:
            if c.nombre == carretera:
                cont += 1
                return True
            else:
                continue
        if cont == 0:
            return False


def get_nTimes(datos, carretera, hora):

    cont  = 0
    for c in datos.carreteras:
        if c.nombre == carretera:
            cont2 = 0
            for d in c.hora:
                if hora == d.hora:
                    cont2 += 1
                    return d.nTimes
                    break
                else:
                    continue
            if cont2 == 0:
                return 0
        else:
            continue
    if cont == 0:
        return 0


def destino_congestionado(datos, carretera, hora, destino):	#devuelve conozco_cong_destino y destino_congestionado
    umbralCongestion = 0.7

    if len(datos.carreteras) == 0:
        return 0, 0, 0
    else:
        cont = 0
        for c in datos.carreteras:
            print ("Analizando carretera anterior = ", c.nombre)
            if c.nombre == carretera:
                cont += 1
                if len(c.destino) == 0:
                    print ("No hay ningún destino registrado")
                    return 0, 0, 0
                else:
                    cont2 = 0
                    cont3 = 0
                    for t in c.destino:
                        for h in c.hora:
                            print ("Destino actual = ", destino)
                            print ("Destino almacenado = ", t.destino)
                            if t.destino == destino:
                                print ("El destino está registrado")
                                cont2 += 1
                                print ("Hora del destino almacenado = ", t.hora)
                                print ("Hora de nTimes = ", h.hora)
                                print ("Hora = ", hora)
                                if t.hora == hora and h.hora == hora:
                                    print ("El destino está registrado a esta hora")
                                    cont3 += 1
                                    cong = calcular_congestion_destino(t.nCoches, h.nTimes)
                                    print ("Valor de la congestión = ", cong)
                                    if cong > umbralCongestion:
                                        return 1, 1, cong
                                    else:
                                        return 1, 0, cong
                                else:
                                    continue
                            else:
                                continue
                    if cont2 == 0:
                        print ("El destino no está registrado")
                        cont2 = 0
                        return 0, 0, 0
                    if cont3 == 0:
                        print ("El destino no está registrado a esta hora")
                        cont3 = 0
                        return 1, 0, 0
            else:
                continue
        if cont == 0:
            cont = 0
            return 0, 0, 0

def carretera_congestionada(datos, carretera, time):

    if len(datos.carreteras) == 0:
        return 0
    else:
        cont = 0
        for c in datos.carreteras:
            if c.nombre == carretera:
                cont += 1
                if len(c.congestion) == 0:
                    return 0
                else:
                    if len(c.destino) == 0:
                        return 0
                    else:
                        cont2 = 0
                        for t in c.congestion:
                            if time == t.hora:
                                cont2 += 1
                                return t.coeficiente/t.nTimes
                            else:
                                continue
                        if cont2 == 0:
                            cont2 = 0
                            return 0
            else:
                continue
        if cont == 0:
            cont = 0
            return 0


def almacenar_destino_coches(carretera, destino, array_destinos):

    array_destinos.extend([carretera, destino])


def almacenar_congestion_carretera(carretera, data, array_carretera):

    array_carretera.extend([carretera, data])


#COMUNICACIÓN E INTERCAMBIO DE DATOS CON OTROS COCHES


def search_devices(datos, carretera):

    nTimes = 0
    nTimesMax = 5
    nearby_devices = 0

    while nTimes < nTimesMax:
        print ("Buscando dispositivos...")
        nearby_devices = discover_devices(lookup_names = True, duration = 3)
        print (nearby_devices)
        nTimes += 1
        if len(nearby_devices) > 0:
            break
    if len(nearby_devices) == 0:
        return 0, 0

    print ("Found devices")
    print (nearby_devices)
    addr, name = nearby_devices[0]

    if conozco_carretera(datos, carretera):
        message = "¿LUGAR DE DESTINO?"
    else:
        message = "¿CONGESTIÓN EN LA CARRETERA?"


    return message, addr


def receive_communication():

    print ("Esperando dispositivos...")

    data, addr, client_socket, server_socket = connection.receive_info_timeout(4, 8)
    return data, addr, client_socket, server_socket


def process_information(datos, carretera, time, destino, array_carretera, array_destinos, data, addr):

    try:
        data1, data2 = data.split('/')
        print (data1)
        print (data2)

        if data1 == "YES CONGESTIÓN":
            message = "MI DESTINO/" + str(destino)
            almacenar_congestion_carretera(carretera, float(data2), array_carretera)
            print ("Almacenado ", data2)
            return message


        elif data1 == "YES DESTINO":
            congestion = carretera_congestionada(datos, carretera, time)
            message = "MI CONGESTIÓN/" + str(congestion)
            almacenar_destino_coches(carretera, data2, array_destinos)
            print ("Almacenado ", data2)
            return message


        elif data1 == "OK, LA CONGESTIÓN DE MI DESTINO":
            conozco_cong_dest, destino_cong, cong = destino_congestionado(datos, carretera, time, destino)

            if destino_cong == 1:
                message = "DESTINO CONGESTIONADO"
            else:
                message = "DESTINO NO CONGESTIONADO"
            almacenar_destino_coches(carretera, data2, array_destinos)
            return message


        elif data1 == "OK MANDA TU DESTINO":

            almacenar_congestion_carretera(carretera, data2, array_carretera)
            message = "OK, LA CONGESTIÓN DE MI DESTINO/" + str(destino)
            return message

        elif data1 == "MI DESTINO":
            almacenar_destino_coches(carretera, data2, array_destinos)
            print ("Destino almacenado: ", array_destinos)
            message = "CLOSE SOCKETS"
            return message

        elif data1 == "MI CONGESTIÓN":
            almacenar_congestion_carretera(carretera, float(data2), array_carretera)
            message = "CLOSE SOCKETS"
            return message

        else:
            connection.close_sockets(client_socket, server_socket)
            message = "CLOSE SOCKETS"
            return message


    except ValueError as e:
        print ("Mensaje de un solo elemento")
        print (e)
    finally:
        print ("Continuar")

    if data == "¿INTERCAMBIAMOS DESTINOS?":
        conozco_congestion_destino, destino_cong, cong = destino_congestionado(datos, carretera, time, destino)

        if conozco_congestion_destino == 0:
            message = "¿TU CONGESTIÓN POR MI DESTINO?"
            return message

        elif conozco_congestion_destino == 1:
            message = "YES DESTINO/" + str(destino)
            return message

        else:
            message = "NO"
            return message

    elif data == "¿LUGAR DE DESTINO?":
        conozco_congestion_destino, destino_cong, cong = destino_congestionado(datos, carretera, time, destino)

        if conozco_congestion_destino == 0:
            message = "¿TU CONGESTIÓN POR MI DESTINO?"
            return message

        elif conozco_congestion_destino == 1:
            message = "¿INTERCAMBIAMOS DESTINOS?"
            return message

        else:
            message = "NO"
            return message

    elif data == "¿TU CONGESTIÓN POR MI DESTINO?":

        congestion = carretera_congestionada(datos, carretera, time)
        message = "YES CONGESTIÓN/" + str(congestion)
        return message



    elif data == "¿CONGESTIÓN EN LA CARRETERA?":
        message = "¿TU DESTINO POR MI CONGESTIÓN?"
        return message

    elif data == "¿TU DESTINO POR MI CONGESTIÓN?":
        conozco_congestion_destino, destino_cong, cong = destino_congestionado(datos, carretera, time, destino)

        if destino_cong == 1:
            message = "NO"
            return message

        elif conozco_congestion_destino == 1:
            message = "CONGESTIÓN DE MI DESTINO"
            return message

        else:
            message = "YES DESTINO/" + str(destino)
            return message

    elif data == "CONGESTIÓN DE MI DESTINO":
        conozco_congestion_destino, destino_cong, cong = destino_congestionado(datos, carretera, time, destino)

        if destino_cong == 1:
            message = "NO"
            return message

        else:
            message = "YES CONGESTIÓN DESTINO, TU CONGESTIÓN"
            return message

    elif data == "YES CONGESTIÓN DESTINO, TU CONGESTIÓN":

        congestion = carretera_congestionada(datos, carretera, time)
        message = "OK MANDA TU DESTINO/" + str(congestion)
        return message

    elif data == "DESTINO CONGESTIONADO":
        print ("CAMBIAR DE RUTA, MI DESTINO ESTÁ CONGESTIONADO")

    elif data == "DESTINO NO CONGESTIONADO":
        print ("DESTINO NO CONGESTIONADO, CONTINUAR POR AQUÍ")
        message = "CLOSE SOCKETS"
        return message

    elif data == "NO":
        message = "CLOSE SOCKETS"
        return message

    else:
        message = "CLOSE SOCKETS"
        return message


def send_communication(message, addr):

    client_socket = connection.send_info(addr, message, 4)
    print ("Enviado: ", message)
    client_socket.close()




#COMPROBACIÓN DE VALORES COMPARTIDOS, REPUTACIÓN Y CONFIANZA


def truth(theoricalData, realData):
    dif = abs(float(theoricalData) - float(realData))
    print ("Diferencia = ", dif)
    if dif < 0.2:
        return 1
    else:
        return 0


def reputation_c(truthtable):
    alpha = 0.5
    initialReputation = 0.5
    r1 = initialReputation + truthtable.sumTruth
    print ("Sumatorio de truth_i anteriores ", truthtable.sumTruth)
    print ("Último valor de truth ", truthtable.truth)
    print ("Valor de r1 = ", r1)
    if truthtable.nTimes == 0:
        r2 = r1 - truthtable.repAnt + math.exp(-(1-truthtable.truth))
    else:
        r2 = r1 - truthtable.repAnt/truthtable.nTimes + math.exp(-(1-truthtable.truth)*truthtable.nTimes)

    if truthtable.truth >= alpha:
        truthtable.repAnt = r1
        if truthtable.nTimes == 0:
            return r1
        else:
            return r1/truthtable.nTimes
    else:
        truthtable.repAnt = r2
        if truthtable.nTimes == 0:
            return r2
        else:
            return r2/truthtable.nTimes

def reputation_d(carretera):
    alpha = 0.5
    initialReputation = 0.5
    r1 = initialReputation + carretera[10]
    print ("Sumatorio de truth_i anteriores ", carretera[10])
    print ("Último valor de truth ", carretera[11])
    print ("Valor de r1 = ", r1)
    if carretera[8] == 0:
        r2 = r1 - carretera[9] + math.exp(-(1-carretera[11]))
    else:
        r2 = r1 - carretera[9]/carretera[8] + math.exp(-(1-carretera[11])*carretera[8])

    if carretera[11] >= alpha:
        carretera[9] = r1
        if carretera[8] == 0:
            return r1
        else:
            return r1/carretera[8]
    else:
        carretera[9] = r2
        if carretera[8] == 0:
            return r2
        else:
            return r2/carretera[8]



def trust(reputation, truth):
    gamma = 0.3
    return gamma*truth + (1-gamma)*reputation


def true_false_carretera(datos, carretera, hora, array_carretera, truthtable, addr):

    if len(array_carretera) == 0:
        print ("No se han obtenido datos de la congestión, no se ejecuta ésta función")

    else:
        for c in datos.carreteras:
            if carretera == c.nombre:
                if len(c.congestion) == 0:
                    print ("No hay datos de la congestión en la carretera para comparar")
                    truth_carretera = 0.5
                else:
                    cont2 = 0
                    for carr in c.congestion:
                        if hora == carr.hora:
                            cont2 += 1
                            congestion_carretera_teorica = carr.coeficiente/carr.nTimes
                            congestion_carretera_real = array_carretera[1]
                            print ("Congestión carretera teórica = ", congestion_carretera_teorica)
                            print ("Congestión carretera real = ", congestion_carretera_real)
                            truth_carretera = truth(congestion_carretera_teorica, congestion_carretera_real)
                            break
                        else:
                            continue
                    if cont2 == 0:
                        print ("No hay datos de la congestión de la carretera a esta hora")
                        truth_carretera = 0.5

            else:
                continue

        for t in truthtable.evaluaciones:
            if t.id == addr:
                t.truth = truth_carretera
                t.sumTruth += truth_carretera
                t.nTimes += 1
                break
            else:
                continue

    array_carretera = []
    print ("Array de carreteras vaciado: ", array_carretera)




#ALMACENAMIENTO DE ARRAYS VOLÁTILES EN ARRAY PRINCIPAL


def almacenamiento_carreteras(datos, carretera, array_carretera, myhour, congestion, truthtable, trust_c, addr):

    cont = 0
    for t in truthtable.evaluaciones:
        if t.id == addr:
            truth = t.truth
            rep = reputation_c(t)
            trust_c = trust(rep, truth)
            break
        else:
            continue
    if cont == 0:
        evaluacion = definicion_clases.Evaluacion(addr, 0.5, 0, 1, 0.5)
        truthtable.agregarEvaluaciones(evaluacion)

    cont = 0
    if len(array_carretera) == 0:
        print ("Array de carreteras vacío")
        for c in datos.carreteras:
            if carretera  == c.nombre:
                print ("La carretera ya está registrada")
                cont2 = 0
                cont += 1
                if trust_c < 0.5:
                    print ("No es una información de confianza, no se almacenan valores")
                    break
                else:
                    for t in c.congestion:
                        print ("Hora almacenada: ", t.hora)
                        if myhour == t.hora:
                            print("Ya hay información a esta hora")
                            t.coeficiente += congestion
                            t.nTimes += 1
                            cont2 += 1
                            break
                        else:
                            continue
                    if cont2 == 0:
                        print ("No hay información a esta hora, la añado")
                        cong = definicion_clases.Congestion(myhour, congestion, 1)
                        c.agregarCongestion(cong)
                        cont += 1
                        cont2 = 0
                        break
            else:
                continue
        if cont == 0:
            cong = definicion_clases.Congestion(myhour, congestion, 1)
            carr = definicion_clases.Carretera(carretera, [], [], [])
            datos.agregar_carreteras(carr)
            cont = 0
    else:
        cont = 0
        for c in datos.carreteras:
            print ("Carretera del array carreteras: ", array_carretera[0])
            print ("Carretera del array datos, ", c.nombre)
            if array_carretera[0] == c.nombre:
                print ("Analizando carretera:", c.nombre)
                cont2 = 0
                cont += 1
                if trust_c < 0.5:
                    print ("No es una información de confianza, no se almacenan valores")
                    break
                else:
                    for t in c.congestion:
                        if myhour == t.hora:
                            t.coeficiente += 0.8*congestion + 0.2*float(array_carretera[1])
                            t.nTimes += 1
                            cont += 1
                            cont2 += 1
                            print ("Valores introducidos de la congestión en la carretera= ", t)
                            break
                        else:
                            continue
                    if cont2 == 0:
                        cong = definicion_clases.Congestion(int(myhour), 0.8*congestion + 0.2*float(array_carretera[1]), 1)
                        c.agregarCongestion(cong)
                        cont2 = 0
                        cont += 1
                        break
                    print ("Contador = ", cont)

            else:
                continue
        if cont == 0:
            cong = definicion_clases.Congestion(int(myhour), 0.8*congestion + 0.2*float(array_carretera[1]), 1)
            carr = definicion_clases.Carretera(array_carretera[0], [], [], [])
            carr.agregarCongestion(cong)
            datos.agregar_carreteras(carr)
            cont = 0
    datos.mostrarInfo()



def almacenamiento_destinos(datos, array_destinos, myhour):

    print ("Almacenamiento destinos...")
    print (array_destinos)
    print ("Longitud del array destinos = ", len(array_destinos))
    if len(array_destinos) == 0:
        print ("Array de destinos vacío")
    else:
        print ("Array de destinos no vacío")
        print (array_destinos)
        cont = 0
        for c in datos.carreteras:
            print ("Analizando destino desde carretera: ", array_destinos[0])
            print ("Carretera guardada: ", c.nombre)
            if array_destinos[0] == c.nombre:
                print ("Destino detectado desde mi carretera")
                cont += 1
                if len(c.destino) == 0:
                    print ("No hay destinos almacenados, añadimos")
                    dest = definicion_clases.Destino(array_destinos[1], myhour, 1)
                    c.agregarDestino(dest)
                    cont += 1
                    break
                else:
                    cont2 = 0
                    cont3 = 0
                    for d in c.destino:
                        if array_destinos[1] == d.destino:
                            cont2 += 1
                            print ("Ya tengo información anterior acerca de este destino")
                            if d.hora == myhour:
                                print ("Ya tengo información anterior acerca de este destino a esta hora")
                                d.nCoches += 1
                                cont3 += 1
                                cont += 1
                                break
                            else:
                                continue
                        else:
                            continue
                    if cont3 == 0:
                        dest = definicion_clases.Destino(array_destinos[1], myhour, 1)
                        c.agregarDestino(dest)
                        cont2 += 1
                        cont += 1
                        cont3 = 0
                        print ("No tengo información del destino a esta hora, la añado")

                    if cont2 == 0:
                        dest = definicion_clases.Destino(array_destinos[1], myhour, 1)
                        c.agregarDestino(dest)
                        cont2 = 0
                        cont += 1
            else:
                continue
        if cont == 0:
            print ("La carretera no está registrada, la añado")
            dest = definicion_clases.Destino(array_destinos[1], myhour, 1)
            carr = definicion_clases.Carretera(array_destinos[0], [], [], [])
            carr.agregarDestino(dest)
            datos.agregar_carreteras(carr)
            cont = 0
    datos.mostrarInfo()


def almacenamiento_nTimes(datos, carretera, myhour):

    for c in datos.carreteras:
        print ("Analizando carretera: ", c.nombre)
        print ("Mi carretera: ", carretera)
        if carretera == c.nombre:
            print ("nTimes: La carretera está registrada")
            if len(c.hora) == 0:
                h = definicion_clases.Hora(myhour, 1)
                c.agregarHora(h)
                break
            cont = 0
            for n in c.hora:
                if myhour == n.hora:
                    print ("nTimes: Ya hay info a esta hora")
                    n.nTimes += 1
                    cont += 1
                    break
                else:
                    print ("nTimes: No hay info a esta hora")
                    continue
            if cont == 0:
                h = definicion_clases.Hora(myhour, 1)
                c.agregarHora(h)
                break
        else:
            print ("nTimes: la carretera no está registrada")


def almacenamiento_array_principal(datos, carretera, array_destinos, array_carretera, nCoches,  moment, truthtable, addr):

    now = datetime.datetime.now()
    myhour = now.hour
    congestion = calcular_congestion_carretera(nCoches, moment)
    print ("Congestión calculada en este tramo = ", congestion)
    print ("Hora actual = ", myhour)
    print ("Array carretera: ", array_carretera)
    print ("Array_destinos: ", array_destinos)


    cont = 0
    for t in truthtable.evaluaciones:
        if t.id == addr:
            truth = t.truth
            rep = reputation_c(t)
            trust_c = trust(rep, truth)
            break
        else:
            continue
    if cont == 0:
        trust_c = 0.5
        evaluacion = definicion_clases.Evaluacion(addr, 0, 0, 0, 0.5)
        truthtable.agregarEvaluaciones(evaluacion)


    cont = 0

    if len(datos.carreteras) == 0:
        print ("La longitud del array de datos es 0")
        if len(array_destinos) == 0 and len(array_carretera) == 0:
            print ("Ambos arrays vacíos")
            cong = definicion_clases.Congestion(myhour, congestion, 1)
            h = definicion_clases.Hora(myhour, 1)
            carr = definicion_clases.Carretera(carretera, [], [], [])
            carr.agregarCongestion(cong)
            carr.agregarHora(h)
            datos.agregar_carreteras(carr)

        elif len(array_carretera) == 0 and len(array_destinos) != 0:
            print ("Array carreteras vacío, array destinos no vacío")
            cong = definicion_clases.Congestion(myhour, congestion, 1)
            h = definicion_clases.Hora(myhour, 1)
            dest = definicion_clases.Destino(array_destinos[1], myhour, 1)
            carr = definicion_clases.Carretera(carretera, [], [], [])
            carr.agregarCongestion(cong)
            carr.agregarDestino(dest)
            carr.agregarHora(h)
            datos.agregar_carreteras(carr)

        elif len(array_carretera) != 0 and len(array_destinos) == 0:
            print ("Array destinos vacío, array carreteras no vacío")
            cong = definicion_clases.Congestion(myhour, 0.8*congestion + 0.2*float(array_carretera[1]), 1)
            h = definicion_clases.Hora(myhour, 1)
            carr = definicion_clases.Carretera(carretera, [], [], [])
            carr.agregarCongestion(cong)
            carr.agregarHora(h)
            datos.agregar_carreteras(carr)

        else:
            print ("Ambos arrays no vacíos")
            cong = definicion_clases.Congestion(myhour, 0.8*congestion + 0.2*float(array_carretera[1]), 1)
            h = definicion_clases.Hora(myhour, 1)
            dest = definicion_clases.Destino(array_destinos[1], myhour, 1)
            carr = definicion_clases.Carretera(carretera, [], [], [])
            carr.agregarCongestion(cong)
            carr.agregarDestino(dest)
            carr.agregarHora(h)
            datos.agregar_carreteras(carr)

    else:
        almacenamiento_carreteras(datos, carretera, array_carretera, myhour, congestion, truthtable, trust_c, addr)
        almacenamiento_destinos(datos, array_destinos, myhour)
        almacenamiento_nTimes(datos, carretera, myhour)

    array_destinos = []
    print ("Array de destinos vaciado: ", array_destinos)
    datos.mostrarInfo()


