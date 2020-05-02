clear

%% An�lisis de los campos verdes, prueba final latencia

%% Inicializaci�n de variables

%iteration: array que contiene el n�mero de cada iteraci�n
%value: valor de los campos verdes en cada iteraci�n

iteration = 1:12;
value = [267.8 90 116.3 257.96 126 84 75 95.5 260.4 109 85.8 56];


%% Representaci�n

plot(iteration, value, '-go', 'linewidth', 2, 'markeredgecolor', 'b');
grid minor;
title('An�lisis de los tiempos de respuesta de las celdas verdes');
xlabel('Iteraci�n');
ylabel('Tiempo (ms)');
axis([1 12 50 300]);
