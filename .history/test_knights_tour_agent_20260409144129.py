
from time import time

import pytest

from knights_tour_GUI import Chessboard
from knights_tour_agent import KnightsTourAgent

[pytest]
timeout = 10

@pytest.fixture(scope="session")
def results_collector():
    results = []
    yield results
    print("-----TESTS COMPLETE----\n")

@pytest.fixture
def build_chessboard():
    def _make(dimension_x, dimension_y, starting_pos, obstacle_boxes=0):
        #only change the GUI and render delay if you need to visually see the test
        board = Chessboard(GUI=False, render_delay_sec=0.00, grid_rows=dimension_y, grid_cols=dimension_x, starting_knight_pos=starting_pos, obstacle_boxes=obstacle_boxes)
        agent = KnightsTourAgent(board)
        return board, agent

    return _make




class TestKnightsTour:

    @pytest.mark.parametrize("dimension_x, dimension_y,starting_pos, obstacle_boxes, expected", [
        # your configs here for each chessboard
        # (num_rows, num_cols, starting_pos, num_obstacles, solvable? (True/False) )
        ##### Solvable ####

        # SQUARES
        (4, 6, (0, 0), 0, True),
        (6, 6, (0, 0), 0, True),
        (7, 7, (0, 0), 0, True),
        (8, 8, (0, 0), 0, True),
        (12, 12, (0, 0), 0, True),
        (16, 16, (0, 0), 0, True),
        (20, 20, (0, 0), 0, True),

        # # RECTANGLES
        (5, 6, (0, 0), 0, True),
        (6, 8, (0, 0), 0, True),
        (8, 10, (0, 0), 0, True),
        (6, 10, (0, 0), 0, True),
        (5, 8, (0, 0), 0, True),

        # OBSTACLES - Extremely Difficult to Determine
        # (6, 6, (0, 0), 2, True),
        # (7, 7, (0, 0), 1, True),
        # (8, 8, (0, 0), 4, True),
        # (10, 10, (0, 0), 3, True),
        # (5, 6, (0, 0), 1, True),
        # (5, 8, (0, 0), 3, True),
        # (6, 8, (0, 0), 5, True),
        # (6, 10, (0, 0), 10, True),
        # (8, 10, (0, 0), 6, True),
        # (3, 4, (0, 0), 2, True),
        # (3, 8, (0, 0), 8, True),

        # INTERESTING CASES
        # # Solvable 3's are 3xN where N is a multiple of 4
        (3, 12, (0, 0), 0, True),
        (3, 8, (0, 0), 0, True),

        # # 5x5 in specific starting positions
        (5, 5, (1, 3), 0, True),
        (5, 5, (0, 0), 0, True),
        (5, 5, (4, 4), 0, True),
        (5, 5, (3, 4), 0, False),
        (5, 5, (2, 3), 0, False),

        # LONG SOLVES
        (4, 3, (0, 0), 0, True), # Around 9 Seconds
        (8, 4, (0, 0), 0, True), # Around 29 Seconds

        #### Mathematically Unsolvable #####
        (3, 3, (0, 0), 0, False),
        (2, 1, (0, 0), 0, False),
        (4, 4, (0, 0), 0, False),


    ])

    def test_knights_tour(self, dimension_x, dimension_y, starting_pos, obstacle_boxes, expected, build_chessboard, results_collector):
        start_time = time()
        board, agent = build_chessboard(dimension_x, dimension_y, starting_pos, obstacle_boxes)
        try:
            agent.knights_tour()
            solved = agent.done
        except Exception:
            print("TIMEOUT HIT")
            solved = False
        finally:
            end_time = time()
        results_collector.append({
    "board_label": f"{dimension_x}x{dimension_y}",
    "dimensions": (dimension_x, dimension_y),
    "starting_pos": starting_pos,
    "depth": 1,
    "solved": solved,
    "time_seconds": end_time - start_time,
    "backtrack_count": getattr(agent, 'backtrack_count', 0),
    "move_count": len(agent.placedKnights),
    "restarts": getattr(agent, 'restarts', 0),
})
        assert expected == solved
