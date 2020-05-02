
%% Inicialización de variables

%gamma: determina el peso del indicador de verdad y de la reputación en el cálculo del indicador de confianza
%threshold: umbral de decisión de valores de Trtuh positivos y negativos
%Etruth: sumatorio de los indicadores de verdad anteriores
%Ttrust: array que almacena todos los indicadores de confianza calculados
%Trep: array que almacena todos los indicadores de reputación calculados
%Ttruth: array que almacena los indicadores de verdad a la entrada


clear
gamma = 0.3;
threshold = 0.5;
Etruth = 0;
Ttrust = [];
Trep = [];
Ttruth = [1 1 1 0.5 1 1 0.5 0.5 1 1 0 0.5 0.5 1 0.5 0.5 1 0.5 1 1 0 0 1 0 0.5 1 1 0.5 0.5 1 0 0.5 1 1];

%% Código

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


%% Representación de la reputación y confianza en función de Truth

x = 1:length(Ttruth);
subplot(2,1,1)

f = fit(x(:), Trep(:), 'cubicinterp');
plot(f, x, Trep)
grid on
title('Evolución de la reputación');
xlabel('Instante de tiempo');
ylabel('Reputación');
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
title('Evolución de la confianza');
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
