# Driver File
# Handles User Input and display current game state

import pygame as p
from ChessEngine import *
p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
CELL_SIZE = HEIGHT// DIMENSION
MAX_FPS = 15
IMAGES = {}
GREY = (119, 132, 102)
WHITE =  (189, 196, 180)
BG = (60, 70, 50)
INDENT = 12

#should be called only once
def loadImages():
    pieces = ["bR", "bN", "bB", "bK", "bQ", "bB", "bB", "bN", "bR","bP",
              "wR", "wN", "wB", "wK", "wQ", "wB", "wB", "wN", "wR","wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"),(CELL_SIZE,CELL_SIZE))
        #now we can access the IMAGES dictionary
    
# GUI
def drawGameState(screen,gameState):
    drawBoardAndPieces(screen,gameState)       #draw cells & pieces

def drawBoardAndPieces(screen,gameState):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = WHITE if (i+j)%2==0 else GREY
            x = j * CELL_SIZE + INDENT
            y = i * CELL_SIZE + INDENT
            square =p.Rect(x,y,CELL_SIZE,CELL_SIZE)
            p.draw.rect(screen,color,square,width=CELL_SIZE)
            piece = gameState.board[i][j]
            if piece!="--":
                x = j * CELL_SIZE + INDENT
                y = i * CELL_SIZE + INDENT
                screen.blit(IMAGES[piece],(x,y))

def main():
    screen = p.display.set_mode((WIDTH+ 2* INDENT,HEIGHT + INDENT *2 ))
    clock = p.time.Clock()
    screen.fill(BG)
    gameState = GameState()
    print(gameState.board)
    loadImages() # ONLY ONCEEEEEEE
    drawGameState(screen, gameState)
    running = True
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        clock.tick(MAX_FPS)
        p.display.flip()
        
if __name__ == "__main__":
    main()