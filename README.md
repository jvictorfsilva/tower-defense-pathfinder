# Tower Defense Pathfinder

## Overview

**Tower Defense Pathfinder** is a Python application that generates random grid-based tower defense instances and finds the minimum-damage path from the top-left corner to the bottom-right corner of the grid. Towers (`T`) block movement and inflict damage on adjacent cells. The solver uses the A\* search algorithm with Manhattan distance as a heuristic to minimize total damage taken.

This project was developed as a solution to the CIC111 2023S1 assignment:  
https://hokama.com.br/disciplinas/cic111_2023s1/enunciado.pdf

## Folder Structure

```
.
├── TowerDefense.py       # Main solver program using A* search
├── GenInst.py           # Random instance generator with solvability check
├── insts/               # Generated input instance files (.in)
│   └── instXX.in
├── outs/                # Solver output files (.out)
│   └── outXX.out
└── README.md            # Project documentation
```

## Requirements

- Python 3.6 or higher
- No external libraries required (uses only the Python standard library)

## Generating Instances

Use `GenInst.py` to create random, solvable grid instances:

```bash
python GenInst.py
```

- Instances will be saved in the `insts/` directory as `inst01.in`, `inst02.in`, ..., `inst10.in`.
- You can configure:
  - `num_instances`: number of grids to generate (default: 10)
  - `start_size`: initial grid size (default: 8)
  - `step`: size increment per instance (default: 4)
  - `tower_probability`: probability of placing a tower in each cell (default: 0.25)

## Solving Instances

Use `TowerDefense.py` to compute the minimum-damage path for an instance:

```bash
python TowerDefense.py insts/instXX.in
```

- Replace `XX` with the instance number (e.g., `01`).
- Output path and damage details will be printed to the console.
- The path (sequence of moves) will be written to `outs/outXX.out`.

### Example

```bash
python TowerDefense.py insts/inst01.in
# Console:
# Minimum-damage path: EESSWW...
# Total damage taken: 120
# Generated file: outs/out01.out
```

## Algorithm Details

1. **Instance Generation (`GenInst.py`):**
   - Creates an *n*×*n* grid populated with towers (`T`) at random.
   - Ensures start `(0,0)` and goal `(n-1,n-1)` are free cells.
   - Uses breadth-first search (BFS) to check solvability (avoiding towers).
2. **Damage Calculation (`TowerDefense.py`):**
   - For each free cell, computes damage as `10` per adjacent tower (8 neighbors).
3. **Pathfinding (A\* Search):**
   - States: grid cells `(i,j)`.
   - Cost function: cumulative damage.
   - Heuristic: Manhattan distance to goal.
   - Allowed moves: North (`N`), South (`S`), East (`E`), West (`W`).
   - Reconstructs the lowest-damage path and outputs move sequence.

## Output Format

- Each output file (`outXX.out`) contains a single line with the move sequence (`N`, `S`, `E`, `W`).
- The console also shows the total damage for verification.

## Notes

- Both scripts seed the random number generator for reproducibility (`random.seed(42)`).
- Directories `insts/` and `outs/` are created automatically if missing.

## License

This project is provided under the MIT License. Feel free to adapt and use the code for educational purposes.
