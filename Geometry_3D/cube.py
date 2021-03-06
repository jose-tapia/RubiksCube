import numpy as np
from copy import deepcopy
import CubeUtils

class Cube:
    def __init__(self):
        self.cube = [[['X' for _ in range(3)] for _ in range(3)] for _ in range(3)]
    
    def __str__(self):
        empty = [[' ']*3]*3
        first_line = [empty, self.get_face('U')]
        second_line = [self.get_face('W'), self.get_face('S'), self.get_face('E'), self.get_face('N')]
        third_line = [empty, self.get_face('D')]

        cube_str = ['']
        for line in [first_line, second_line, third_line]:
            for subline in range(3):
                for face in line:
                    for c in face[subline]:
                        cube_str.append(str(c))
                    cube_str.append(' ')
                cube_str.append('\n')
        return ' '.join(cube_str)

    def get_face_positions(self, dir = ''):    
        x_default, y_default, z_default = CubeUtils.orientation[dir]
        xs = [x_default] if x_default is not None else range(len(self.cube))
        ys = [y_default] if y_default is not None else range(len(self.cube[0]))
        zs = [z_default] if z_default is not None else range(len(self.cube[0][0]))
        return [[x, y, z] for x in xs for y in ys for z in zs]

    def get_face(self, dir):
        if dir != '':
            positions = self.get_face_positions(dir)
            colors = [self.cube[x][y][z] for x, y, z in positions]
            return [colors[:3], colors[3:6], colors[6:]]   
        else:
            return []

    def set_color(self, dir, color):
        face = self.get_face_positions(dir)
        for x, y, z in face:
            self.cube[x][y][z] = color

    def get_color(self, dir):
        x, y, z = CubeUtils.orientation[dir]
        x = x if x is not None else 1
        y = y if y is not None else 1
        z = z if z is not None else 1
        return self.cube[x][y][z]
    
    def apply_rotation(self, alpha, beta, gamma, face = ''):
        R = CubeUtils.get_rotation_matrix(alpha, beta, gamma)
        positions = self.get_face_positions(face)

        cube = deepcopy(self.cube)
        for x, y, z in positions:
            x_r, y_r, z_r = np.matmul(R, [x-1, y-1, z-1])
            x_r, y_r, z_r = int(np.rint(x_r+1)), int(np.rint(y_r+1)), int(np.rint(z_r+1))
            self.cube[x_r][y_r][z_r] = cube[x][y][z]

class RubiksCube(Cube):
    def __init__(self, scramble = []):
        self.cube = [[[Cube() for _ in range(3)] for _ in range(3)] for _ in range(3)]
        CubeUtils.cube_dirs = [[[[] for _ in range(3)] for _ in range(3) ] for _ in range(3)]

        for dir, color in zip(CubeUtils.orientation.keys(), CubeUtils.colors):
            positions = self.get_face_positions(dir)
            for x, y, z in positions:
                self.cube[x][y][z].set_color(dir, color)
                CubeUtils.cube_dirs[x][y][z].append(dir)
        
        self.apply_scramble(scramble)
    
    def get_face(self, dir):
        if dir != '':
            positions = self.get_face_positions(dir)
            colors = [self.cube[x][y][z].get_color(dir) for x, y, z in positions]
            if dir in ['U', 'S', 'W']:
                return [colors[:3], colors[3:6], colors[6:]]   
            if dir in ['N', 'E']:
                color_matrix = [colors[:3], colors[3:6], colors[6:]]
                for idx in range(3):
                    color_matrix[idx].reverse()
                return color_matrix
            if dir == 'D':
                return [colors[6:], colors[3:6], colors[:3]]
        return []

    def apply_movement(self, movement):
        if movement in CubeUtils.get_all_movements():
            basic_mov = CubeUtils.get_basic_prefix(movement)
            times = CubeUtils.get_suffix_times(movement)
            self._apply_basic_movement(basic_mov, times)
            return
        else:
            print(f'Unsupported movement: {movement}')
            return

    def apply_scramble(self, scramble):
        for movement in scramble:
            self.apply_movement(movement)

    def get_piece_colors(self, x: int, y: int, z: int):
        colors = []
        for dir in CubeUtils.cube_dirs[x][y][z]:
            colors.append(self.cube[x][y][z].get_color(dir))
        return colors

    def set_piece_colors(self, x, y, z, colors):
        dirs = CubeUtils.cube_dirs[x][y][z]
        if len(dirs) != len(colors):
            return 
        for dir, color in zip(dirs, colors):
            self.cube[x][y][z].set_color(dir, color)

    def find_piece(self, colors):
        colors_copy = colors.copy()
        colors_copy.sort()
        positions = self.get_face_positions()
        for x, y, z in positions:
            colors_piece = self.get_piece_colors(x, y, z)
            colors_piece.sort()
            if colors_piece == colors_copy:
                return x, y, z
        return None
    
    def erase_piece(self, colors):
        positions = self.find_piece(colors)
        if positions is None:
            return
        x, y, z = positions
        dirs = CubeUtils.cube_dirs[x][y][z]
        for dir in dirs:
            self.cube[x][y][z].set_color(dir, 'X')

    def _apply_basic_movement(self, movement, times = 1.0):
        dir, alpha, beta, gamma = CubeUtils.cube_notations[movement]
        alpha_t, beta_t, gamma_t = alpha * times, beta * times, gamma * times

        self.apply_rotation(alpha_t, beta_t, gamma_t, dir)
        positions = self.get_face_positions(dir)
        for x, y, z in positions:
            self.cube[x][y][z].apply_rotation(alpha_t, beta_t, gamma_t)
            
if __name__ == "__main__":
    #rubik_1 = RubiksCube(["D'", "R", "L", "F", "R'", "L", "U2", "F", "D2", "R'", "L2", "F2", "D", "R2", "B2", "D2", "L2", "U'", "B2", "U'"])
    #rubik_2 = RubiksCube(["F", "R2", "U'"])
    rubik_3 = RubiksCube(["B", "F", "U", "L'", "D'", "R'","F'"])
    rubik_4 = RubiksCube(["U'", "F", "B", "R'", "U", "R'", "F'", "D2", "L", "F", "U'", "F2", "L2", "U'", "D", "L2", "U'", "B2", "U'"])
    # U' F B R' U R' F' D2 L F U' F2 L2 U' D L2 U' B2 U'
    rubik_5 = RubiksCube()
    #print(rubik_1)
    #print(rubik_2)
    print(rubik_5)

    positions = rubik_5.get_face_positions('S')
    for x, y, z in positions:
        print(rubik_5.get_piece_colors(x, y, z))
    print(rubik_5.find_piece(['G', 'R']))

    rubik_5.apply_scramble(["D'", "R'", "D", "R", "D", "F", "D'", "F'"])
    rubik_5.apply_scramble(["D", "D"])
    rubik_5.apply_scramble(["D'", "R'", "D", "R", "D", "F", "D'", "F'"])

    for x, y, z in positions:
        print(rubik_5.get_piece_colors(x, y, z))
    
    print(rubik_5.find_piece(['G', 'R']))
    print(rubik_5)