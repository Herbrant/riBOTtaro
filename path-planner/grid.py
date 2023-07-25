import numpy as np

class Grid:
    GRID_IND_DEFAULT = 0
    GRID_IND_OBSTACLE = -1
    GRID_IND_STARTING_CELL = 1
    GRID_IND_DESTINATION_CELL = 2
    GRID_IND_PATH = 4

    def __init__(self, grid_file):
        self.matrix = np.loadtxt(grid_file)
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])
        self.destination = (0,0)

    def set_starting_cell(self, cell):
        row, col = cell[0], cell[1]
        self.matrix[row][col] = self.GRID_IND_STARTING_CELL

