import copy
import time
import numpy as np
from knightstouragent import *
from warnsdorff import *

####################################################
# The Knight's Tour is a classic problem in which the goal is to move a knight around a chessboard, visiting each square exactly once.
# The knight moves in an L-shape: two squares in one direction and then one square perpendicular to that.
# The challenge is to find a sequence of moves that allows the knight to visit every square on the board without repeating any square.
# In this implementation, we will use:
# A GUI to visualize the knight's movements on the chessboard.
# A grid to represent the chessboard, where each cell can be marked with the number move the knight just made and the knight's current position is indicated by a knight symbol.
# The objective is to find a sequence of moves that allows the knight to visit every square on the board without overlap and without having to backtrack/undo moves.
# Additional constraints can be added to make the problem more challenging, such as introducing obstacles on the board like "dead" squares and mandating the final square to be at a certain location..




####################################################


game = Chessboard(GUI=True, render_delay_sec=0.5, grid_length=6,grid_width= 6, obstacle_boxes=0)
currentKnightPos, grid, placedKnights, done = game.execute('export')
np.savetxt('initial_grid.txt', grid, fmt="%d")

currentKnightPos,grid, placedKnights, done = game.execute('export')

currentKnightPos, grid, placedKnights, done = game.execute('place', (0, 0))
currentKnightPos,  grid, placedKnights, done = game.execute('place', (2, 1))
currentKnightPos, grid, placedKnights, done = game.execute('place', (4, 2))


print(currentKnightPos,  grid, placedKnights, done)


####################################################
# Timing your code's execution for metrics.
####################################################

start = time.time()  # <- do not modify this.



def get_valid_moves(current_pos, grid):
    """
    Returns a list of (x, y) tuples for all legal knight moves 
    from the current position that land on unvisited (-1) squares.
    """
    x, y = current_pos
    grid_size = grid.shape[0] # assuming a square chessboard/numpy matrix
    
    # defining all 8 possible "L" knight steps
    possible_steps = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    valid = []
    
    for x1, y1 in possible_steps:
        new_x, new_y = x + x1, y + y1
        
        # check if the move is within the grid boundaries
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            
            # check if the cell is unvisited (-1)
            if grid[new_y, new_x] == -1:
                valid.append((new_x, new_y))
                
    return valid


def warnsdorff_solver(current_pos, move_count):
    # base case: knight has filled the whole board
    if move_count == (grid_size * grid_size):
        return True

    # get nodes and their Warnsdorff scores
    nodes = valid_moves(current_pos)

    # sort nodes by the number of onward moves they have
    nodes.sort(key=lambda c: len(valid_moves(c)))

    for next_move in nodes:
        # move to the square
        game.execute("place", next_move) 
        
        # recursively try to solve from the new position
        if warnsdorff_solver(next_move, move_count + 1):
            return True
        
        # if we fail (dead end) then backtrack
        game.execute("undo")
        
    return False





end=time.time()
print(f"Solved with {end-start} seconds of execution time!")

game._main()
np.savetxt('grid.txt', grid, fmt="%d")
with open("final_grid.txt", "w") as outfile:
    outfile.write(str(filledSpaces))

