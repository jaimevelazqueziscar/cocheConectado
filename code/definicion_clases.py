import pickle


class Congestion:

    def __init__(self, hora, coeficiente, nTimes):
        self.hora = hora
        self.coeficiente = coeficiente
        self.nTimes = nTimes

    def __str__(self):
        return "{} {} {}".format(self.hora, self.coeficiente, self.nTimes)



class Destino:

    def __init__(self, destino, hora, nCoches):
        self.destino = destino
        self.hora = hora
        self.nCoches = nCoches

    def __str__(self):
        return "{} {} {}".format(self.destino, self.hora, self.nCoches)


class Hora:

    def __init__(self, hora, nTimes):
        self.hora = hora
        self.nTimes = nTimes

    def __str__(self):
        return "{} {}".format(self.hora, self.nTimes)


class Carretera:

    def __init__(self, nombre, congestion, destino, hora):
        self.nombre = nombre
        self.congestion = congestion
        self.destino = destino
        self.hora = hora

    def __str__(self):
        return "{} {} {} {}".format(self.nombre, self.congestion, self.destino, self.hora)

    congestion = []
    hora = []
    destino = []

    def agregarCongestion(self, c):
        self.congestion.append(c)

    def agregarHora(self, h):
        self.hora.append(h)

    def agregarDestino(self, d):
        self.destino.append(d)


class datos:

    carreteras=[]

    def cargarDatos(self):
        listaDeCarreteras=open("../store/array_datos.txt", "ab+")
        listaDeCarreteras.seek(0)

        try:
            self.carreteras = pickle.load(listaDeCarreteras)
        except:
            print (" ")
        finally:
            listaDeCarreteras.close()

    def agregar_carreteras(self, c):
        cont = 0
        for carr in self.carreteras:
            if carr.nombre == c.nombre:
                cont += 1
                break
        if cont == 0:
            self.carreteras.append(c)
            self.guardarCarreteras()

    def mostrarCarreteras(self):
        for c in self.carreteras:
            print(c)

    def guardarCarreteras(self):
        listaDeCarreteras=open("../store/array_datos.txt", "wb")
        pickle.dump(self.carreteras, listaDeCarreteras)
        listaDeCarreteras.close()

    def mostrarInfo(self):
        print("La información almacenada es la siguiente:")
        for c in self.carreteras:
            print ("\nCarretera: ")
            print (c.nombre)
            print ("Congestiones: ")
            for cong in c.congestion:
                print (cong)
            print ("Destinos: ")
            for d in c.destino:
                print(d)
            print("Horas:")
            for h in c.hora:
                print(h)


class Evaluacion:

    def __init__(self, id, sumTruth, repAnt, nTimes, truth):
        self.id = id
        self.sumTruth = sumTruth
        self.repAnt = repAnt
        self.nTimes = nTimes
        self.truth = truth

    def __str__(self):
        return "{} {} {} {}".format(self.id, self.sumTruth, self.repAnt, self.nTimes, truth)


class EvalSemaforo:

    def __init__(self, id, sumTruth, repAnt, nTimes,difTime, difVel, truth):
        self.id = id
        self.sumTruth = sumTruth
        self.repAnt = repAnt
        self.nTimes = nTimes
        self.difTime = difTime
        self.difVel = difVel
        self.truth = truth

    def __str__(self):
        return "{} {} {} {}".format(self.id, self.sumTruth, self.repAnt, self.nTimes, self.difTime, self.difVel, self.truth)



class truthtable:

    evaluaciones = []

    def cargarDatos(self):
        listaDeEvaluaciones=open("../store/array_truth.txt", "ab+")
        listaDeEvaluaciones.seek(0)

        try:
            self.evaluaciones = pickle.load(listaDeEvaluaciones)
        except:
            print (" ")
        finally:
            listaDeEvaluaciones.close()

    def agregarEvaluaciones(self, e):
        cont = 0
        for ev in self.evaluaciones:
            if ev.id == e.id:
                cont += 1
                break
        if cont == 0:
            self.evaluaciones.append(e)
            self.guardarCarreteras()

    def mostrarCarreteras(self):
        for e in self.evaluaciones:
            print(e)

    def guardarCarreteras(self):
        listaDeEvaluaciones=open("../store/array_truth.txt", "wb")
        pickle.dump(self.evaluaciones, listaDeEvaluaciones)
        listaDeEvaluaciones.close()

    def mostrarInfo(self):
        print("La información almacenada es la siguiente:")
        for e in self.evaluaciones:
            print ("\n ", e.id, " ", e.sumTruth, " ", e.repAnt, " ", e.nTimes, " ", e.truth)



class truthSemaforo:

    evaluaciones = []

    def cargarDatos(self):
        listaDeEvaluaciones=open("../store/truth_semaforo.txt", "ab+")
        listaDeEvaluaciones.seek(0)

        try:
            self.evaluaciones = pickle.load(listaDeEvaluaciones)
        except:
            print (" ")
        finally:
            listaDeEvaluaciones.close()

    def agregarEvaluaciones(self, e):
        cont = 0
        for ev in self.evaluaciones:
            if ev.id == e.id:
                cont += 1
                break
        if cont == 0:
            self.evaluaciones.append(e)
            self.guardarCarreteras()


    def mostrarEvaluaciones(self):
        for e in self.evaluaciones:
            print(e)

    def guardarEvaluaciones(self):
        listaDeEvaluaciones=open("../store/truth_semaforo.txt", "wb")
        pickle.dump(self.evaluaciones, listaDeEvaluaciones)
        listaDeEvaluaciones.close()

    def mostrarInfo(self):
        print("La información almacenada es la siguiente:")
        for e in self.evaluaciones:
            print ("\n ", e.id, " ", e.sumTruth, " ", e.repAnt, " ", e.nTimes, " ", e.difTime, " ", e.difVel, " ",  e.truth)

