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
        chessboard.execute("place", next_move) 
        
        # recursively try to solve from the new position
        if warnsdorff_solver(next_move, move_count + 1):
            return True
        
        # if we fail (dead end) then backtrack
        chessboard.execute("undo")
        
    return False


# How recursion breaks:
# 1. The agent sees a node with a score of 0 (no onward moves) and because it's got the lowest score it picks it first
# 2. The agent calls solve(node_with_zero, move_count + 1)
# 3. Inside this new function call, nodes = valid_moves(current_pos) returns an empty list []
# 4. Since the list is empty the "for next_move in nodes:" loop never runs and is skipped entirely
# 5. this solve() call returns FALSE and exits out. chessboard.execute("undo") refills -1 in the matrix. 
# 6. "for next_move in nodes" picks the next lowest node. If it has a score > 0, our recursive cycle begins again. If not we go through all nodes until we find one that does or backtrack a second time, and so on and so forth.