import sys
import os
import heapq

# Directions: South, North, East, West
MOVES = {"S": (1, 0), "N": (-1, 0), "E": (0, 1), "W": (0, -1)}


def read_instance(file_name):
    """
    Read instance from input file.
    Returns grid size and grid layout.
    """
    with open(file_name, "r") as file:
        size = int(file.readline().strip())
        grid = [file.readline().strip() for _ in range(size)]
    return size, grid


def calculate_damage(size, grid):
    """
    Calculate damage values for each cell based on adjacent towers.
    Cells with towers ("T") are impassable (None).
    """
    damages = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if grid[i][j] == "T":
                damages[i][j] = None
            else:
                damage = 0
                # Check all eight neighbors
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < size and 0 <= nj < size and grid[ni][nj] == "T":
                            damage += 10
                damages[i][j] = damage
    return damages


def heuristic(i, j, size):
    """
    Manhattan distance heuristic to goal (bottom-right).
    """
    return abs(size - 1 - i) + abs(size - 1 - j)


def a_star(size, damages):
    """
    Perform A* search to find minimum-damage path.
    Returns cost-so-far matrix and backpointers.
    """
    INF = float("inf")
    goal = (size - 1, size - 1)
    cost_so_far = [[INF] * size for _ in range(size)]
    cost_so_far[0][0] = 0
    came_from = {}
    open_list = []
    # (priority, cost, row, col)
    heapq.heappush(open_list, (heuristic(0, 0, size), 0, 0, 0))
    visited = [[False] * size for _ in range(size)]

    while open_list:
        priority, current_cost, i, j = heapq.heappop(open_list)
        if visited[i][j]:
            continue
        visited[i][j] = True
        if (i, j) == goal:
            break

        for move, (di, dj) in MOVES.items():
            ni, nj = i + di, j + dj
            if 0 <= ni < size and 0 <= nj < size and damages[ni][nj] is not None:
                new_cost = current_cost + damages[ni][nj]
                if new_cost < cost_so_far[ni][nj]:
                    cost_so_far[ni][nj] = new_cost
                    came_from[(ni, nj)] = (i, j, move)
                    estimated = new_cost + heuristic(ni, nj, size)
                    heapq.heappush(open_list, (estimated, new_cost, ni, nj))

    return cost_so_far, came_from


def reconstruct_path(came_from, destination):
    """
    Reconstruct path of moves from start to destination.
    Returns a string of move letters.
    """
    i, j = destination
    path = []
    while (i, j) in came_from:
        pi, pj, move = came_from[(i, j)]
        path.append(move)
        i, j = pi, pj
    return "".join(reversed(path))


def main():
    """
    Main entry point: reads input, runs A*, writes output, prints results.
    """
    if len(sys.argv) < 2:
        print("Usage: python TowerDefense.py instXX.in")
        sys.exit(1)

    input_file = sys.argv[1]
    base_name = os.path.basename(input_file)
    instance_number = base_name.replace("inst", "").replace(".in", "")
    output_file = f"outs/out{instance_number}.out"

    size, grid = read_instance(input_file)
    damages = calculate_damage(size, grid)
    costs, backpointers = a_star(size, damages)

    path = reconstruct_path(backpointers, (size - 1, size - 1))
    total_damage = costs[size - 1][size - 1]

    with open(output_file, "w") as f:
        f.write(path + "\n")

    print(f"Minimum-damage path: {path}")
    print(f"Total damage taken: {total_damage}")


if __name__ == "__main__":
    main()
