from pathlib import Path
from collections import deque
from grid import Grid
import sys, math

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../")

from lib.phidias.phidias_interface import start_message_server_http, Messaging

class Grassfire:
    def __init__(self, grid, width, height):
        self.grid = grid
        self.width = width
        self.height = height
        self.position = (0, 0)  # (y,x)
        self.grid.set_starting_cell(self.position)

        # Networking
        self.phidias_agent = 'main@127.0.0.1:6565'
        self.robot_agent = 'robot@127.0.0.1:6566'
        self.http_server_thread = start_message_server_http(
            consumer=self, port=6567)

    def run(self):
        self.http_server_thread.join()

    def _is_cell_valid(self, cell):
        row, col = cell[0], cell[1]
        if row < 0 or row >= len(self.grid.matrix) or \
           col < 0 or col >= len(self.grid.matrix[row]):
            return False

        if self.grid.matrix[row][col] == Grid.GRID_IND_OBSTACLE:
            return False
        return True

    def find_path(self, dest_cell):
        dir_vertical, dir_horizontal = [-1, 1, 0, 0], [0, 0, 1, -1]

        queue = deque([(self.position, [self.position])])
        visited = [self.position]

        while len(queue) > 0:
            path = queue.popleft()
            row, col = path[0]

            if (row, col) == dest_cell:
                # Destination reached
                return path[1]

            for i in range(4):
                cell = (dir_vertical[i] + row, dir_horizontal[i] + col)
                if not self._is_cell_valid(cell) or cell in visited:
                    continue

                queue.append((cell, [*path[1], cell]))
                visited.append(cell)

        return []

    def get_block_size(self):
        return (self.width / self.grid.cols, self.height / self.grid.rows)
    
    def to_indexes(self, pos):
        block_size = self.get_block_size()
        print("Block size:", block_size)
        indexes = [math.floor(pos[0] / block_size[0]
                                ), math.floor(pos[1] / block_size[1])]

        # if (indexes[0] < 0):
        #     indexes[0] = 0
        # elif (indexes[0] >= self.grid.cols):
        #     indexes[0] = self.grid.cols - 1

        # if (indexes[1] < 0):
        #     indexes[1] = 0
        # elif indexes[1] >= self.grid.rows:
        #     indexes[1] = self.grid.rows - 1

        return indexes

    def to_pos(self, indexes):
        block_size = self.get_block_size()
        return [indexes[1] * block_size[0], indexes[0] * block_size[1]]

    def on_belief(self, _from, name, terms):
        print(_from, name, terms)
        
        indexes = self.to_indexes(terms)
        print("new target:", indexes)

        path = self.find_path((indexes[1], indexes[0]))

        if len(path) > 0:
            coordinates = [self.to_pos(x) for x in path]
            print("minitargets: ", coordinates)

            for c in coordinates:
                Messaging.send_belief(self.phidias_agent,
                                      'add_minitarget_reactor', c, 'main')

            self.position = (indexes[1], indexes[0])
        else:
            print("No path found.")

        Messaging.send_belief(self.phidias_agent,
                              "go_to_minitarget_reactor", [], 'main')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <grid-file>".format(sys.argv[0]))
        sys.exit(1)
    
    grid = Grid(sys.argv[1])
    solver = Grassfire(grid, 1.0, 1.0)
    solver.run()    
