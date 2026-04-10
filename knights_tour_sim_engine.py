import os
# Silences pygame starter print statement (slows down iterations)
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import sqlite3
import multiprocessing
import random
import time
from knights_tour_agent import KnightsTourAgent
from knights_tour_GUI import Chessboard


def setup_db():
    conn = sqlite3.connect('knights_tour_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            board_length INTEGER, board_width INTEGER,
            start_y INTEGER, start_x INTEGER, k_depth INTEGER,
            solved BOOLEAN, move_count INTEGER,
            backtrack_count INTEGER, execution_time REAL, timeout_hit BOOLEAN
        )
    ''')
    conn.commit()
    return conn, cursor


def run_single_tour(dim_y, dim_x, start_pos, k, return_dict):
    """Isolated tour process"""
    try:
        board = Chessboard(GUI=False, render_delay_sec=0.0,
                           grid_rows=dim_y, grid_cols=dim_x,
                           starting_knight_pos=start_pos)
        agent = KnightsTourAgent(board)  #

        start_time = time.time()
        success = agent.pohl_solver(start_pos, 1, k=k)  #
        end_time = time.time()

        return_dict['solved'] = success
        return_dict['move_count'] = len(board.placedKnights) if success else -1
        return_dict[
            'backtrack_count'] = agent.backtrack_count if not success == -1 else -1
        return_dict['execution_time'] = end_time - start_time
        return_dict['success_flag'] = True
    except Exception:
        return_dict['success_flag'] = False


def execute_with_timeout(dim_y, dim_x, start_pos, k, timeout=3.0):
    """Manages timeout kill-switch"""
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    return_dict['success_flag'] = False

    p = multiprocessing.Process(target=run_single_tour,
                                args=(dim_y, dim_x, start_pos, k, return_dict))
    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        p.join()
        return (False, -1, -1, timeout, True)  # signal for timeout bust

    if not return_dict.get('success_flag', False):
        return (False, 0, 0, 0, False)

    return (return_dict['solved'], return_dict['move_count'],
            return_dict['backtrack_count'], return_dict['execution_time'],
            False)


if __name__ == '__main__':
    conn, cursor = setup_db()
    # 5 boards in a square config of increasing size
    # 5 boards in a rectangular config of increasing LxW ratio
    boards = [(8, 8), (16, 16), (32, 32), (64, 64), (128, 128),
              (8, 16), (8, 24), (8, 32), (8, 40), (8, 48)]

    MAX_SAMPLES = 30    # just a test figure, we could go higher when ready

    for y, x in boards:
        print(f"\nBoard {y}x{x}:")

        # If number of squares is less/equal to x, sim tour for every grid pos
        if (y * x) <= 64:
            starts = [(i, j) for i in range(y) for j in range(x)]
        # Otherwise sample x tours from random starting pos (max samples above)
        else:
            starts = [(random.randint(0, y - 1), random.randint(0, x - 1)) for
                      _ in range(MAX_SAMPLES)]

        # Simulating for 3 k-depths levels
        for k in [1, 2, 3]:
            print(f"  k={k} processing...", end="", flush=True)
            batch_data = []  # Collect rows for bulk insert

            for start_pos in starts:
                # Get tuple of results
                res = execute_with_timeout(y, x, start_pos, k, timeout=3.0)
                #(y, x, start_y, start_x, k, solved, moves, backtracks, time, timeout)
                batch_data.append((y, x, start_pos[0], start_pos[1], k, *res))

            # batch insert to save I/O execution time
            cursor.executemany('''
                INSERT INTO simulations (board_length, board_width, start_y, start_x, k_depth, 
                                         solved, move_count, backtrack_count, execution_time, timeout_hit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', batch_data)

            conn.commit()  # one batch insert per k-depth
            print("Done.")

    conn.close()
    print("\nSimulation complete!")