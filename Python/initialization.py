import numpy as np

def initialization(search_agents_no, dim, ub, lb):
    """Initialize the first population of search agents"""
    if isinstance(ub, (int, float)):
        # Single boundary values
        positions = np.random.rand(search_agents_no, dim) * (ub - lb) + lb
    else:
        # Different boundaries for each variable
        positions = np.zeros((search_agents_no, dim))
        for i in range(dim):
            ub_i = ub[i] if len(ub) > i else ub[0]
            lb_i = lb[i] if len(lb) > i else lb[0]
            positions[:, i] = np.random.rand(search_agents_no) * (ub_i - lb_i) + lb_i
    
    return positions
