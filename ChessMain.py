# Driver File
# Handles User Input and display current game state

import pygame as p
import numpy as np
from ChessEngine import *

p.init()
p.display.set_caption('Beaver')
FONT = p.font.Font('freesansbold.ttf', 10)
WIDTH = HEIGHT = 512
DIMENSION = 8
CELL_SIZE = HEIGHT// DIMENSION
MAX_FPS = 15
IMAGES = {}
GREY = (119, 132, 102)
WHITE =  (189, 196, 180)
BG = (60, 70, 50)
INDENT = 18

#should be called only once
def loadImages():
    pieces = np.array(["bR", "bN", "bB", "bK", "bQ", "bB", "bB", "bN", "bR","bP",
              "wR", "wN", "wB", "wK", "wQ", "wB", "wB", "wN", "wR","wP"])
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"),(CELL_SIZE,CELL_SIZE))
        #now we can access the IMAGES dictionary
    
# GUI
def drawGameState(screen,gameState):
    drawBoardAndPieces(screen,gameState)       #draw cells & pieces

def drawRanksAndFiles(screen):
    for i in range(DIMENSION):
        rank = str(DIMENSION-i)
        rankBox = FONT.render(rank, True, WHITE)
        screen.blit(rankBox, (INDENT//2, i*CELL_SIZE + INDENT +CELL_SIZE//2))
    files = {7: "a",6:  "b",5: "c",4: "d",3: "e",2: "f",1: "g",0: "h"}
    for j in range(DIMENSION):
        file = files[DIMENSION-j-1]
        fileBox = FONT.render(file, True, WHITE)
        screen.blit(fileBox, (j*CELL_SIZE + INDENT +CELL_SIZE//2,HEIGHT+ INDENT+INDENT//4))


def drawBoardAndPieces(screen,gameState):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = WHITE if (i+j)%2==0 else GREY
            x = j * CELL_SIZE + INDENT
            y = i * CELL_SIZE + INDENT
            square =p.Rect(x,y,CELL_SIZE,CELL_SIZE)
            p.draw.rect(screen,color,square,width=CELL_SIZE)
            piece = gameState.board[i][j]
            if piece != "--":
                x = j * CELL_SIZE + INDENT
                y = i * CELL_SIZE + INDENT
                screen.blit(IMAGES[piece],(x,y))

def main():
    screen = p.display.set_mode((WIDTH+ 2* INDENT,HEIGHT + INDENT *2 ))
    clock = p.time.Clock()
    screen.fill(BG)
    gameState = GameState()
    # print(gameState.board)
    loadImages() # ONLY ONCEEEEEEE
    drawRanksAndFiles(screen)
    running = True
    lastSqSelected = () #(row,col)
    playerClicks = [] #(6,4) -> (4,4)
    while running:
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            if e.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos()
                
                col = (loc[0] - INDENT ) // CELL_SIZE
                row = (loc[1] - INDENT ) // CELL_SIZE
                if col>=0 and col < DIMENSION and row >=0 and row < DIMENSION:
                    if (row,col) == lastSqSelected:
                        lastSqSelected = ()
                        playerClicks = []
                    else:
                        lastSqSelected = (row,col)
                        playerClicks.append(lastSqSelected)
                    if len(playerClicks)==2:
                        # print(playerClicks)
                        move = GameMove(board=gameState.board,
                                        startSquare=playerClicks[0],
                                        endSquare=playerClicks[1])
                        gameState.makeMove(move)
                        print(move.toChessNotation())
                        lastSqSelected = ()
                        playerClicks = []
        drawGameState(screen, gameState)
        clock.tick(MAX_FPS)
        p.display.flip()
        
if __name__ == "__main__":
    main()