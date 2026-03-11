# decodeknight
Foundations of AI Final CS5100 Project-  Decode Knight: a Knight's Tour Solver
A Python implementation of solving the Knight's Tour problem on configurable chessboards.
Problem Overview
The Knight's Tour is a sequence of chess knight moves such that the knight visits every square on the board exactly once. This project explores solutions across increasingly complex environments:

Phase 1: Standard n×n fully deterministic, fully observable board
Phase 2: Boards with obstacles / dead squares
Phase 3: Rectangular n×m boards

Possible Algorithmic Approaches

Backtracking — exhaustive depth-first search with pruning
Warnsdorff's Heuristic — greedy approach that prioritizes moves with the fewest onward options
Bisected Knight’s Tour / Quadrisected Knight’s Tour - Breaking the chessboard into smaller identical sections and solving them using the same pattern
