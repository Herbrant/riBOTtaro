# NF1 implementation
from pathlib import Path
import sys, math
import numpy as np

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../")

from lib.phidias.phidias_interface import start_message_server_http, Messaging

class Grassfire():
    START = 0
    DEST = -1     # destination
    UNVIS = -2    # unvisited
    OBST = -3     # obstacle
    PATH = -4
    
    def __init__(self, grid, width, height):
        self.grid = np.array(grid)
        self.width = width
        self.height = height
        self.position = (0, 0)
        self.phidias_agent = 'main@127.0.0.1:6565'
        self.robot_agent = 'robot@127.0.0.1:6566'
        self.http_server_thread = start_message_server_http(
           consumer=self, port=6567)

    def run(self):
        self.http_server_thread.join()
        
    def to_indexes(self, coordinates):
        # Divido la dimensione dello spazio in blocchi della stessa dimensione
        rows = len(self.grid)
        cols = len(self.grid[0])
        block_width = self.width / rows
        block_height = self.height / cols
        
        return (math.floor(coordinates[0] / block_height + block_height/2.0 - 1) - 1, math.floor(coordinates[1] / block_width + block_width / 2.0 - 1) - 1)
    
    def to_coordinates(self, indexes):
        # Divido la dimensione dello spazio in blocchi della stessa dimensione
        rows = len(self.grid)
        cols = len(self.grid[0])
        block_width = self.width / rows
        block_height = self.height / cols
        
        # Restituisco le coordinate del centro del blocco
        return (round(indexes[0] * block_height + block_height/2.0, 2), round(indexes[1] *block_width + block_width/2.0, 2))
    
    def check_adjacent(self, grid, cell, currentDepth):
        (rows, cols) = grid.shape

        # Track how many adjacent cells are updated.
        numCellsUpdated = 0

        # From the current cell, examine, using sin and cos:
        # cell to right (col + 1), cell below (row + 1),
        # cell to left (col - 1), cell above (row - 1).
        for i in range(4):
            rowToCheck = cell[0] + int(math.sin((math.pi/2) * i))
            colToCheck = cell[1] + int(math.cos((math.pi/2) * i))

            # Ensure cell is within bounds of grid.
            if not (0 <= rowToCheck < rows and 0 <= colToCheck < cols):
                continue
            # Check if destination found.
            elif grid[rowToCheck, colToCheck] == Grassfire.DEST:
                return Grassfire.DEST
            # If adjacent cell unvisited or depth > currentDepth + 1,
            # mark with new depth.
            elif (grid[rowToCheck, colToCheck] == Grassfire.UNVIS
                or grid[rowToCheck, colToCheck] > currentDepth + 1):
                grid[rowToCheck, colToCheck] = currentDepth + 1
                numCellsUpdated += 1
        return numCellsUpdated

    def backtrack(self, grid, cell, currentDepth):
        (rows, cols) = grid.shape

        for i in range(4):
            rowToCheck = cell[0] + int(math.sin((math.pi/2) * i))
            colToCheck = cell[1] + int(math.cos((math.pi/2) * i))

            if not (0 <= rowToCheck < rows and 0 <= colToCheck < cols):
                continue
            elif grid[rowToCheck, colToCheck] == currentDepth:
                nextCell = (rowToCheck, colToCheck)
                grid[nextCell] = Grassfire.PATH
                return nextCell
    
    def reset_grid(self, goal):
        res_grid = self.grid
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if res_grid[i][j] == 0:
                    res_grid[i][j] = Grassfire.UNVIS
                else:
                    res_grid[i][j] = Grassfire.OBST

        res_grid[self.position[0]][self.position[1]] = Grassfire.START
        res_grid[goal[0]][goal[1]] = Grassfire.DEST
        
        return res_grid

    def find_path(self, goal):
        grid = self.reset_grid(goal)
        depth = 0
        destFound = False
        cellsExhausted = False
        
        path = []

        while (not destFound) and (not cellsExhausted):
            numCellsModified = 0
            depthIndices = np.where(grid == depth)
            matchingCells = list(zip(depthIndices[0], depthIndices[1]))

            for cell in matchingCells:
                adjacentVal = self.check_adjacent(grid, cell, depth)
                if adjacentVal == Grassfire.DEST:
                    destFound = True
                    break
                else:
                    numCellsModified += adjacentVal

            if numCellsModified == 0:
                cellsExhausted = True
            elif not destFound:
                depth += 1

        if destFound:
            destCell = np.where(grid == Grassfire.DEST)
            backtrackCell = (destCell[0].item(), destCell[1].item())
            path.append(backtrackCell)
            
            while depth > 0:
                # Work backwards until return to start cell.
                nextCell = self.backtrack(grid, backtrackCell, depth)
                path.append(nextCell)
                backtrackCell = nextCell
                depth -= 1
        
        path.reverse()
        return path
    
    def find_minitargets_coordinates(self, goal):
        print("find_minitargets_coordinates")
        minitargets = self.find_minitargets(goal)
        return  [self.to_coordinates(x) for x in minitargets]

    def on_belief(self, _from, name, terms):
        print(_from, name, terms)
        indexes = self.to_indexes(terms)
        path = self.find_path(indexes)
        print(path)
        coordinates = [self.to_coordinates(x) for x in path]       
        
        print("minitargets: ", coordinates)
        
        for c in coordinates:
            Messaging.send_belief(self.phidias_agent, 'add_minitarget_reactor', c, 'main')
        
        Messaging.send_belief(self.phidias_agent, "go_to_minitarget_reactor", [], 'main')
        
        self.position = (indexes[0], indexes[1])


# Esempio di utilizzo
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

if __name__ == '__main__':
    a = Grassfire(grid, 0.7, 0.5)
    a.run()
