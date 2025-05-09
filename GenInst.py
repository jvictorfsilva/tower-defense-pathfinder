import os
import random
from collections import deque

def generate_instance(size, tower_probability=0.25):
    """
    Generates a random grid of given size.
    'T' represents a tower with given probability, '.' is a walkable cell.
    Ensures start (0,0) and end (size-1,size-1) are always walkable.
    """
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            if (i == 0 and j == 0) or (i == size - 1 and j == size - 1):
                row.append('.')
            else:
                cell = 'T' if random.random() < tower_probability else '.'
                row.append(cell)
        grid.append("".join(row))
    return grid

def is_solvable(grid):
    """
    Checks if there's a path from (0,0) to (n-1,n-1) avoiding towers using BFS.
    Moves allowed: up, down, left, right.
    """
    n = len(grid)
    if grid[0][0] == 'T' or grid[n-1][n-1] == 'T':
        return False

    moves = [(1,0),(-1,0),(0,1),(0,-1)]
    visited = [[False]*n for _ in range(n)]
    queue = deque([(0,0)])
    visited[0][0] = True

    while queue:
        i, j = queue.popleft()
        if (i, j) == (n-1, n-1):
            return True
        for di, dj in moves:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and not visited[ni][nj] and grid[ni][nj] == '.':
                visited[ni][nj] = True
                queue.append((ni, nj))
    return False

def save_instance(grid, file_path):
    """
    Saves the instance grid to a file.
    """
    with open(file_path, 'w') as f:
        f.write(str(len(grid)) + '\n')
        for row in grid:
            f.write(row + '\n')

def main():
    random.seed(42)  # For reproducibility

    output_dir = "insts"
    os.makedirs(output_dir, exist_ok=True)

    num_instances = 10
    start_size = 8
    step = 4
    tower_probability = 0.25

    for i in range(num_instances):
        size = start_size + step * i
        # Generate until solvable
        attempts = 0
        while True:
            grid = generate_instance(size, tower_probability)
            attempts += 1
            if is_solvable(grid):
                break
        file_path = os.path.join(output_dir, f"inst{str(i+1).zfill(2)}.in")
        save_instance(grid, file_path)
        print(f"Instance {i+1} ({size}x{size}) solved after {attempts} attempts, saved to {file_path}")

if __name__ == "__main__":
    main()