

%% Resultados de reputación y confianza de la simulación del modo semáforo
clear
threshold = 0.5;

% Para un valor de verdad de todo 1's

x = 1:9;

A = importdata('resultados_1s.txt');

subplot(2,1,1)

a = A(:, 1)
f = fit(x(:), a(:), 'cubicinterp');
plot(f, x, a)
grid on
title('Evolución de la reputación con unos a la entrada');
xlabel('Instante de tiempo');
ylabel('Reputación');
hold on 
plot([0, 18], [threshold, threshold], '--g')
hold off
axis([0 9 0.3 1])

subplot(2,1,2)

a = A(:, 1)
f = fit(x(:), a(:), 'cubicinterp')
plot(f, x, a)
grid on
title('Evolución de la confianza con unos a la entrada');
xlabel('Instante de tiempo');
ylabel('Confianza');
hold on 
plot([0, 18], [threshold, threshold], '--g')
hold off
axis([0 9 0.3 1])


% Para un valor de verdad de todo 0's
figure

x = 1:9;

A = importdata('resultados_0s.txt');

subplot(2,1,1)

a = A(:, 1)
f = fit(x(:), a(:), 'cubicinterp')
plot(f, x, a)
grid on
title('Evolución de la reputación con ceros a la entrada');
xlabel('Instante de tiempo');
ylabel('Reputación');
hold on 
plot([0, 18], [threshold, threshold], '--g')
hold off
axis([0 9 0 0.7])

subplot(2,1,2)

a = A(:, 1)
f = fit(x(:), a(:), 'cubicinterp')
plot(f, x, a)
grid on
title('Evolución de la confianza con ceros a la entrada');
xlabel('Instante de tiempo');
ylabel('Confianza');
hold on 
plot([0, 18], [threshold, threshold], '--g')
hold off
axis([0 9 0 0.7])



% Para un valor de verdad de todo 0.5's
figure

x = 1:9;

A = importdata('resultados_05s.txt');

subplot(2,1,1)

a = A(:, 1)
f = fit(x(:), a(:), 'cubicinterp')
plot(f, x, a)
grid on
title('Evolución de la reputación con 0,5 a la entrada');
xlabel('Instante de tiempo');
ylabel('Reputación');
hold on 
plot([0, 18], [threshold, threshold], '--g')
hold off
axis([0 9 0 1])

subplot(2,1,2)

a = A(:, 1);
f = fit(x(:), a(:), 'cubicinterp');
plot(f, x, a)
grid on
title('Evolución de la confianza con 0,5 a la entrada');
xlabel('Instante de tiempo');
ylabel('Confianza');
hold on 
plot([0, 18], [threshold, threshold], '--g')
hold off
axis([0 9 0 1])

% Para valores alternados de 1 y 0

figure

x = 1:17;

A = importdata('resultados_1_0_1.txt');

subplot(2,1,1)

a = A(:, 1);
f = fit(x(:), a(:), 'cubicinterp');
plot(f, x, a)
grid on
title('Evolución de la reputación con 1s y 0s a la entrada');
xlabel('Instante de tiempo');
ylabel('Reputación');
hold on 
plot([0, 18], [threshold, threshold], '--g')
plot([5, 5], [0.2, 1], '--b')
plot([12, 12], [0.2, 1], '--b')
txt1 = 'Truth = 1';
txt2 = 'Truth = 0';
text(1, 0.3, txt1);
text(7, 0.3, txt2);
text(14, 0.3, txt1);
hold off
axis([0 17 0.2 1])
legend('Valores tomados', 'Curva de la reputación', 'Umbral', 'Cambio de 1 a 0')

subplot(2,1,2)

a = A(:, 1);
f = fit(x(:), a(:), 'cubicinterp');
plot(f, x, a)
grid on
title('Evolución de la confianza con 1s y 0s a la entrada');
xlabel('Instante de tiempo');
ylabel('Confianza');
hold on 
plot([0, 18], [threshold, threshold], '--g')
plot([5, 5], [0.2, 1], '--b')
plot([12, 12], [0.2, 1], '--b')
txt1 = 'Truth = 1';
txt2 = 'Truth = 0';
text(1, 0.3, txt1);
text(7, 0.3, txt2);
text(14, 0.3, txt1);
hold off
axis([0 17 0.2 1])
legend('Valores tomados', 'Curva de la confianza', 'Umbral', 'Cambio de 1 a 0')

