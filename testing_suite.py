#PTest Suite for Agent Analysis

# Runs Warnsdorff's heuristic on the knight's tour problem and prints the resulting grid and path taken by the knight. 
# Runs Pohls algorithm on the knight's tour problem and prints the resulting grid and path taken by the knight.
# Time to execute, numbers of resets, number of moves
# Graphs - time to execute vs depth, number of resets vs depth, number of moves vs depth
# Comparison between the two algos for these metrics
# Don't go above 4 for depth, otherwise it takes too long to run.

import numpy as np
import random
from knights_tour_agent import reset_grid, get_valid_moves
from knights_tour_GUI import Chessboard
import pytest


def pohl_solver(self, current_pos, move_count, k=1, reset=0):
    if move_count == (self.game.gridSize * self.game.gridSize):
        return True

    reset_count = reset
    starting_pos = self.placedKnights[0]
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
    if reset_count > 0:
        scored_nodes.pop(reset_count-1)   # offset index by one

    if not scored_nodes:
        print("Out of reset options")
        return False

    # execute the moves in the game (same as warnsdorff)
    for score, next_move in scored_nodes:
        self.game.execute("place", next_move)

        # recursive call to solve the rest of the board from the new position
        if self.pohl_solver(next_move, move_count + 1, k):
            return True

        # Hit a dead-end
        break
    # resetting to starting position
    self.game.reset_grid(current_pos, starting_pos)
    # Increasing reset count
    reset += 1
    self.pohl_solver(starting_pos, 1, k, reset_count)






