import numpy as np
import random

colors = ['W', 'O', 'G', 'R', 'B', 'Y']

orientation = dict({'U':[0, None, None], 
                    'W':[None, None, 0], 
                    'S':[None, 2, None], 
                    'E':[None, None, 2],  
                    'N':[None, 0, None],
                    'D':[2, None, None],
                    '':[None, None, None]})

cube_notations = dict({'U': ['U', -np.pi/2, 0, 0], 
                       'L': ['W', 0, 0, -np.pi/2],
                       'F': ['S', 0, np.pi/2, 0],
                       'R': ['E', 0, 0, np.pi/2],
                       'B': ['N', 0, -np.pi/2, 0],
                       'D': ['D', np.pi/2, 0, 0]})
        
cube_dirs = [[[[] for _ in range(3)] for _ in range(3) ] for _ in range(3)]

def get_basic_movements():
    return list(cube_notations.keys())

def get_suffix_times(movement):
    if len(movement) == 1:
        return 1.0
    if len(movement) > 2:
        return None
    if movement[1] == '2':
        return 2.0
    if movement[1] == "'":
        return 3.0
    return None

def get_basic_prefix(movement):
    if movement is None:
        return None
    if len(movement) == 1:
        return movement
    if len(movement) > 2:
        return None
    if get_suffix_times(movement) is not None:
        return movement[0]
    return None

def get_all_movements():
    basic_movs = get_basic_movements()
    return [mov+suffix for mov in basic_movs for suffix in ['', "'", '2']]

def create_scramble():
    movements = get_all_movements()
    #movements = get_basic_movements()
    return random.choices(movements, k = random.randint(20, 35))

def get_rotation_matrix(alpha, beta, gamma):
    Rx = [[1, 0, 0], 
            [0, np.cos(alpha), -np.sin(alpha)],
            [0, np.sin(alpha), np.cos(alpha)]]
    Ry = [[np.cos(beta), 0, np.sin(beta)],
            [0, 1, 0],
            [-np.sin(beta), 0, np.cos(beta)]]
    Rz = [[np.cos(gamma), -np.sin(gamma), 0],
            [np.sin(gamma), np.cos(gamma), 0],
            [0, 0, 1]]
    return np.matmul(np.matmul(Rx, Ry), Rz)
