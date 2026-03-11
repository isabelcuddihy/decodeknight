import time
import pygame
import numpy as np
import random

class Chessboard:
    def __init__(self, GUI=True, render_delay_sec=0.1, gs=6, num_colored_boxes=5):
        # Constants
        self.gridSize = gs
        self.cellSize = 40
        self.screenSize = self.gridSize * self.cellSize
        self.fps = 60
        self.sleeptime = render_delay_sec

        # Basic color definitions
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        # Color palette for moves
        self.status = ["#FFFFFF", "#000000"]
        # Mapping of status indices to status names (for debugging purposes)
        self.statusIndexToName = {0: "Empty", 1: "Filled"}

        # Shape definitions represented by arrays
        self.moves = [
             # 2 left 1 up
             # 2 left 1 down
             # 2 right 1 up
             # 2 right 1 down
             # 2 up 1 left
             # 2 up 1 right
             # 2 down 1 left
             # 2 down 1 right
        ]

        # Corresponding dimensions of the moves
        self.moveDimesions = [
            (1, -2),
            (-1, -2),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (2, 1),
            (2, -1),
            (2, 1), 
            (2, -1)
        ]

        # Mapping of shape indices to shape names (for debugging purposes)
        self.shapesIdxToName = {
            0: "Up2Left1",
            1: "Up2Right1",
            2: "Down2Left1",
            3: "Down2Right1",
            4: "Right2Up1",
            5: "Right2Down1",
            6: "Left2Up1",
            7: "Left2Down1",
        }

        # Global variables (now instance attributes)
        self.screen = None
        self.clock = None
        self.grid = np.full((self.gridSize, self.gridSize), -1)
        self.currentShapeIndex = 0
        self.currentColorIndex = 0
        self.knightPos = [0, 0]
        self.placedShapes = []
        self.done = False

        # Initialize grid with random obstacles - In Progress
        self._addRandomColoredBoxes(self.grid, num_colored_boxes)

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
            return self.knightPos, self.currentShapeIndex, self.currentColorIndex, self.grid, self.placedShapes, self.done
        if command.lower() in ['w', 'up']:
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='w', key=ord('w'))
            try:
                pygame.event.post(new_event)
                self._refresh()
            except:
                pass
            self.knightPos[1] = max(0, self.knightPos[1] - 1)
        elif command.lower() in ['s', 'down']:
            self.knightPos[1] = min(self.gridSize - len(self.moves[self.currentShapeIndex]), self.knightPos[1] + 1)
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='s', key=ord('s'))
            try:
                pygame.event.post(new_event)
                self._refresh()
            except:
                pass
        elif command.lower() in ['a', 'left']:
            self.knightPos[0] = max(0, self.knightPos[0] - 1)
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='a', key=ord('a'))
            try:
                pygame.event.post(new_event)
                self._refresh()
            except:
                pass
        elif command.lower() in ['d', 'right']:
            self.knightPos[0] = min(self.gridSize - len(self.moves[self.currentShapeIndex][0]), self.knightPos[0] + 1)
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='d', key=ord('d'))
            try:
                pygame.event.post(new_event)
                self._refresh()
            except:
                pass
        elif command.lower() in ['p', 'place']:
            if self.canPlace(self.grid, self.moves[self.currentShapeIndex], self.knightPos):
                self._placeShape(self.grid, self.moves[self.currentShapeIndex], self.knightPos, self.currentColorIndex)
                self.placedShapes.append((self.currentShapeIndex, self.knightPos.copy(), self.currentColorIndex))
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
        elif command.lower() in ['h', 'switchshape']:
            self.currentShapeIndex = (self.currentShapeIndex + 1) % len(self.moves)
            currentShapeDimensions = self.moveDimesions[self.currentShapeIndex]
            xXented = self.knightPos[0] + currentShapeDimensions[0]
            yXetended = self.knightPos[1] + currentShapeDimensions[1]

            if (xXented > self.gridSize and yXetended > self.gridSize):
                self.knightPos[0] -= (xXented - self.gridSize)
                self.knightPos[1] -= (yXetended - self.gridSize)
            elif (yXetended > self.gridSize):
                self.knightPos[1] -= (yXetended - self.gridSize)
            elif (xXented > self.gridSize):
                self.knightPos[0] -= (xXented - self.gridSize)

            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='h', key=ord('h'))

            try:
                pygame.event.post(new_event)
                self._refresh()
            except:
                pass
        elif command.lower() in ['k', 'switchcolor']:
            self.currentColorIndex = (self.currentColorIndex + 1) % len(self.status)
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='k', key=ord('k'))
            try:
                pygame.event.post(new_event)
                self._refresh()
            except:
                pass
        elif command.lower() in ['u', 'undo']:
            if self.placedShapes:
                lastShapeIndex, lastShapePos, lastColorIndex = self.placedShapes.pop()
                self._removeShape(self.grid, self.moves[lastShapeIndex], lastShapePos)
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

        return self.knightPos, self.currentShapeIndex, self.currentColorIndex, self.grid, self.placedShapes, self.done

    def canPlace(self, grid, shape, pos):
        # Does knight fit in grid and is position empty
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    if pos[0] + j >= self.gridSize or pos[1] + i >= self.gridSize:
                        return False
                    if grid[pos[1] + i, pos[0] + j] != -1:
                        return False
        # Check for filled square
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

    def _drawShape(self, screen, shape, color, pos):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((pos[0] + j) * self.cellSize, (pos[1] + i) * self.cellSize, self.cellSize, self.cellSize)
                    pygame.draw.rect(screen, color, rect, width=6)

    def _placeShape(self, grid, shape, pos, colorIndex):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    grid[pos[1] + i, pos[0] + j] = colorIndex

    def _removeShape(self, grid, shape, pos):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    grid[pos[1] + i, pos[0] + j] = -1

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

        # Draw the shape that is currently selected by the user
        self._drawShape(self.screen, self.moves[self.currentShapeIndex], self.status[self.currentColorIndex], self.knightPos)

        pygame.display.flip()
        self.clock.tick(self.fps)
        time.sleep(self.sleeptime)

    def _addRandomColoredBoxes(self, grid, num_boxes=5):
        ## Adds the random colored boxes.
        empty_positions = list(zip(*np.where(grid == -1)))
        random_positions = random.sample(empty_positions, min(num_boxes, len(empty_positions)))

        # Place random colored boxes at selected positions
        for pos in random_positions:
            color_index = self.getAvailableColor(grid, pos[1], pos[0])
            grid[pos[0], pos[1]] = color_index

    def _loop_gui(self):
        ## Main Loop for the GUI
        running = True
        while running:
            self.screen.fill(self.white)
            self._drawGrid(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Handle key events to move moves and perform actions
                    if event.key == pygame.K_w:
                        self.knightPos[1] = max(0, self.knightPos[1] - 1)
                    elif event.key == pygame.K_s:
                        self.knightPos[1] = min(self.gridSize - len(self.moves[self.currentShapeIndex]), self.knightPos[1] + 1)
                    elif event.key == pygame.K_a:
                        self.knightPos[0] = max(0, self.knightPos[0] - 1)
                    elif event.key == pygame.K_d:
                        self.knightPos[0] = min(self.gridSize - len(self.moves[self.currentShapeIndex][0]), self.knightPos[0] + 1)
                    elif event.key == pygame.K_p:  # Place the shape on the grid
                        if self.canPlace(self.grid, self.moves[self.currentShapeIndex], self.knightPos):
                            self._placeShape(self.grid, self.moves[self.currentShapeIndex], self.knightPos, self.currentColorIndex)
                            self.placedShapes.append((self.currentShapeIndex, self.knightPos.copy(), self.currentColorIndex))
                            if self.checkGrid(self.grid):
                                # Calculate and display score based on the number of moves used
                                score = (self.gridSize**2) / len(self.placedShapes)
                                print("All cells are covered with no overlaps and no adjacent same status! Your score is:", score)
                            else:
                                print("Grid conditions not met!")
                    elif event.key == pygame.K_h:  # Switch to the next shape
                        self.currentShapeIndex = (self.currentShapeIndex + 1) % len(self.moves)
                        currentShapeDimensions = self.moveDimesions[self.currentShapeIndex]
                        xXented = self.knightPos[0] + currentShapeDimensions[0]
                        yXetended = self.knightPos[1] + currentShapeDimensions[1]

                        if (xXented > self.gridSize and yXetended > self.gridSize):
                            self.knightPos[0] -= (xXented - self.gridSize)
                            self.knightPos[1] -= (yXetended - self.gridSize)
                        elif (yXetended > self.gridSize):
                            self.knightPos[1] -= (yXetended - self.gridSize)
                        elif (xXented > self.gridSize):
                            self.knightPos[0] -= (xXented - self.gridSize)

                        print("Current shape", self.shapesIdxToName[self.currentShapeIndex])
                    elif event.key == pygame.K_k:  # Switch to the next color
                        self.currentColorIndex = (self.currentColorIndex + 1) % len(self.status)
                    elif event.key == pygame.K_u:  # Undo the last placed shape
                        if self.placedShapes:
                            lastShapeIndex, lastShapePos, lastColorIndex = self.placedShapes.pop()
                            self._removeShape(self.grid, self.moves[lastShapeIndex], lastShapePos)
                    elif event.key == pygame.K_e:  # Export the current grid state
                        gridState = self._exportGridState(self.grid)
                        print("Exported Grid State: \n", gridState)
                        print("Placed Shapes:", self.placedShapes)
                    elif event.key == pygame.K_i:  # Import a dummy grid state (for testing)
                        dummyGridState = self._exportGridState(np.random.randint(-1, 4, size=(self.gridSize, self.gridSize)))
                        self.grid = self._importGridState(dummyGridState)
                        self.placedShapes.clear()  # Clear history since we are importing a new state

            # Draw all placed moves
            for i in range(self.gridSize):
                for j in range(self.gridSize):
                    if self.grid[i, j] != -1:
                        rect = pygame.Rect(j * self.cellSize, i * self.cellSize, self.cellSize, self.cellSize)
                        pygame.draw.rect(self.screen, self.status[self.grid[i, j]], rect)

            # Draw the current shape
            self._drawShape(self.screen, self.moves[self.currentShapeIndex], self.status[self.currentColorIndex], self.knightPos)

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
        print("W/A/S/D to move the moves.")
        print("H to change the shape.")
        print("K to change the color.")
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
