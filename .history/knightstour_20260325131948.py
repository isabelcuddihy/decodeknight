import copy
import time
import numpy as np
from knightstouragent import *

##############################################################################################################################

# You can visualize what your code is doing by setting the GUI argument in the following line to true.
# The render_delay_sec argument allows you to slow down the animation, to be able to see each step more clearly.

# For your final submission, please set the GUI option to False.

# The gs argument controls the grid size. You should experiment with various sizes to ensure your code generalizes.
# Please do not modify or remove lines 18 and 19.

##############################################################################################################################

game = Chessboard(GUI=True, render_delay_sec=0.5, grid_length=6,grid_width= 6, obstacle_boxes=0)
currentKnightPos, moveChoice, grid, placedKnights, done = game.execute('export')
np.savetxt('initial_grid.txt', grid, fmt="%d")
##############################################################################################################################

# Initialization

# shapePos is the current position of the brush.

# currentShapeIndex is the index of the current brush type being placed (order specified in gridgame.py, and assignment instructions).

# currentColorIndex is the index of the current color being placed (order specified in gridgame.py, and assignment instructions).

# grid represents the current state of the board. 
    
    # -1 indicates an empty cell
    # 0 indicates a cell already visited (black by default)
    # 1 indicates a cell as an obstacle (white by default)

# filledSpaces is a list of squares already visited on the board.
    
    # Each shape is represented as a list containing two elements: a) the location of the shape  and b) color of the shape (-1 for free, 0 for visited, 1 for obstacle)

# done is a Boolean that represents whether all sqaures have been visited are satisfied. Updated by the knightstouragent.py file.

##############################################################################################################################

currentKnightPos, moveChoice, grid, placedKnights, done = game.execute('export')

print(currentKnightPos, moveChoice, grid, placedKnights, done)


####################################################
# Timing your code's execution for the leaderboard.
####################################################

start = time.time()  # <- do not modify this.

##########################################
# Write all your code in the area below. 
##########################################

'''
Main idea
State Space: Current Grid with all accepted shapes placed
Action Space: Copy of Current Grid with new potential shape placed
Objective Function:  squares_filled - (adjacent colors * some penalty amount) - (shapes_used * some penalty amount)
while not done: use results from execute
    1. Generate a random valid action
    2. Try placing it in the grid (copy to protect current state)
    3. Calculate objective function of new state
    4. If new score > old score:
        - Actually place it (using execute())
        - Update current score
        4A - sideways move of new_score == old_score place sometimes (low percent chance) 
            -to explore other branch even if not particularly better DO NOT reset attempt counter to 0
        4B - if new score < old score: place (very low percent chance) the downhill/backtracking move
            -DO NOT reset counter to 0
    5. Else:
        - Reject the move, try again
Reset/Restart if stuck in a cycle of over 1500 attempts to find a valid position

Sideways move and/or Downhill move to help maintain current progress and find additional paths to 
move forward without restarting (See enhancements implemented for further details)

'''
'''
This function calculates the objective function score for a given grid state. 
'''
def objectiveFunctionScore(grid):
    # Ensure all squares are filled
    remaining_squares = np.sum(grid == -1)
    # Check that 
    filled_squares = np.sum(grid != -1)
    total_squares = game.gridSize ** 2 # Assuming a square grid, adjust if using rectangular
    if filled_squares < total_squares * 0.75:  # Less than 75% full
        # penalties low-> touching colors, high-> smaller shapes (i.e. use larger shapes)
        return filled_squares - (10*remaining_squares) - (len(filledSpaces)* 2)
    elif filled_squares < total_squares * 0.9:
        # penalties med -> touching colors, med -> smaller shapes (i.e. use larger shapes)
         return filled_squares - (15*remaining_squares) - (len(filledSpaces)* 1.5)
    else:  # fewer options, smaller shapes going to be needed
        # penalties low-> smaller shapes, high-> touching colors
        return filled_squares - (20 * remaining_squares) - (len(filledSpaces) * 0.5)

'''
Function builds all the commands needed to execute the desired new move in the original grid
Params - (x_move :INT )how many horizontal steps to execute
(y_move :INT )how many vertical steps to execute
Returns - list of strings containing the commands needed to execute the desired new move in the original grid
'''
def setUpCommandExecution(grid):

    execution_commands = []
    #find valid move based on current location
    # check can place 
    execution_commands.append("place")
    return execution_commands

current_objective_function_score = objectiveFunctionScore(grid)

while not done:
    possible_score = objectiveFunctionScore(grid.copy())
    if possible_score > current_objective_function_score:
        # FOUND VALID MOVE
        attempts_since_improvement = 0
        #place or undo
        execution_commands = setUpCommandExecution(grid.copy(), possible_valid_move)
        for command in execution_commands:
            shapePos, currentShapeIndex, currentColorIndex, grid, filledSpaces, done = game.execute(command)
        current_objective_function_score = possible_score

    # Counter of attempts to find valid move goes over -> reset grid and start again
    if attempts_since_improvement >= max_attempts_without_improvement:
        # Stuck in a loop, no move is improving status, so need to restart, undo all placed shapes
        while len(filledSpaces) > 0:
            shapePos, currentShapeIndex, currentColorIndex, grid, filledSpaces, done = game.execute('undo')
        current_objective_function_score = objectiveFunctionScore(grid)
        attempts_since_improvement = 0
end=time.time()
print(f"Solved with {end-start} seconds of execution time!")

game._main()
np.savetxt('grid.txt', grid, fmt="%d")
with open("final_grid.txt", "w") as outfile:
    outfile.write(str(filledSpaces))

