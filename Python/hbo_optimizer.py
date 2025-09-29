import numpy as np
from initialization import initialization
from attack_strategies import left_attack, right_attack, center_attack
from utils import enforce_bounds, parallaxe

def HBO(warriors_no, max_iter, lb, ub, dim, fobj):
    """
    Hannibal Barca Optimizer (HBO) - Main Algorithm
    
    Parameters:
    - warriors_no: Number of search agents
    - max_iter: Maximum number of iterations
    - lb, ub: Lower and upper bounds
    - dim: Problem dimension
    - fobj: Objective function
    
    Returns:
    - HA_score: Best fitness value
    - HA_pos: Best position found
    - convergence_curve: Convergence history
    """
    
    # Initialize global variables
    HA_pos = np.zeros(dim)
    HA_score = float('inf')
    Rom_Gen = np.zeros(dim)
    Rom_score = float('inf')
    convergence_curve = np.zeros(max_iter)
    
    # Initialize populations
    roman_rate = 0.63
    romans_no = int(warriors_no * roman_rate)
    cartagos_no = warriors_no - romans_no
    
    romans, cartagos, romans_fitness, cartagos_fitness = initialize_populations(
        romans_no, cartagos_no, dim, lb, ub, fobj)
    
    # Sort and divide populations into strategic groups
    left_romans, right_romans, center_romans = divide_romans(romans, romans_fitness)
    left_cartagos, right_cartagos, center_cartagos = divide_cartagos(cartagos, cartagos_fitness)
    
    # Main optimization loop
    for it in range(max_iter):
        # Determine battle phase
        phase = get_battle_phase(it, max_iter)
        
        # Execute battle strategies
        (left_romans, right_romans, center_romans, left_cartagos, right_cartagos, center_cartagos,
         HA_score, HA_pos, Rom_score, Rom_Gen) = execute_battle_phase(
            phase, left_romans, right_romans, center_romans, 
            left_cartagos, right_cartagos, center_cartagos,
            Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj)
        
        # Store convergence and display progress
        convergence_curve[it] = HA_score
        print(f'Iteration #{it+1}, Best objective = {HA_score:.6e}')
    
    return HA_score, HA_pos, convergence_curve

def initialize_populations(romans_no, cartagos_no, dim, lb, ub, fobj):
    """Initialize and evaluate both populations"""
    romans = initialization(romans_no, dim, ub, lb)
    cartagos = initialization(cartagos_no, dim, ub, lb)
    romans_fitness = evaluate_population(romans, fobj)
    cartagos_fitness = evaluate_population(cartagos, fobj)
    return romans, cartagos, romans_fitness, cartagos_fitness

def evaluate_population(population, fobj):
    """Evaluate fitness for entire population"""
    fitness = np.zeros(population.shape[0])
    for i in range(population.shape[0]):
        fitness[i] = fobj(population[i, :])
    return fitness

def divide_romans(romans, romans_fitness):
    """Divide Romans into strategic groups (best 3% each for left/right)"""
    sorted_indices = np.argsort(romans_fitness)
    sorted_romans = romans[sorted_indices, :]
    percent_3 = max(1, int(0.03 * len(romans)))
    
    left_group = sorted_romans[:percent_3, :]
    right_group = sorted_romans[percent_3:min(2*percent_3, len(romans)), :]
    center_group = sorted_romans[2*percent_3:, :]
    
    return left_group, right_group, center_group

def divide_cartagos(cartagos, cartagos_fitness):
    """Divide Carthaginians into strategic groups (worst 12% each for left/right)"""
    sorted_indices = np.argsort(cartagos_fitness)[::-1]  # Descending order
    sorted_cartagos = cartagos[sorted_indices, :]
    percent_12 = max(1, int(0.12 * len(cartagos)))
    
    left_group = sorted_cartagos[:percent_12, :]
    right_group = sorted_cartagos[percent_12:min(2*percent_12, len(cartagos)), :]
    center_group = sorted_cartagos[2*percent_12:, :]
    
    return left_group, right_group, center_group

def get_battle_phase(iteration, max_iter):
    """Determine current battle phase"""
    if iteration <= 0.33 * max_iter:
        return 1  # Early phase - all attacks
    elif iteration <= 0.66 * max_iter:
        return 2  # Middle phase - strategic retreats
    else:
        return 3  # Final phase - encirclement

def execute_battle_phase(phase, left_romans, right_romans, center_romans,
                        left_cartagos, right_cartagos, center_cartagos,
                        Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj):
    """Execute battle strategies based on phase"""
    
    if phase == 1:  # Early phase: All attacks
        right_cartagos, left_romans, HA_score, HA_pos, Rom_score, Rom_Gen = execute_attack(
            right_attack, right_cartagos, left_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj)
        left_cartagos, right_romans, HA_score, HA_pos, Rom_score, Rom_Gen = execute_attack(
            left_attack, left_cartagos, right_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj)
        center_cartagos, center_romans, HA_score, HA_pos, Rom_score, Rom_Gen = execute_attack(
            center_attack, center_cartagos, center_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj)
    
    elif phase == 2:  # Middle phase: Strategic retreats
        right_cartagos, left_romans, HA_score, HA_pos, Rom_score, Rom_Gen = execute_attack(
            right_attack, right_cartagos, left_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj)
        left_cartagos, left_romans, HA_score, HA_pos, Rom_score, Rom_Gen = execute_attack(
            left_attack, left_cartagos, left_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj)
        right_romans, HA_score, HA_pos, Rom_score, Rom_Gen = execute_retreat(
            right_romans, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj)
        center_cartagos, center_romans, HA_score, HA_pos, Rom_score, Rom_Gen = execute_attack(
            center_attack, center_cartagos, center_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj)
    
    else:  # Final phase: Encirclement
        right_cartagos, center_romans, HA_score, HA_pos, Rom_score, Rom_Gen = execute_attack(
            right_attack, right_cartagos, center_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj)
        left_romans, HA_score, HA_pos, Rom_score, Rom_Gen = execute_retreat(
            left_romans, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj)
        left_cartagos, center_romans, HA_score, HA_pos, Rom_score, Rom_Gen = execute_attack(
            left_attack, left_cartagos, center_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj)
        right_romans, HA_score, HA_pos, Rom_score, Rom_Gen = execute_retreat(
            right_romans, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj)
        center_cartagos, center_romans, HA_score, HA_pos, Rom_score, Rom_Gen = execute_attack(
            center_attack, center_cartagos, center_romans, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj)
    
    return (left_romans, right_romans, center_romans, left_cartagos, right_cartagos, center_cartagos,
            HA_score, HA_pos, Rom_score, Rom_Gen)

def execute_attack(attack_func, attackers, defenders, Rom_Gen, HA_pos, HA_score, Rom_score, lb, ub, fobj):
    """Execute attack and update positions"""
    attackers, defenders = attack_func(attackers, defenders, Rom_Gen, HA_pos)
    attackers, HA_score, HA_pos, Rom_score, Rom_Gen = evaluate_and_update(
        attackers, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj)
    defenders, HA_score, HA_pos, Rom_score, Rom_Gen = evaluate_and_update(
        defenders, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj)
    return attackers, defenders, HA_score, HA_pos, Rom_score, Rom_Gen

def execute_retreat(retreaters, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj):
    """Execute retreat maneuver"""
    for i in range(retreaters.shape[0]):
        if isinstance(ub, (int, float)):
            retreaters[i, :] = retreaters[i, :] + np.random.randn(retreaters.shape[1]) * (ub - lb)
        else:
            retreaters[i, :] = retreaters[i, :] + np.random.randn(retreaters.shape[1]) * (np.array(ub) - np.array(lb))
    
    retreaters, HA_score, HA_pos, Rom_score, Rom_Gen = evaluate_and_update(
        retreaters, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj)
    return retreaters, HA_score, HA_pos, Rom_score, Rom_Gen

def evaluate_and_update(population, HA_score, HA_pos, Rom_score, Rom_Gen, lb, ub, fobj):
    """Evaluate population and update best solutions"""
    for i in range(population.shape[0]):
        population[i, :] = enforce_bounds(population[i, :], ub, lb)
        fitness = fobj(population[i, :])
        
        if fitness < HA_score:
            HA_score = fitness
            HA_pos = population[i, :].copy()
        elif fitness < Rom_score:
            Rom_score = fitness
            Rom_Gen = population[i, :].copy()
    
    return population, HA_score, HA_pos, Rom_score, Rom_Gen
