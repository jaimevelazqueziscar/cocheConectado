
%% Inicializaci�n de variables

%gamma: determina el peso del indicador de verdad y de la reputaci�n en el c�lculo del indicador de confianza
%threshold: umbral de decisi�n de valores de Trtuh positivos y negativos
%Etruth: sumatorio de los indicadores de verdad anteriores
%Ttrust: array que almacena todos los indicadores de confianza calculados
%Trep: array que almacena todos los indicadores de reputaci�n calculados
%Ttruth: array que almacena los indicadores de verdad a la entrada


clear
gamma = 0.3;
threshold = 0.5;
Etruth = 0;
Ttrust = [];
Trep = [];
Ttruth = [1 1 1 0.5 1 1 0.5 0.5 1 1 0 0.5 0.5 1 0.5 0.5 1 0.5 1 1 0 0 1 0 0.5 1 1 0.5 0.5 1 0 0.5 1 1];

%% C�digo

for i = 1:length(Ttruth)
    if i == 1
        Trep(i) = (reputation(0.5, i, Etruth, 0.5))/i;
        Ttrust(i) = gamma*0.5+(1-gamma)*0.5;

    else
        Trep(i) = (reputation(Ttruth(i-1), i, Etruth, Trep(i-1)))/i;
        Ttrust(i) = gamma*Ttruth(i-1)+(1-gamma)*Trep(i-1);
    end
    Etruth = Etruth + Ttruth(i);
end;


%% Representaci�n de la reputaci�n y confianza en funci�n de Truth

x = 1:length(Ttruth);
subplot(2,1,1)

f = fit(x(:), Trep(:), 'cubicinterp');
plot(f, x, Trep)
grid on
title('Evoluci�n de la reputaci�n');
xlabel('Instante de tiempo');
ylabel('Reputaci�n');
hold on 
plot([0, length(Ttruth)], [threshold, threshold], '--g')

for i = 1:length(Ttruth)
    txt = num2str(Ttruth(i));
    text(i, Trep(i) - 0.04, txt);
end;

axis([0 length(Ttruth)+1 0.3 1])
hold off

subplot(2,1,2)

f = fit(x(:), Ttrust(:), 'cubicinterp')
plot(f, x, Ttrust)
grid on
title('Evoluci�n de la confianza');
xlabel('Instante de tiempo');
ylabel('Confianza');
hold on 
plot([0, length(Ttruth)], [threshold, threshold], '--g')

for i = 1:length(Ttruth)
    txt = num2str(Ttruth(i));
    text(i, Ttrust(i)-0.04, txt);
end;
axis([0 length(Ttruth)+1 0.3 1])

hold off
