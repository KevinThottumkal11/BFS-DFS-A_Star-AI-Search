"""
This is the main file for the AI Search project.
This file assess the performance of various search algorithms like
DFS, BFS, and A* Algorithm and reports its performance.

Kevin Binu Thottumkal, Mohawk College, 4 December 2024
"""
from queue import LifoQueue, Queue, PriorityQueue
from time import time
import copy
from prim_maze_generator import print_maze, generate_maze
from puzzle import is_goal, get_start_state, next_states
from path import create_path, add_state_to_path, print_path

## DFS
def DFS(start_state, maze):
    """
    Performs a depth-first search starting at start_state. Returns the path
    to the goal if found, or None if no path exists. Relies on functions
    is_goal and next_states to define the goal and the search

    Args:
        start_state (tupule) - (row, col): represents the staring state in the maze
        maze (2d list) - 2D list representing the maze

    Returns:
        list - if the path to the final goal state is found, else None
    """
    closed = set()  # Used set for better performance
    open = LifoQueue()
    open.put((start_state, create_path(start_state)))

    while not open.empty():
        state, path = open.get(False)
        if state not in closed:
            closed.add(state)
            if is_goal(state, maze):
                return path

            for new_state in next_states(state, maze):
                new_path = add_state_to_path(path, new_state)
                open.put((new_state, new_path))

    return None

## BFS
def BFS(start_state, maze):
    """
    Implementation of the Breadth-First Search.

    Args:
        start_state (tupule) - (row, col): represents the staring state in the maze
        maze (2d list) - 2D list representing the maze

    Returns:
        list - if the path to the final goal state is found, else None
    """
    closed = set()
    open = Queue()
    open.put((start_state, create_path(start_state)))

    while not open.empty():
        state, path = open.get()
        if state not in closed:
            closed.add(state)
            if is_goal(state, maze):
                return path
            for new_state in next_states(state, maze):
                new_path = add_state_to_path(path, new_state)
                open.put((new_state, new_path))
    return None

## A* Searching

# Heurestic function
def manhattan_distance(state, maze):
    """
    Heuristic function for A* search
    REFERENCE: https://www.geeksforgeeks.org/a-search-algorithm/

    Manhattan distance is a heuristic function which calculates the sum of the
    absolute values of the difference of goal state's x and y coordinates and
    the current state's x and y coordinates.

    Manhattan distance is considered to be one of the simplest heurestic function
    as it involves simple arithmetic operation.
    This heuristic is guarenteed not overestimate the cost beacuse it considers each step
    to be equla cost providing a uniform and cosistent comparison for each path to the goal.

    Limitation:
        This function does not include extra cost due to the obstaclesS

    Args:
        start_state (tupule) - (row, col): represents the staring state in the maze
        maze (2d list) - 2D list representing the maze

    Returns:
        int - Manhattan distance value from the current state to the goal state
    """
    height = len(maze)
    width = len(maze[0])
    target_row = height - 1

    # looking for goal (empty cell) in the last row
    target_cell = None
    for col in range(width):
        if maze[target_row][col] == 'c':
            target_cell = col
            break

    if target_cell is None:
        raise ValueError("No target cell (goal) found in the bottom row.")

    return abs(state[0] - target_row) + abs(state[1] - target_cell)

def AStar(start_state, maze):
    """
    Implemetation of the A* Search algorithm with a heuristic function.

    Args:
        start_state (tupule) - (row, col): represents the staring state in the maze
        maze (2d list) - 2D list representing the maze

    Returns:
        list - if the path to the final goal state is found, else None
    """
    closed = set()
    open = PriorityQueue()
    open.put((0, start_state, create_path(start_state)))

    while not open.empty():
        fCost, state, path = open.get()
        if state not in closed:
            closed.add(state)
            if is_goal(state, maze):
                return path
            for new_state in next_states(state, maze):
                new_path = add_state_to_path(path, new_state)
                gCost = len(path)

                row = new_state[0]
                col = new_state[1]

                cellValue = maze[row][col]  # counting cell values when difficulty is higher

                if cellValue.isdigit():
                    gCost += int(cellValue)

                hCost = manhattan_distance(new_state, maze)  # Estimated cost to the goal
                totalFCost = gCost + hCost          # f(n) = g(n) + h(n)
                open.put((totalFCost, new_state, new_path))
    return None

def calculate_totalcost(search_path, maze):
    """
    Method to find the total cost of the path in the maze

    Args:
        start_state (tupule) - (row, col): represents the staring state in the maze
        maze (2d list) - 2D list representing the maze

    Returns:
        int - Total cost of the path in the maze
    """
    cost = 0
    for (row, col) in search_path:
        cellValue = maze[row][col]
        if cellValue.isdigit():
            cost += int(cellValue)
        else:
            cost += 1
    return cost

def print_maze_solution(maze, path):
    """
    Print the solution of the maze with an asterisk(*) for representing the path

    Args:
        maze (list): 2D representation of the maze
        path: Solution path
    """
    # Create a deep copy of the maze
    maze_sol = copy.deepcopy(maze)

    for (row, col) in path:
        if maze_sol[row][col] not in ['w']:
            maze_sol[row][col] = '*'
    print_maze(maze_sol)

def main():
    """
    Main method for the AI Seach project
    """

    # generate_maze will throw error if the value of height or width is less than 3
    height = int(input("Maze Height: "))
    while height < 3:
        print("Minimum vakue of height should be 3!")
        height = int(input("Maze Height: "))

    width = int(input("Maze Width: "))
    while width < 3:
        print("Minimum value of width should be 3!")
        width = int(input("Maze Width: "))

    difficulty = float(input("Difficulty (0.0 -> 1.0): "))
    while difficulty < 0.0 or difficulty > 1.0:
        print("Difficulty value should be between 0.0 and 1.0")
        difficulty = float(input("Difficulty (0.0 -> 1.0): "))

    maze = generate_maze(height, width, True, difficulty)
    start_state = get_start_state(maze)

    print("\n")
    print("Original Maze")
    print_maze(maze)
    print("\n")

    # A*
    start = time()
    astar = AStar(start_state, maze)
    end = time()

    if astar:
        print("A* Search")
        print_maze_solution(maze, astar)
        total_cost = calculate_totalcost(astar, maze)
        print(f"Cost: {total_cost}")
        print(f"Time: {end-start} seconds")
    else:
        print("No solution found for A* !")

    # BFS
    start = time()
    bfs = BFS(start_state, maze)
    end = time()

    if bfs:
        print("\n")
        print("Breadth-First Search")
        print_maze_solution(maze, bfs)
        total_cost = calculate_totalcost(bfs, maze)
        print(f"Cost: {total_cost}")
        print(f"Time: {end-start} seconds")
    else:
        print("No solution found for BFS !")

    # DFS
    start = time()
    dfs = DFS(start_state, maze)
    end = time()

    if dfs:
        print("\n")
        print("Depth-First Search")
        print_maze_solution(maze, dfs)
        total_cost = calculate_totalcost(dfs, maze)
        print(f"Cost: {total_cost}")
        print(f"Time: {end-start} seconds")
    else:
        print("No solution found for DFS !")

if __name__ == "__main__":
    main()