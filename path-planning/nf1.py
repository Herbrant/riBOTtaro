# NF1 implementation
from queue import Queue

def grassfire(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])

    distance = [[float('inf')] * cols for _ in range(rows)]
    
    queue = Queue()
    queue.put(start)
    distance[start[0]][start[1]] = 0
    
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while not queue.empty():
        current = queue.get()

        if current == goal:
            break
        
        for move in moves:
            next_row = current[0] + move[0]
            next_col = current[1] + move[1]
            
            if (0 <= next_row < rows and 0 <= next_col < cols and
                    distance[next_row][next_col] == float('inf') and grid[next_row][next_col] != 1):
                queue.put((next_row, next_col))
                distance[next_row][next_col] = distance[current[0]][current[1]] + 1

    return distance

# Esempio di utilizzo
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)

distances = grassfire(grid, start, goal)

# Stampa la griglia delle distanze
for row in distances:
    print(row)