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
currentKnightPos, moveChoice, grid, placedKnights, done = game.execute('export')
np.savetxt('initial_grid.txt', grid, fmt="%d")

currentKnightPos, moveChoice, grid, placedKnights, done = game.execute('export')

print(currentKnightPos, moveChoice, grid, placedKnights, done)


####################################################
# Timing your code's execution for metrics.
####################################################

start = time.time()  # <- do not modify this.



'''
Main idea
State Space: Current Grid with all accepted moves
Action Space: Copy of Current Grid with new potential move placed
Objective Function:  squares_filled - (remaining * some penalty amount)
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
Function builds all the commands needed to execute the desired new move in the original grid
Params - (x_move :INT )how many horizontal steps to execute
(y_move :INT )how many vertical steps to execute
Returns - list of strings containing the commands needed to execute the desired new move in the original grid
'''
def setUpCommandExecution(grid, possible_valid_move):

   warnsdorff_solver(possible_valid_move, move_count + 1)
end=time.time()
print(f"Solved with {end-start} seconds of execution time!")

game._main()
np.savetxt('grid.txt', grid, fmt="%d")
with open("final_grid.txt", "w") as outfile:
    outfile.write(str(filledSpaces))

