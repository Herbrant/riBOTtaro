import numpy as np

class Grid:
    GRID_IND_DEFAULT = 0
    GRID_IND_OBSTACLE = 1
    GRID_IND_STARTING_CELL = -1

    def __init__(self, grid_file):
        self.matrix = np.loadtxt(grid_file)
        print(self.matrix)
        self.matrix = np.rot90(self.matrix, 2)
        self.matrix = np.fliplr(self.matrix)
        print(self.matrix)
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def set_starting_cell(self, cell):
        row, col = cell[0], cell[1]
        self.matrix[row][col] = self.GRID_IND_STARTING_CELL

