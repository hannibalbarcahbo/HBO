function [HA_score, HA_pos, Convergence_curve] = HBO(warriors_no, Max_iter, lb, ub, dim, fobj)
    %% HBO - Hannibal's Battle Optimization Algorithm
    % Optimized version with improved structure and reduced code duplication
    
    %% Initialize global variables
    HA_pos = zeros(1, dim);
    HA_score = inf;
    Rom_Gen = zeros(1, dim);
    Rom_score = inf;
    Convergence_curve = zeros(1, Max_iter);
    
    %% Initialize populations
    roman_rate = 0.63;
    romans_no = round(warriors_no * roman_rate);
    cartagos_no = warriors_no - romans_no;
    
    [romans, cartagos, romans_fitness, cartagos_fitness] = initializePopulations(...
        romans_no, cartagos_no, dim, lb, ub, fobj);
    
    %% Sort and divide populations into strategic groups
    [left_romans, right_romans, center_romans] = divideRomans(romans, romans_fitness);
    [left_cartagos, right_cartagos, center_cartagos] = divideCartagos(cartagos, cartagos_fitness);
    
    %% Main optimization loop
    for it = 1:Max_iter
        % Determine battle phase based on iteration
        phase = getBattlePhase(it, Max_iter);
        
        % Execute battle strategies based on phase
        [left_romans, right_romans, center_romans, left_cartagos, right_cartagos, center_cartagos, ...
         HA_score, HA_pos, Rom_score, Rom_Gen] = executeBattlePhase(phase, ...
            left_romans, right_romans, center_romans, left_cartagos, right_cartagos, center_cartagos, ...
            Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj);
        
        % Display progress and store convergence
        fprintf('Iteration #%d, Best objective = %.6e\n', it, HA_score);
        Convergence_curve(it) = HA_score;
    end
    
   
end

function [romans, cartagos, romans_fitness, cartagos_fitness] = initializePopulations(romans_no, cartagos_no, dim, lb, ub, fobj)
    %% Initialize and evaluate both populations
    romans = initialization(romans_no, dim, ub, lb);
    cartagos = initialization(cartagos_no, dim, ub, lb);
    
    romans_fitness = evaluatePopulation(romans, fobj);
    cartagos_fitness = evaluatePopulation(cartagos, fobj);
end

function fitness = evaluatePopulation(population, fobj)
    %% Evaluate fitness for entire population
    fitness = zeros(1, size(population, 1));
    for i = 1:size(population, 1)
        fitness(i) = fobj(population(i, :));
    end
end

function [left_group, right_group, center_group] = divideRomans(romans, romans_fitness)
    %% Divide Romans into strategic groups (best 3% each for left/right)
    [~, sorted_indices] = sort(romans_fitness);
    sorted_romans = romans(sorted_indices, :);
    
    percent_3 = max(1, round(0.03 * size(romans, 1)));
    left_group = sorted_romans(1:percent_3, :);
    right_group = sorted_romans(percent_3+1:min(2*percent_3, size(romans,1)), :);
    center_group = sorted_romans(2*percent_3+1:end, :);
end

function [left_group, right_group, center_group] = divideCartagos(cartagos, cartagos_fitness)
    %% Divide Carthaginians into strategic groups (worst 12% each for left/right) 
    [~, sorted_indices] = sort(cartagos_fitness, 'descend');
    sorted_cartagos = cartagos(sorted_indices, :);
    
    percent_12 = max(1, round(0.12 * size(cartagos, 1)));
    left_group = sorted_cartagos(1:percent_12, :);
    right_group = sorted_cartagos(percent_12+1:min(2*percent_12, size(cartagos,1)), :);
    center_group = sorted_cartagos(2*percent_12+1:end, :);
end

function phase = getBattlePhase(iteration, max_iter)
    %% Determine current battle phase
    if iteration <= 0.33 * max_iter
        phase = 1; % Early phase - all attacks
    elseif iteration <= 0.66 * max_iter
        phase = 2; % Middle phase - strategic retreats
    else
        phase = 3; % Final phase - encirclement
    end
end

function [left_romans, right_romans, center_romans, left_cartagos, right_cartagos, center_cartagos, ...
          HA_score, HA_pos, Rom_score, Rom_Gen] = executeBattlePhase(phase, ...
    left_romans, right_romans, center_romans, left_cartagos, right_cartagos, center_cartagos, ...
    Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj)
    
    switch phase
        case 1 % Early phase: All attacks
            [right_cartagos, left_romans, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
                executeAttack(@right_attack, right_cartagos, left_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj);
            
            [left_cartagos, right_romans, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
                executeAttack(@left_attack, left_cartagos, right_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj);
            
            [center_cartagos, center_romans, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
                executeAttack(@center_attack, center_cartagos, center_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj);
            
        case 2 % Middle phase: Strategic retreats
            [right_cartagos, left_romans, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
                executeAttack(@right_attack, right_cartagos, left_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj);
            
            [left_cartagos, left_romans, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
                executeAttack(@left_attack, left_cartagos, left_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj);
            
            % Right Romans retreat
            [right_romans, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
                executeRetreat(right_romans, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj);
            
            [center_cartagos, center_romans, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
                executeAttack(@center_attack, center_cartagos, center_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj);
            
        case 3 % Final phase: Encirclement
            [right_cartagos, center_romans, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
                executeAttack(@right_attack, right_cartagos, center_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj);
            
            % Left Romans retreat
            [left_romans, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
                executeRetreat(left_romans, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj);
            
            [left_cartagos, center_romans, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
                executeAttack(@left_attack, left_cartagos, center_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj);
            
            % Right Romans retreat  
            [right_romans, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
                executeRetreat(right_romans, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj);
            
            [center_cartagos, center_romans, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
                executeAttack(@center_attack, center_cartagos, center_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj);
    end
end

function [attackers, defenders, HA_score, HA_pos, Rom_score, Rom_Gen] = executeAttack(...
    attack_func, attackers, defenders, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj)
    %% Execute attack and update positions for both groups
    
    % Perform attack
    [attackers, defenders] = attack_func(attackers, defenders, Rom_Gen, HA_pos);
    
    % Evaluate and update attackers
    [attackers, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
        evaluateAndUpdate(attackers, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj);
    
    % Evaluate and update defenders  
    [defenders, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
        evaluateAndUpdate(defenders, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj);
end

function [retreaters, HA_score, HA_pos, Rom_score, Rom_Gen] = executeRetreat(...
    retreaters, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj)
    %% Execute retreat maneuver (random movement)
    
    for i = 1:size(retreaters, 1)
        retreaters(i, :) = retreaters(i, :) + randn(1, size(retreaters, 2)) .* (ub - lb);
    end
    
    [retreaters, HA_score, HA_pos, Rom_score, Rom_Gen] = ...
        evaluateAndUpdate(retreaters, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj);
end

function [population, HA_score, HA_pos, Rom_score, Rom_Gen] = evaluateAndUpdate(...
    population, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj)
    %% Evaluate population and update best solutions
    
    for i = 1:size(population, 1)
        % Enforce bounds
        population(i, :) = enforceBounds(population(i, :), ub, lb);
        
        % Evaluate fitness
        fitness = fobj(population(i, :));
        
        % Update best solutions
        if fitness < HA_score
            HA_score = fitness;
            HA_pos = population(i, :);
        elseif fitness < Rom_score
            Rom_score = fitness;
            Rom_Gen = population(i, :);
        end
    end
end

