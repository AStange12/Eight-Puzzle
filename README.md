# 8-Puzzle Solver

## Overview
In this project I created an 8-puzzle program in C++, generating random solvable* 8-puzzle boards along with various search algorithms to solve said puzzle. The program utilizes Depth-First Search (DFS), Best-First Search (BestFS), and A* Search algorithms. Two different heuristics are applied to estimate the distance between a given board state and the goal state: 
   - The number of misplace tiles
   - The Manhattan Distance – sum of all tiles ‘distance’ to their goal state
   
The performance of each algorithm is analyzed by tracking run times for time complexity, and priority queue/stack/visited list size for space complexity. It should be noted that since DFS performs significantly worse than A* and BestFS, which show comparable performance’s, DFS was left out in some of the testing.


## Setup
Follow these steps to set up and run the 8-puzzle solver:

1. **Install Python**: Ensure you have Python 3 installed. You can download it here: [Python Downloads](https://www.python.org/downloads/)
   
2. **Get an IDE**: It is recommended to use an IDE like Visual Studio Code for easier navigation and execution. Download it here: [Visual Studio Code](https://code.visualstudio.com/download)
   
3. **Download the Python Code**: Ensure you have all the necessary files and that they match the Python version you are running.
   
4. **Run the Program**:
   - Open the folder containing the Python files in your IDE.
   - Run `EightPuzzle_Main.py` to start the solver.
   
5. **Follow Menu Instructions**: The terminal will display the initial board and prompt you to select a search algorithm. During execution, the program will display a counter for every 1,000 boards visited. If the goal board is found before visiting 10,000 boards, the program will display the solution path. Otherwise, the search will terminate, indicating failure. Performance statistics will be automatically saved to a CSV file.

## Optional Code Modifications
You can modify various parts of the code to customize behavior:

### `EightPuzzle_Main.py`
- To compare the algorithms further, comment out the default `main` function and uncomment lines 58 or 59 at the bottom.
- Adjust or remove the explored board limit by modifying line 151 (default: `10000`). You can also comment out the relevant if-statements in each search function.

### `BoardClass.py`
- To solve specific boards, modify the `initializePuzzleBoard()` function. Add a new board in the sample boards section using existing templates.
- Uncomment lines 108–110 to always initialize the puzzle with your custom board. The `X` and `Y` values correspond to the coordinates of the empty tile (0), with indexing starting at 0.
- To switch the heuristic, comment out one of the computeDistanceFromGoal functions and uncomment the other on line 194 - 220 (Manhattan Distance is the top function, Misplaced Tiles is the bottom function).

## References
- [Python Downloads](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- ChatGPT and VSCode's Copilot extension where used in the creation of this project

