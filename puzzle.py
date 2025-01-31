"""
This is the file that contains method that determines the goal state and
other possible state for the maze on the AI Search assignment.

Kevin Binu Thottumkal, Mohawk College, 4 December 2024
"""

def is_goal(state, maze):
    """
    Method which will return true if the currrent state matches the goal state.
    Here for the maze the final goal state will be in the last row

    Args:
        state (tupule) - (row, col): represents the current state in the maze
        maze (2d list) - 2D list representing the maze

    Returns:
        bool - True, if the current row is at the last row (goal_state); False, if not on the last row
    """
    height = len(maze)
    return state[0] == height - 1

def get_start_state(maze):
    """
    Method to find the starting state of the maze.
    The starting position will in the first row where there is a gap

    Args:
        maze (2d list) - 2D list representing the maze

    Returns:
        tuple - (row, col): The coordinates of the starting state, represented as.
    """
    width = len(maze[0])
    for i in range(width):
        if maze[0][i] == "c":
            return (0, i)

def next_states(state, maze):
    """
    Method to find the possible next moves in the maze.
    It will check for obstructions (wall) for the nearby moves available
    and finds the moves which does not ahve any obstructions

    Args:
        state (tupule) - (row, col): represents the current state in the maze
        maze (2d list) - 2D list representing the maze

    Returns:
        list of tuple: A list of tupules representing the valid possible next moves (next possible states)
    """
    currentRow, currentCol = state
    row, col = state
    height = len(maze)
    width = len(maze[0])

    # Up, Down, Left, Right
    moves = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]

    possible_moves= []

    for (row, col) in moves:
        if (0 <= row < height and 0 <= col < width and maze[row][col] != 'w'):
            possible_moves.append((row, col))

    return possible_moves