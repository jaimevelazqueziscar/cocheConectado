En esta carpeta encontramos distintos archivos gracias a los cuales se pueden ejecutar todos los algoritmos diseñados.

Los ficheros "common.py", "gstreamer.py" y "detect.py" se utilizan para la detección en tiempo real de vehículos en la vía pública. Se requiere una cámara para poder ejecutar los archivos. Los ficheros "connection.py" y "fsm_semaforo.py" son los necesarios en el algoritmo del semáforo para que las tareas se lleven a cabo adecuadamente. Por su parte, "info_coches.py" y "fsm_coches.py" se utilizan para la comunicación inter-coches. Por último, el fichero "definicion_clases.py" define las distintas clases a crear para que el almacenamiento de la información recopilada se realice correctamente.

Por otra parte, encontramos distintos ficheros .txt que conviene explicar. "nCoches.txt" almacena el número de coches detectados en cada proceso de comunicación. A partir de aquí, podremos calcular fácilmente el grado de congestión en la carretera. Es una variable compartida por el algoritmo de detección de coches y comunicación inter-coches. 

"prioridad_bt.txt" almacena el valor de la variable priority, que regula la integración de los tres algoritmos en un mismo sistema final de forma que se ejecute cada uno de ellos en el momento oportuno.

"velocidad.txt" almacena la velocidad del vehículo. De esta forma, podremos saber cuándo está parado en un semáforo, y activar el consiguiente algoritmo.

Por último, el fichero "tfg.sh" permite la ejecución simultánea de todos los algoritmos en la terminal. Bastará la orden "bash tfg.sh" para comenzar a correr el programa completo.

