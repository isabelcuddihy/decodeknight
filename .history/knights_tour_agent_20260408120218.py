import copy
import time
import numpy as np
import random
from knights_tour_GUI import *
import sys

# set limit high enough for a 50x50 board (2500 moves) plus some buffer for helper functions. 
# adjust higher for larger NxN tests 
sys.setrecursionlimit(3000)


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



########################## CONTROL PANEL #################################################
# adjust board dimensions (as square)
DIM = 18    

# randomizes starting position, change to fixed coord e.g. (0,0) for testing
STARTING_POS = (random.randint(0,(DIM-1)), random.randint(0,(DIM-1)))

# sets depth of search used for heuristic scoring. 1 = Standard Warnsdorff heurstic
# depth = 2 is Pohl's suggested value (can solve as large as 50x50 boards)
DEPTH = 1   
######################################################################################




######################### INITIALIZING CHESSBOARD ######################################################## 
game = Chessboard(GUI=True, render_delay_sec=0.02, grid_length=DIM,grid_width=DIM,starting_knight_pos=STARTING_POS, obstacle_boxes=0)
currentKnightPos, grid, placedKnights, done = game.execute('export')
np.savetxt('initial_grid.txt', grid, fmt="%d")

currentKnightPos,grid, placedKnights, done = game.execute('export')
grid_size = grid.shape[0]

print(currentKnightPos,  grid, placedKnights, done)
###################################################################################################3


#AGENT CODE BELOW

def reset_grid(grid, pos):
    # Resets the grid to its initial state with all cells unvisited (-1) except the starting position which is marked as visited (1).
    grid.fill(-1)  # Mark all cells as unvisited
    grid[pos[0], pos[1]] = 1  # Mark the starting position as visited
    return grid


def get_valid_moves(current_pos, grid):
    """
    Returns a list of (x, y) tuples for all legal knight moves 
    from the current position that land on unvisited (-1) squares.
    """
    y, x = current_pos
    grid_size = grid.shape[0] # assuming a square chessboard/numpy matrix
    
    # defining all 8 possible "L" knight steps
    possible_steps = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    valid = []
    
    for y1, x1 in possible_steps:
        new_y, new_x = y + y1, x + x1
        
        # check if the move is within the grid boundaries
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            
            # check if the cell is unvisited (-1)
            if grid[new_y, new_x] == -1:
                valid.append((new_y, new_x))
                
    return valid



def recur_num_of_mov(node, level, grid):
    # Temporarily mark current node to prevent cycles
    original_val = grid[node[0], node[1]]
    grid[node[0], node[1]] = 1 
    
    children = get_valid_moves(node, grid)
    
    # Base Case: Level 1 is just the count of immediate moves (just like Warnsdorff)
    if level == 1:
        grid[node[0], node[1]] = original_val # Restore before returning
        return len(children)
    
    # sum the connectivity of all children recursively 
    total_connectivity = 0
    for child in children:
        total_connectivity += recur_num_of_mov(child, level - 1, grid)
    
    grid[node[0], node[1]] = original_val # Restore before returning
    return total_connectivity




def pohl_solver(current_pos, move_count, game, k=1):
    if move_count == (game.gridSize * game.gridSize):
        return True

    # Get valid moves using the live game grid
    nodes = get_valid_moves(current_pos, game.grid)
    if not nodes:
        return False 

    # score moves using Pohl's generalized rule 
    scored_nodes = []
    for n in nodes:
        # We pass the grid to simulate connections at depth k
        score = recur_num_of_mov(n, k, game.grid)
        scored_nodes.append((score, n))
    
    # pick moves with the fewest further moves first 
    scored_nodes.sort()
    
    # execute the moves in the game (same as warnsdorff)
    for score, next_move in scored_nodes:
        game.execute("place", next_move)
        
        # recursive call to solve the rest of the board from the new position
        if pohl_solver(next_move, move_count + 1, game, k):
            return True
        
        # backtracking if we failed
        game.execute("undo")
        
    return False


print("Valid moves from start:", get_valid_moves(currentKnightPos, grid))
print("Placed knights:", placedKnights)
print("Grid state:\n", grid)



# Timing code's execution for metrics
start = time.time()  # <- do not modify this.

pohl_solver(currentKnightPos, len(placedKnights), game, k=DEPTH)

end=time.time()


print(f"Solved with {end-start} seconds of execution time!")
game._main()


np.savetxt('grid.txt', grid, fmt="%d")
with open("final_grid.txt", "w") as outfile:
    outfile.write(str(placedKnights))





######################### OUTDATED CODE ################################

# The function below (warnsdorff_solver) was v1 of our agent. It implemented Warnsdorff's basic heuristic and could solve standard 8x8 boards.
# Its functionality has been embedded in pohl_solver() and its output can be reproduced by setting DEPTH = 1 in control panel.

#def warnsdorff_solver(current_pos, move_count):
#    # base case: knight has filled the whole board
#    if move_count == (grid_size * grid_size):
#        return True
#
#    # get nodes and their Warnsdorff scores
#    nodes = get_valid_moves( current_pos, game.grid)

#    # sort nodes by the number of onward moves they have
#    nodes.sort(key=lambda c: len(get_valid_moves(c, game.grid)))

#    for next_move in nodes:
#        # move to the square
#        game.execute("place", next_move) 
        
        # recursively try to solve from the new position
#        if warnsdorff_solver(next_move, move_count + 1):
#            return True
        
#        # if we fail (dead end) then backtrack
#        game.execute("undo")
        
#    return False
