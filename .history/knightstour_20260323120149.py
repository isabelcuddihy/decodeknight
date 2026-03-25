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

game = Chessboard(GUI=True, render_delay_sec=0.5, gs=6, num_colored_boxes=0)
shapePos, currentShapeIndex, currentColorIndex, grid, filledSpaces, done = game.execute('export')
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

shapePos, currentShapeIndex, currentColorIndex, grid, filledSpaces, done = game.execute('export')

print(shapePos, currentShapeIndex, currentColorIndex, grid, filledSpaces, done)


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
ENHANCEMENTS IMPLEMENTED:

1. Sideways Move (15% chance): Accept move with equal objective score to help escape 
   plateaus and explore other solutions when stuck. Still counts as an attempted move because 
   it's not solving the puzzle more, just changing the configuration.

2. Downhill Move (1% chance): Accept worse move to escape local optimization 
   and explore other paths when stuck. Still counts as an attempted move because 
   it's making the puzzle less solved.

3. Restarts (after 1500 attempts without improvement): Undo all placed shapes and 
   restart from initial configuration to try different solution paths and prevent infinite loops.
'''


# YOUR CODE HERE
'''
This function calculates the new objective function score of the potential state created by a valid move
Params - (grid) Temp copy grid of original grid with new move applied
Returns - New objective function score (INT)
under 70% solved focus on bigger shapes, 
under 90% solved focus on balance of big shapes and no conflicting colors, 
over 90% solved focus on no conflicting colors since big shapes won't fit
'''

def objectiveFunctionScore(grid):
    # Ensure all squares are filled
    empty_square = 0
    # Check that 
    for i in range(game.gridSize):
        for j in range(game.gridSize):
            color = grid[i, j]
            if color == -1:
                continue
            if i > 0 and grid[i - 1, j] == color:
                adjacent_colors += 1

            if j > 0 and grid[i, j - 1] == color:
                adjacent_colors += 1
    filled_squares = np.sum(grid != -1)
    total_squares = game.gridSize ** 2
    if filled_squares < total_squares * 0.75:  # Less than 75% full
        # penalties low-> touching colors, high-> smaller shapes (i.e. use larger shapes)
        return filled_squares - (10*adjacent_colors) - (len(filledSpaces)* 2)
    elif filled_squares < total_squares * 0.9:
        # penalties med -> touching colors, med -> smaller shapes (i.e. use larger shapes)
         return filled_squares - (15*adjacent_colors) - (len(filledSpaces)* 1.5)
    else:  # fewer options, smaller shapes going to be needed
        # penalties low-> smaller shapes, high-> touching colors
        return filled_squares - (20 * adjacent_colors) - (len(filledSpaces) * 0.5)

'''
Function builds all the commands needed to execute the desired new move in the original grid
Params - (x_move :INT )how many horizontal steps to execute
(y_move :INT )how many vertical steps to execute
Returns - list of strings containing the commands needed to execute the desired new move in the original grid
'''
def setUpCommandExecution(x_move, y_move):
    pass
    # move brush to approved spot combo of x moves and y moves
#     execution_commands = []
#     if x_move > 0:
#         for i in range(x_move):
#             execution_commands.append("right")
#     elif x_move < 0:
#         for i in range(abs(x_move)):
#             execution_commands.append("left")

#     if y_move > 0:
#         for i in range(y_move):
#             execution_commands.append("down")
#     elif y_move < 0:
#         for i in range(abs(y_move)):
#             execution_commands.append("up")
#     # how many times to cycle through until next new shape
#     moves_to_new_shape = (random_shape - currentShapeIndex) % 9
#     for i in range(moves_to_new_shape):
#         execution_commands.append("switchshape")

#     # how many times to cycle through until new color
#     moves_to_new_color = (random_color - currentColorIndex) % 4
#     for i in range(moves_to_new_color):
#         execution_commands.append("switchcolor")
#     execution_commands.append("place")
#     return execution_commands

# current_objective_function_score = objectiveFunctionScore(grid)
# max_attempts_without_improvement = 1500
# attempts_since_improvement = 0
# while not done:
#     # print(f"Still solving : filled squares so far {np.sum(grid != -1)}")
#     # randomized option for next shape, location, color
#     random_shape = random.randint(0, 8)
#     random_x_pos = random.randint(0, grid.shape[0] - game.shapesDims[random_shape][0])
#     random_y_pos = random.randint(0, grid.shape[1] - game.shapesDims[random_shape][1])
#     random_color = game.getAvailableColor(grid, random_x_pos, random_y_pos)
#     attempts_since_improvement += 1
#     if game.canPlace(grid, game.shapes[random_shape], (random_x_pos, random_y_pos)):
#         # find objective function value for this choice
#         copy_grid = copy.deepcopy(grid)
#         for i, row in enumerate(game.shapes[random_shape]):
#             for j, square in enumerate(row):
#                 if square:
#                     copy_grid[random_y_pos + i, random_x_pos + j] = random_color
#         possible_score = objectiveFunctionScore(copy_grid)
#         # move brush to possible spot
#         brush_x, brush_y = shapePos
#         x_move = random_x_pos - brush_x
#         y_move = random_y_pos - brush_y
#         if possible_score > current_objective_function_score:
#             # FOUND VALID MOVE
#             attempts_since_improvement = 0
#             execution_commands = setUpCommandExecution(x_move, y_move)
#             for command in execution_commands:
#                 shapePos, currentShapeIndex, currentColorIndex, grid, filledSpaces, done = game.execute(command)
#             current_objective_function_score = possible_score

#         # SIDEWAYS MOVE - 15% Chance of Happening
#         elif possible_score == current_objective_function_score:
#             if random.random() < 0.15:  # 15% chance to take a sideways move
#                 # Take a sideways move --> move isn't better, but isn't worse and can help get agent unstuck
#                 execution_commands = setUpCommandExecution(x_move, y_move)
#                 for command in execution_commands:
#                     shapePos, currentShapeIndex, currentColorIndex, grid, filledSpaces, done = game.execute(command)
#                 current_objective_function_score = possible_score

#         # DOWNHILL MOVE - 1% Chance of Happening
#         elif possible_score < current_objective_function_score:
#             if random.random() < 0.01:  # 1% chance for a backwards/downhill move
#                 # Downhill Move --> Allows for the possibility that making a "worse"
#                 # move will allow much more progress further on
#                 execution_commands = setUpCommandExecution(x_move, y_move)
#                 for command in execution_commands:
#                     shapePos, currentShapeIndex, currentColorIndex, grid, filledSpaces, done = game.execute(command)
#                 current_objective_function_score = possible_score
#     # Counter of attempts to find valid move goes over -> reset grid and start again
#     if attempts_since_improvement >= max_attempts_without_improvement:
#         # Stuck in a loop, no move is improving status, so need to restart, undo all placed shapes
#         while len(filledSpaces) > 0:
#             shapePos, currentShapeIndex, currentColorIndex, grid, filledSpaces, done = game.execute('undo')
#         current_objective_function_score = objectiveFunctionScore(grid)
#         attempts_since_improvement = 0
# print(f"Solved with {len(filledSpaces)} shapes")
########################################

# Do not modify any of the code below. 

########################################

end=time.time()
game._main()
np.savetxt('grid.txt', grid, fmt="%d")
with open("shapes.txt", "w") as outfile:
    outfile.write(str(filledSpaces))
with open("time.txt", "w") as outfile:
    outfile.write(str(end-start))
