clear

%% Inicialización de variables

%n: array que almacena el número de coches a la entrada en cada
%instante de tiempo
%t: array que almacena el tiempo de procesamiento medido para cada instante
%de tiempo

n = [1, 2, 3, 5, 8, 14, 20];

t = [49.02, 84.29, 145.81, 216.88, 413.56, 717.36, 937.01];

%% Representación

f = fit(n(:), t(:), 'linear');
plot(f, n, t)
grid on
title('Tiempos de prcesamiento y envío del semáforo');
xlabel('Número de coches');
ylabel('Tiempo empleado (ms)');

x1 = linspace(0, 20);
p = polyfit(n, t, 1);
f1 = polyval(p, x1);

hold on
plot(x1, f1, 'r--')