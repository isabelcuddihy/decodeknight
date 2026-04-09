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
