import time
import pygame
import numpy as np
import random

class Chessboard:
    def __init__(self, GUI=True, render_delay_sec=0.1, grid_length=6, grid_width = 6, obstacle_boxes=5):
        # Constants
        self.gridSize = grid_length * grid_width
        self.cellSize = 40
        self.screenSize = self.gridSize * self.cellSize
        self.fps = 60
        self.sleeptime = render_delay_sec
        self.placedKnights = [] # List to track prev ious knight positions in order (position, move number)
        self.obstacle_boxes = obstacle_boxes

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
        self.grid = np.full((self.gridSize, self.gridSize), -1)
        self.currentKnightPos = [0, 0]
        self.moveChoice = 0 # Index to track the current move choice from self.moves
        self.done = False

        # Initialize grid with random obstacles - In Progress
        # self._addRandomColoredBoxes(self.grid, num_colored_boxes)

        # Initialize the graphical interface (if enabled)
        if GUI:
            pygame.init()
            self.screenSize = self.gridSize * self.cellSize
            self.screen = pygame.display.set_mode((self.screenSize, self.screenSize))
            pygame.display.set_caption("Chessboard")
            self.clock = pygame.time.Clock()

            self._refresh()
    # Movements of the knight
    def execute(self, command='e'):
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
            if self.canPlace(self.grid, self.moves[self.moveChoice], self.currentKnightPos):
                self._placeKnight(self.grid, self.moves[self.moveChoice], self.currentKnightPos, self.currentColorIndex)
                self.placedKnights.append(( self.currentKnightPos, len(self.placedKnights) + 1))
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
            if self.placedKnights:
                lastShapeIndex, lastShapePos, lastColorIndex = self.placedKnights.pop()
                self._removeKnight(self.grid, self.moves[lastShapeIndex], lastShapePos)
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

        return self.currentKnightPos, self.moveChoice, self.grid, self.placedKnights, self.done

    def canPlace(self, grid, pos):
        # Does knight fit in grid and is position empty
        if pos[0]  >= self.gridSize or pos[1] >= self.gridSize:
            return False
        # Check for filled square
        if grid[pos[0]][pos[1]] != -1:
            return False
        return True

    def checkGrid(self, grid):
        # Ensure all cells are filled
        if -1 in grid:
            return False

        return True


    # All other methods are private (no requirement for public)

    def _drawGrid(self, screen):
        for x in range(0, self.screenSize, self.cellSize):
            for y in range(0, self.screenSize, self.cellSize):
                rect = pygame.Rect(x, y, self.cellSize, self.cellSize)
                pygame.draw.rect(screen, self.black, rect, 1)

    def _placeKnight(self, grid, pos):
        grid[pos[0]][pos[1]] = 1
        

    def _removeKnight(self, grid, pos):
        grid[pos[0]][pos[1]] = -1
        self.placedKnights.pop() # Remove the last placed knight from the list

    def _exportGridState(self, grid):
        ## To export the grid for debug purposes.
        return grid

    def _importGridState(self, gridState):
        ## Can be used to import a grid for same atarting conditions from a file.
        grid = np.array([ord(char) - 65 for char in gridState]).reshape((self.gridSize, self.gridSize))
        return grid

    def _refresh(self):
        self.screen.fill(self.white)
        self._drawGrid(self.screen)

        # Draw the current state of the grid
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if self.grid[i, j] != -1:
                    rect = pygame.Rect(j * self.cellSize, i * self.cellSize, self.cellSize, self.cellSize)
                    pygame.draw.rect(self.screen, self.status[self.grid[i, j]], rect)

        pygame.display.flip()
        self.clock.tick(self.fps)
        time.sleep(self.sleeptime)

    # def _addRandomColoredBoxes(self, grid, num_boxes=5):
    #     ## Adds the random colored boxes.
    #     empty_positions = list(zip(*np.where(grid == -1)))
    #     random_positions = random.sample(empty_positions, min(num_boxes, len(empty_positions)))

    #     # Place random colored boxes at selected positions
    #     for pos in random_positions:
    #         color_index = self.getAvailableColor(grid, pos[1], pos[0])
    #         grid[pos[0], pos[1]] = color_index

    def _loop_gui(self):
        ## Main Loop for the GUI
        running = True
        while running:
            self.screen.fill(self.white)
            self._drawGrid(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()

    def _printGridState(self, grid):
        ## Utility method. Can be used for debugging.
        for row in grid:
            print(' '.join(f'{cell:2}' for cell in row))
        print()

    def _printControls(self):
        ## Prints the controls for manual control
        print("P to place the shape.")
        print("U to undo the last placed shape.")
        print("E to print the grid state from GUI to terminal.")
        print("I to import a dummy grid state.")
        print("Q to quit (terminal mode only).")
        print("Press any key to continue")

    def _main(self):
        ## Allows manual control over the environment.
        self._loop_gui()


if __name__ == "__main__":
    # printControls() and main() now encapsulated in the class:
    game = Chessboard(True, render_delay_sec=0.1, gs=6, num_colored_boxes=5)
    game._printControls()
    game._main()
