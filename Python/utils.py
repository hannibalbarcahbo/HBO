import numpy as np

def enforce_bounds(position, ub, lb):
    """Enforce boundary constraints"""
    if isinstance(ub, (int, float)):
        ub = np.full_like(position, ub)
        lb = np.full_like(position, lb)
    else:
        ub = np.array(ub)
        lb = np.array(lb)
    
    flag_ub = position > ub
    flag_lb = position < lb
    position = position * ~(flag_ub | flag_lb) + ub * flag_ub + lb * flag_lb
    
    return position

def parallaxe(pos_right, Rom_Gen):
    """Parallax function for position modification"""
    N = pos_right.shape[0]
    
    if N % 2 != 0:
        couples = np.random.permutation(N-1).reshape(-1, 2)
    else:
        couples = np.random.permutation(N).reshape(-1, 2)
    
    modified_pos_right = pos_right.copy()
    
    for idx in range(couples.shape[0]):
        couple_center = (pos_right[couples[idx, 0], :] + pos_right[couples[idx, 1], :]) / 2
        center_to_gen_dist = np.linalg.norm(couple_center - Rom_Gen)
        
        for j in range(2):
            warrior = pos_right[couples[idx, j], :]
            influence_direction = (Rom_Gen - warrior) / np.linalg.norm(Rom_Gen - warrior)
            adjusted_step_size = center_to_gen_dist * (0.5 + np.random.rand() * 2)
            modified_pos_right[couples[idx, j], :] = warrior + adjusted_step_size * influence_direction
    
    return modified_pos_right
