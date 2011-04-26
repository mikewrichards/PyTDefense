import pygame, sys, random
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("Tower Defense 0.1")

colors = {"black":(0, 0, 0), "red":(255, 0, 0), "green":(0, 255, 0),
          "blue":(0, 0, 255), "white":(255, 255, 255)}

#game data is initialized here
gridElements = {"empty":0, "enter":1, "exit":2}
moveElements = {"n/a":0, "up":8, "down":2, "left":4, "right":6}
clearTiles = (0, 1, 2)

grid = [[1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2]]

moveGrid = [[6, 6, 6, 6, 6, 6, 6, 2],
            [0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0]]

def checkGrid(grid, newGrid, x, y):
    if 0 <= y and y < len(newGrid) and y < len(grid):
        if 0 <= x and x < len(newGrid[y]) and x < len(grid[y]):
            if newGrid[y][x] == 0 and grid[y][x] in clearTiles:
                return 0
    return -1 

def calculateMove(grid, newGrid, x, y, endx, endy):
    if x == endx and y == endy:
        #at our destination
        return True
    
    if (checkGrid(grid, newGrid, x - 1, y) == 0 or
        checkGrid(grid, newGrid, x + 1, y) == 0 or
        checkGrid(grid, newGrid, x, y - 1) == 0 or
        checkGrid(grid, newGrid, x, y + 1) == 0):
        #an untested path exists
        if checkGrid(grid, newGrid, x + 1, y) == 0:
            #right
            newGrid[y][x] = 6
            if calculateMove(grid, newGrid, x + 1, y, endx, endy):
                return True
        if checkGrid(grid, newGrid, x, y + 1) == 0:
            #down
            newGrid[y][x] = 2
            if calculateMove(grid, newGrid, x, y + 1, endx, endy):
                return True
        if checkGrid(grid, newGrid, x - 1, y) == 0:
            #left
            newGrid[y][x] = 4
            if calculateMove(grid, newGrid, x - 1, y, endx, endy):
                return True
        if checkGrid(grid, newGrid, x, y - 1) == 0:
            #up
            newGrid[y][x] = 8
            if calculateMove(grid, newGrid, x, y - 1, endx, endy):
                return True
    #dead end
    return False


def calculateMoveGrid(grid, x, y):
    #this will be an implementation of the A* algorithm
    endx, endy = 0, 0
    for r, row in enumerate(grid):
        for e, element in enumerate(row):
            if element == 2:
                endx, endy = e, r
    newGrid = [[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]]
    calculateMove(grid, newGrid, x, y, endx, endy)
    return newGrid

def handleEvent(event):
    if event.type == QUIT:
        pygame.quit()
        sys.exit()

def gameLogic():
    x = 1

def drawMap():
    xsize = len(grid)
    ysize = len(grid[0])
    tilex = WINDOWWIDTH / xsize
    tiley = WINDOWHEIGHT / ysize
    for y, row in enumerate(grid):
        for x, element in enumerate(grid):
            pygame.draw.rect(surface, colors['white'],
                             pygame.Rect(x * tilex, y * tiley,
                                         tilex, tiley), 1)




def draw():
    surface.fill(colors['black'])
    drawMap()
    pygame.display.update()

print("ORIGINAL:")
for row in moveGrid:
    print(str(row))

print("GENERATED:")
for row in calculateMoveGrid(grid, 0, 0):
    print(str(row))

while True:
    for event in pygame.event.get():
        handleEvent(event)
    gameLogic()
    draw()
    clock.tick(60)
