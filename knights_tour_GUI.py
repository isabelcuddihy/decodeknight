import time
import pygame
import numpy as np
import random


class Chessboard:
    def __init__(self, GUI=True, render_delay_sec=0.1, grid_rows=6, grid_cols = 6, starting_knight_pos=(0, 0), obstacle_boxes=5):
        # Constants
        self.grid_rows = grid_rows #eventually need to do something with width too for m x n grids
        self.grid_cols = grid_cols
        self.gridSize = self.grid_rows * self.grid_cols
        self.cellSize = 25
        self.cellWidth = self.grid_cols * self.cellSize
        self.cellHeight = self.grid_rows * self.cellSize
        self.fps = 60
        self.sleeptime = render_delay_sec
        self.currentKnightPos = (starting_knight_pos[0], starting_knight_pos[1]) # (y, x) format
        self.placedKnights = []
        self.grid = np.full((grid_rows, grid_cols), -1)
        self.grid[self.currentKnightPos[0]][self.currentKnightPos[1]] = 1
        self.placedKnights.append(self.currentKnightPos)
        self.obstacle_boxes = obstacle_boxes


        #Design choices for numbers and colors for GUI
        self.black = (0,0,0)
        self.white = (255, 255, 255)
        self.blue = (254, 198, 78)
        self.status = ["#FFFFFF", "#64EFFF"]  # empty, visited

        # Shape definitions represented by arrays
        self.moves = [ (1, -2), # 2 left 1 up
                      (-1, -2),  # 2 left 1 down
                      (1, 2), # 2 right 1 up
                      (-1, 2), # 2 right 1 down
                      (-2, 1),  # 2 up 1 left
                      (-2, -1), # 2 up 1 right
                      (2, 1), # 2 down 1 left
                      (2, -1)# 2 down 1 right
        ]


        # Global variables (now instance attributes)
        self.screen = None
        self.clock = None

        self.done = False


        # Initialize grid with random obstacles
        # if obstacle_boxes > 0:
        #     self.addRandomObstacleBoxes(self.grid)

        # Initialize the graphical interface (if enabled)
        if GUI:
            pygame.init()
            pygame.font.init()
            self.font = pygame.font.SysFont(None, 24)
            # Draw knight symbol on current position
            self.knight_font = pygame.font.SysFont("applesymbols", 28) # font that supports chess symbols
            self.screen = pygame.display.set_mode((self.cellWidth, self.cellHeight))
            pygame.display.set_caption("Chessboard")
            self.clock = pygame.time.Clock()

            self._refresh()
    # Movements of the knight
    def execute(self, command='e', position=None):
        # Command-based environment interaction similar to Gym
        if command.lower() in ['e', 'export']:
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='e', key=ord('e'))
            try:
                pygame.event.post(new_event)
                self._refresh()
            except:
                pass
            return self.currentKnightPos, self.grid, self.placedKnights, self.done
        elif command.lower() in ['p', 'place']:
            if self.canPlace(self.grid,  position):
                self._placeKnight(self.grid,  position)
                self.currentKnightPos = position
                self.placedKnights.append(( self.currentKnightPos))
                self._exportGridState(self.grid)
                new_event = pygame.event.Event(pygame.KEYDOWN, unicode='p', key=ord('p'))
                try:
                    pygame.event.post(new_event)
                    self._refresh()
                except:
                    pass
                if self.checkGrid(self.grid):
                    self.done = True
                else:
                    self.done = False
       
        elif command.lower() in ['u', 'undo']:
            if len(self.placedKnights) > 1:
                self.placedKnights.pop()
                last_knight_pos= self.placedKnights[-1]
                self._removeKnight(self.grid, self.currentKnightPos)
                self.currentKnightPos = last_knight_pos
                if self.checkGrid(self.grid):
                    self.done = True
                else:
                    self.done = False
                new_event = pygame.event.Event(pygame.KEYDOWN, unicode='u', key=ord('u'))
                try:
                    pygame.event.post(new_event)
                    self._refresh()
                except:
                    pass

        return self.currentKnightPos, self.grid, self.placedKnights, self.done

    def canPlace(self, grid, pos):
        # Does knight fit in grid and is position empty
        if (pos[0] >= self.grid_rows or pos[1] >= self.grid_cols or pos[0] < 0 or pos[1] < 0):
            return False
        # check for filled square or obstacle
        if grid[pos[0]][pos[1]] != -1:  # check DESTINATION, not current pos
            return False

        return True

    def checkGrid(self, grid):
        # Ensure all cells are filled
        if -1 in grid:
            return False

        return True

    # All other methods are private (no requirement for public)

    def _drawGrid(self, screen):
        for col in range(0, self.cellWidth, self.cellSize):
            for row in range(0, self.cellHeight, self.cellSize):
                rect = pygame.Rect(col, row, self.cellSize, self.cellSize)
                pygame.draw.rect(screen, self.blue, rect, 1)

    def _placeKnight(self, grid, pos):

        grid[pos[0]][pos[1]] = len(self.placedKnights) + 1
        
    def _removeKnight(self, grid, pos):
        grid[pos[0]][pos[1]] = -1

    def _exportGridState(self, grid):
        ## To export the grid for debug purposes.
        return grid

    def _importGridState(self, gridState):
        ## Can be used to import a grid for same atarting conditions from a file.
        grid = np.array([ord(char) - 65 for char in gridState]).reshape((self.gridSize, self.gridSize))
        return grid

    def _refresh(self):
        if not self.screen:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        self.screen.fill(self.white)
        self._drawGrid(self.screen)

        # Draw visited squares with move numbers
        for i in range(self.grid_rows):
            for j in range(self.grid_cols):
                if self.grid[i, j] != -1:
                    rect = pygame.Rect(j * self.cellSize, i * self.cellSize, self.cellSize, self.cellSize)
                    pygame.draw.rect(self.screen, self.status[1], rect)
                    move_number = self.grid[i, j]
                    if move_number > 0:
                        text = self.font.render(str(move_number), True, self.black)
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)

        # Draw knight symbol on current position - outside the loop
        knight_text = self.knight_font.render("♞", True, self.black)
        knight_rect = knight_text.get_rect(center=(
            self.currentKnightPos[1] * self.cellSize + self.cellSize // 2,
            self.currentKnightPos[0] * self.cellSize + self.cellSize // 2
        ))
        self.screen.blit(knight_text, knight_rect)

        pygame.display.flip()
        self.clock.tick(self.fps)
        time.sleep(self.sleeptime)

    def addRandomObstacleBoxes(self, grid):
        ## Adds the random obstacle boxes.
        empty_positions = list(zip(*np.where(grid == -1)))
        random_positions = random.sample(empty_positions, min(self.obstacle_boxes, len(empty_positions)))

        # Place random colored boxes at selected positions
        for pos in random_positions:
            grid[pos[0], pos[1]] = 0

    def _loop_gui(self):
        ## Main Loop for the GUI
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill(self.white)
            self._drawGrid(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            self._refresh()

        pygame.quit()

    def _printGridState(self, grid):
        ## Utility method. Can be used for debugging.
        for row in grid:
            print(' '.join(f'{cell:2}' for cell in row))
        print()
    def _status(self):
        ## Utility method. Can be used for debugging.
        print(f"Current Knight Position: {self.currentKnightPos}")
        print(f"Current Grid State:\n{self.grid}")
        print(f"Placed Knights: {self.placedKnights}")
        print(f"Done: {self.done}")


    def _main(self):
        ## Allows manual control over the environment.
        self._loop_gui()


if __name__ == "__main__":
    game = Chessboard(True, render_delay_sec=0.1, grid_rows=6, grid_cols=6, starting_knight_pos=(0, 0), obstacle_boxes=0)
    game._status()
    game._main()

