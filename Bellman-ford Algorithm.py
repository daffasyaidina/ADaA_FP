from tkinter import messagebox, Tk 
import pygame
import sys

pygame.display.set_caption('Bellman-Ford Path Finding Visualizer') 

windowWidth = 800 # Window Size
windowHeight = 800

window = pygame.display.set_mode((windowWidth, windowHeight)) # Create Window

columns = 50 # Grid Size
rows = 50

boxWidth = windowWidth // columns
boxHeight = windowHeight // rows

grid = []
queue = []
path = []

class Box:
    def __init__(self, i, j): # Box Constructor
        self.x = i
        self.y = j
        self.start = False
        self.queued = False
        self.visited = False
        self.target = False
        self.wall = False
        self.neighbours = []
        self.prior = None
        self.distance = float('inf')

    def setNeighbours(self): # Set Neighbours
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

    def draw(self, win, color):# Draw Box
        pygame.draw.rect(win, color, (self.x * boxWidth, self.y * boxHeight, boxWidth-2, boxHeight-2))

# Create Grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

# Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].setNeighbours()

startBox = grid[0][0] # Start Box
startBox.start = True
startBox.distance = 0
queue.append(startBox)

def main(): # Main Loop
    beginSearch = False
    targetBoxSet = False
    searching = True
    targetBox = None

    while True:
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Draw Wall
                if event.buttons[0]:
                    i = x // boxWidth
                    j = y // boxHeight
                    grid[i][j].wall = True
                # Set Target
                if event.buttons[2] and not targetBoxSet:
                    i = x // boxWidth
                    j = y // boxHeight
                    targetBox = grid[i][j]
                    targetBox.target = True
                    targetBoxSet = True

            #start algorithm
            if event.type == pygame.KEYDOWN and targetBoxSet:
                beginSearch = True

        if beginSearch:
            if len(queue) > 0 and searching:
                currentBox = queue.pop(0)
                currentBox.visited = True
                for i in range(columns):
                    for j in range(rows):
                        currentBox = grid[i][j]
                        if currentBox.distance == float('inf'):
                            continue
                        for neighbour in currentBox.neighbours:
                            if neighbour.wall:
                                continue
                            if neighbour.distance > currentBox.distance + 1:
                                neighbour.distance = currentBox.distance + 1
                                neighbour.prior = currentBox
                                if neighbour == targetBox:
                                    searching = False
                                    while neighbour.prior != startBox:
                                        path.append(neighbour.prior)
                                        neighbour = neighbour.prior

            else: #No solution
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo('No Solution','Solution Not Found')
                    searching = False

        # Draw Grid
        window.fill((28, 28, 30)) # Draw Grid

        for i in range(columns): # Draw Boxes
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (72, 72, 74))

                if box.start: # Draw Box Type
                    box.draw(window, (48, 219, 91)) 
                if box.wall: 
                    box.draw(window, (44, 44, 46))
                if box.target:
                    box.draw(window, (255, 214, 10))
                if box.queued:
                    box.draw(window, (255, 69, 58))
                if box.visited:
                    box.draw(window, (48, 209 , 88))
                if box in path:
                    box.draw(window, (10, 132, 255))

        pygame.display.update() # Update Window

main()
  
                
