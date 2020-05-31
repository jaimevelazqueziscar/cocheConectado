import definicion_clases


def almacenamientoFatigaInicio(arrayFatiga, carretera, fatigaInicio):

    arrayFatiga.append([carretera, fatigaInicio, 0])

def almacenamientoFatigaFinal(arrayFatiga, carretera, fatigaFin):

    for ev in arrayFatiga:
        if ev[0] == carretera:
            ev[2] = fatigaFin
            break


def calculoAlmacenamientoCalidad(arrayFatiga, array_evaluaciones, hora, destino):

    for ev in arrayFatiga:
        print ("Almacenando carretera: ", ev[0])
        if ev[0] == destino:
            print ("Ya he llegado a mi destino, no se almacena")
        else:
            carretera = ev[0]
            fatigaInicial = float(ev[1])
            fatigaFinal = float(ev[2])
            umbralFatiga = 0.4
            difFatiga = fatigaFinal - fatigaInicial
            print ("DifFatiga = ", difFatiga)
    
            if difFatiga > umbralFatiga:
                print ("La carretera me produce fatiga")
                calidad = 0
            else:
                print ("Estaba más fatigado antes de entrar en la carretera que ahora")
                calidad = 1

            evaluacion = definicion_clases.PostEvaluation(carretera, hora, calidad)
            array_evaluaciones.agregarEvaluaciones(evaluacion)

    arrayFatiga = []


def compruebaDecisionesAnteriores(array_evaluaciones, carretera, hora):

    umbralCalidad = 0.5

    for ev in array_evaluaciones:
        if ev[0] == carretera:
            if ev[1] == hora:
                calidad += ev[2]
                nTimes += 1
    
    if calidad/nTimes < umbralCalidad:
        print ("NO ES BUENA DECISIÓN PASAR POR AQUÍ")
    else:
        print ("ES BUENA DECISIÓN PASAR POR AQUÍ")





    



