import copy
import time
import numpy as np
import random

import knights_tour_GUI
from knights_tour_GUI import *
import sys

########################## CONTROL PANEL #################################################

# set limit high enough for a 50x50 board (2500 moves) plus some buffer for helper functions.
# adjust higher for larger NxN tests
########################## CONTROL PANEL #################################################
# adjust board dimensions (as rectangle)
DIM_X = 6 # columns
DIM_Y = 6 # rows

#4x6 didn't work but 5x6, 8x6, 8x16, 8x12, 13x11, 13x5, 6x5 did

# randomizes starting position, change to fixed coord e.g. (0,0) for testing
STARTING_POS = (random.randint(0, (DIM_Y - 1)), random.randint(0, (DIM_X - 1)))


# sets depth of search used for heuristic scoring. 1 = Standard Warnsdorff heurstic
# depth = 2 is Pohl's suggested value (can solve as large as 50x50 boards)
DEPTH = 1

# set limit high enough for a 128x128 board (16,384 squares) plus some buffer
# for helper functions. Adjust higher for larger NxN tests
sys.setrecursionlimit(20000)


######################################################################################
# The Knight's Tour is a classic problem in which the goal is to move a knight around a chessboard, visiting each square exactly once.
# The knight moves in an L-shape: two squares in one direction and then one square perpendicular to that.
# The challenge is to find a sequence of moves that allows the knight to visit every square on the board without repeating any square.
# In this implementation, we will use:
# A GUI to visualize the knight's movements on the chessboard.
# A grid to represent the chessboard, where each cell can be marked with the number move the knight just made and the knight's current position is indicated by a knight symbol.
# The objective is to find a sequence of moves that allows the knight to visit every square on the board without overlap and without having to backtrack/undo moves.
# Additional constraints can be added to make the problem more challenging, such as introducing obstacles on the board like "dead" squares and mandating the final square to be at a certain location..
####################################################


class KnightsTourAgent:
    def __init__(self, chessboard: knights_tour_GUI.Chessboard):
        self.game = chessboard
        self.currentKnightPos, self.grid, self.placedKnights, self.done = self.game.execute('export')
        np.savetxt('initial_grid.txt', self.grid, fmt="%d")

        self.currentKnightPos, self.grid, self.placedKnights, self.done = self.game.execute('export')
        self.grid_size = self.game.grid_rows * self.game.grid_cols
        self.grid_rows = self.game.grid_rows
        self.grid_cols = self.game.grid_cols
        self.backtrack_count = 0

        # print(self.currentKnightPos, self.grid, self.placedKnights,
        # self.done)


    #AGENT CODE BELOW

    def reset_grid(self, pos, starting_pos):
        # Resets the grid to its initial state with all cells unvisited (-1) except the starting position which is marked as visited (1).
        self.grid.fill(-1)  # Mark all cells as unvisited
        self.grid[pos[0], pos[1]] = 1  # Mark the starting position as visited
        self.grid[starting_pos[0], starting_pos[1]] = 1  # Ensure the starting position is marked as visited
        self.placedKnights.clear()  # Clear the list of placed knights
        return self.grid


    def get_valid_moves(self,current_pos):
        """
        Returns a list of (x, y) tuples for all legal knight moves
        from the current position that land on unvisited (-1) squares.
        """
        y, x = current_pos

        # defining all 8 possible "L" knight steps
        possible_steps = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        valid = []

        for y1, x1 in possible_steps:
            new_y, new_x = y + y1, x + x1

            # check if the move is within the grid boundaries
            if 0 <= new_x < self.grid_cols and 0 <= new_y < self.grid_rows:

                # check if the cell is unvisited (-1)
                if self.grid[new_y, new_x] == -1:
                    valid.append((new_y, new_x))

        return valid



    def recur_num_of_mov(self,node, level):
        # Temporarily mark current node to prevent cycles
        original_val = self.grid[node[0], node[1]]
        self.grid[node[0], node[1]] = 1

        children = self.get_valid_moves(node)

        # Base Case: Level 1 is just the count of immediate moves (just like Warnsdorff)
        if level == 1:
            self.grid[node[0], node[1]] = original_val # Restore before returning
            return len(children)

        # sum the connectivity of all children recursively
        total_connectivity = 0
        for child in children:
            total_connectivity += self.recur_num_of_mov(child, level - 1)

        self.grid[node[0], node[1]] = original_val # Restore before returning
        return total_connectivity



    def pohl_solver(self,current_pos, move_count, k=1):
        if move_count == (self.game.grid_cols * self.game.grid_rows):
            return True

        # Get valid moves using the live game grid
        nodes = self.get_valid_moves(current_pos)
        if not nodes:
            return False

        # score moves using Pohl's generalized rule
        scored_nodes = []
        for n in nodes:
            # We pass the grid to simulate connections at depth k
            score = self.recur_num_of_mov(n, k)
            scored_nodes.append((score, n))

        # pick moves with the fewest further moves first
        scored_nodes.sort()

        # execute the moves in the game (same as warnsdorff)
        for score, next_move in scored_nodes:
            self.game.execute("place", next_move)

            # recursive call to solve the rest of the board from the new position
            if self.pohl_solver(next_move, move_count + 1, k):
                return True

            # backtracking if we failed / we track wrong guesses
            self.backtrack_count += 1
            self.game.execute("undo")

        return False

    def print_game_results(self):
        print("Valid moves from start:", self.get_valid_moves(self.currentKnightPos))
        print("Placed knights:", self.placedKnights)
        print("Grid state:\n", self.grid)


    def knights_tour(self):
        # Timing code's execution for metrics
        start = time.time()  # <- do not modify this.

        self.pohl_solver(self.currentKnightPos, len(self.placedKnights),  k=DEPTH)

        end=time.time()
        self.done = self.game.checkGrid(self.game.grid)

        # self.print_game_results()
        # print(f"Solved with {end-start} seconds of execution time!")

        np.savetxt('grid.txt', self.grid, fmt="%d")
        with open("final_grid.txt", "w") as outfile:
            outfile.write(str(self.placedKnights))


if __name__ == '__main__':
    print("-----Welcome to the Knights Tour---- \n")
    agent = KnightsTourAgent(Chessboard(GUI=False, render_delay_sec=0.02, grid_rows=DIM_Y, grid_cols=DIM_X,
                                        starting_knight_pos=STARTING_POS, obstacle_boxes=0))
    agent.knights_tour()

######################### OUTDATED CODE ################################

# The function below (warnsdorff_solver) was v1 of our agent. It implemented Warnsdorff's basic heuristic and could solve standard 8x8 boards.
# Its functionality has been embedded in pohl_solver() and its output can be reproduced by setting DEPTH = 1 in control panel.

#def warnsdorff_solver(self,current_pos, move_count):
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
