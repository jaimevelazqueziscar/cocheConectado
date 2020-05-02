clear

%% Análisis de los campos verdes, prueba final latencia

%% Inicialización de variables

%iteration: array que contiene el número de cada iteración
%value: valor de los campos verdes en cada iteración

iteration = 1:12;
value = [267.8 90 116.3 257.96 126 84 75 95.5 260.4 109 85.8 56];


%% Representación

plot(iteration, value, '-go', 'linewidth', 2, 'markeredgecolor', 'b');
grid minor;
title('Análisis de los tiempos de respuesta de las celdas verdes');
xlabel('Iteración');
ylabel('Tiempo (ms)');
axis([1 12 50 300]);
