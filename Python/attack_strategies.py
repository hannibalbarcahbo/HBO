import numpy as np
from utils import parallaxe

def left_attack(pos_right, pos_left, General, Hannibal):
    """Left attack strategy"""
    random_vector_right = np.random.randn(*pos_right.shape) * 0.5
    random_vector_left = np.random.randn(*pos_left.shape) * 0.5
    
    # Mirror positions
    new_pos_right = 2 * np.mean(pos_left, axis=0) - random_vector_right * pos_right
    new_pos_left = 2 * np.mean(pos_right, axis=0) - random_vector_left * pos_left
    
    new_pos_right = 0.94 * parallaxe(new_pos_right, Hannibal)
    new_pos_left = 0.94 * parallaxe(new_pos_left, General)
    
    return new_pos_right, new_pos_left

def right_attack(pos_right, pos_left, General, Hannibal):
    """Right attack strategy"""
    reflection_plane = (np.mean(pos_right, axis=0) + np.mean(pos_left, axis=0)) / 2
    random_vector_right = np.random.randn(*pos_right.shape) * 0.5
    random_vector_left = np.random.randn(*pos_left.shape) * 0.5
    
    new_pos_right = reflection_plane + random_vector_right * (reflection_plane - pos_right)
    new_pos_left = reflection_plane + random_vector_left * (reflection_plane - pos_left)
    
    new_pos_right = 0.94 * parallaxe(new_pos_right, Hannibal)
    new_pos_left = 0.94 * parallaxe(new_pos_left, General)
    
    return new_pos_right, new_pos_left

def center_attack(pos_right, pos_left, General, Hannibal):
    """Center attack strategy"""
    c = 0.94
    random_vector_right = np.random.randn(*pos_right.shape) * c * np.random.rand()
    random_vector_left = np.random.randn(*pos_left.shape) * c * np.random.rand()
    
    new_pos_right = pos_right + random_vector_right * (General - pos_right)
    new_pos_left = pos_left + random_vector_left * (Hannibal - pos_left)
    
    return new_pos_right, new_pos_left
