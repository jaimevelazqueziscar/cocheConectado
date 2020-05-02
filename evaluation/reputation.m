
%% Entradas

%Truth: indicador de verdad en el instante actual
%nTimes: número de veces que hemos calculado el indicador de verdad
%sum_truth: sumatorio de todos los indicadores de verdad calculados anteriormente
%rep_ant = reputación en el instante anterior

%% Salidas

%rep: valor de la reputación en el instante actual

%% Código

function rep = reputation(truth, nTimes, sum_truth, rep_ant)


if (truth >= 0.5)
    rep = 0.5 + sum_truth; 
else 
    rep = 0.5 + sum_truth - (rep_ant - exp(-nTimes*(1-truth)));
end
end

