# Driver File
# Handles User Input and display current game state

import pygame as p
import numpy as np
from ChessEngine import *
from ChessAI import *

p.init()
p.display.set_caption('Beaver')
FONT = p.font.Font('freesansbold.ttf', 10)
HEADING = p.font.Font('freesansbold.ttf', 32)
GAMEEND = p.font.Font('freesansbold.ttf', 40)
WIDTH = HEIGHT = 512
DIMENSION = 8
CELL_SIZE = HEIGHT// DIMENSION
MAX_FPS = 15
IMAGES = {}
GREY = (119, 132, 102)
DARKGREY = (37, 44, 28)
HEADINGCOL = (209, 216, 200)
WHITE =  (189, 196, 180)
BG = (60, 70, 50)
INDENT = 18
HIGHLIGHT1 = (101, 88, 60)
HIGHLIGHT2 = (251, 225, 132)
HumanVsHuman = False
HumanVsComputer = True
ComputerVsComputer = False

#should be called only once
def loadImages():
    pieces = np.array(["bR", "bN", "bB", "bK", "bQ", "bB", "bB", "bN", "bR","bP",
              "wR", "wN", "wB", "wK", "wQ", "wB", "wB", "wN", "wR","wP"])
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"),(CELL_SIZE,CELL_SIZE))
        #now we can access the IMAGES dictionary
    
# GUI
def drawGameState(screen,gameState,validMoves,sqSelected):
    drawBoardAndPieces(screen,gameState)       #draw cells & pieces
    highlightCells(screen, gameState, validMoves, sqSelected)

def drawRanksAndFiles(screen):
    title = "BEAVER CHESS ENGINE"
    titleBox = HEADING.render(title,True,HEADINGCOL)
    titleBox.get_width()
    screen.blit(titleBox, (WIDTH *1.15+ (2*INDENT), CELL_SIZE ))
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
                
def highlightCells(screen,gameState,validMoves,sqSelected): #Highlights the moves
    if sqSelected !=():
        row,col = sqSelected
        me = "w" if gameState.whiteToMove else "b"
        if gameState.board[row][col][0] == me:
            #highlight selected square
            sq = p.Surface((CELL_SIZE,CELL_SIZE))
            sq.set_alpha(50)
            sq.fill(HIGHLIGHT1)
            x = col * CELL_SIZE + INDENT
            y = row * CELL_SIZE + INDENT
            screen.blit(sq,(x,y))
            # Highlight moves
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    sq.set_alpha(120)
                    sq.fill(HIGHLIGHT2)
                    x = move.endCol * CELL_SIZE + INDENT
                    y = move.endRow * CELL_SIZE + INDENT
                    screen.blit(sq, (x, y))
                    
def drawText(screen,text):
    textBox = GAMEEND.render(text,True,DARKGREY)
    textLoc = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textBox.get_width()/2,HEIGHT/2 - textBox.get_height()/2)
    screen.blit(textBox,textLoc)
    
def drawScoreMeter(screen,score):
    p.draw.rect(screen, DARKGREY, p.Rect(WIDTH + 2 * INDENT, INDENT *2 , 46, HEIGHT - 2*INDENT))
    if score > 0:
        score = min(score, 35)
        p.draw.rect(screen, WHITE, p.Rect(WIDTH + 2 * INDENT +3, (HEIGHT + INDENT * 2)//2, 40, (HEIGHT - 2 * INDENT)*score/35))
    else:
        score = max(score, -20)
        p.draw.rect(screen, GREY,p.Rect(WIDTH + 2 * INDENT +3, ((HEIGHT + INDENT * 2)// 2)-(HEIGHT - 2 * INDENT) * -score / 35 , 40, (HEIGHT - 2 * INDENT) * -score / 35))

def main():
    screen = p.display.set_mode((WIDTH*2+ 2* INDENT,HEIGHT + INDENT *2 ))
    clock = p.time.Clock()
    screen.fill(BG)
    gameState = GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False
    loadImages() # ONLY ONCE
    drawRanksAndFiles(screen)
    running = True
    lastSqSelected = () #(row,col)
    playerClicks = [] #(6,4) -> (4,4)
    gameOver = False
    while running:
        # humanTurn = gameState.whiteToMove if HumanVsComputer else False
        humanTurn = False if ComputerVsComputer else gameState.whiteToMove if HumanVsComputer else False
            
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
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
                            move = GameMove(board=gameState.board,
                                            startSquare=playerClicks[0],
                                            endSquare=playerClicks[1])
                            if move in validMoves:
                                print(move.pieceMoved + move.toChessNotation())
                                gameState.makeMove(move)
                                moveMade = True
                                lastSqSelected = ()
                                playerClicks = []
                            else:
                                playerClicks = [lastSqSelected]
                        
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gameState.undoMove()
                    moveMade = True
                    gameOver = False
                    
                elif e.key == p.K_r:
                    gameState = GameState()
                    validMoves = gameState.getValidMoves()
                    lastSqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False
                    
        #AI MOVES
        if not gameOver and not humanTurn:
            AIMove = AlphaBetaPruningAI(gameState,validMoves)
            if AIMove is None:
                AIMove = RandomAI(validMoves)
            gameState.makeMove(AIMove)
            moveMade = True
        
        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False
                    
        drawGameState(screen, gameState,validMoves,sqSelected=lastSqSelected)
        score = ScoreBoard(gameState)
        if score >= 0:
            drawScoreMeter(screen,min(17.2,score))
        else:
            drawScoreMeter(screen, max(-17.2, score))
        # drawScoreMeter(screen,ScoreBoard(gameState))
        
        if gameState.checkmate:
            gameOver = True
            if gameState.whiteToMove:
                text = "BLACK WON"
                drawText(screen,text)
            else:
                text = "WHITE WON"
                drawText(screen,text)
        elif gameState.stalemate:
            gameOver = True
            text = "STALEMATE"
            drawText(screen,text)
            
            
        clock.tick(MAX_FPS)
        p.display.flip()
        
if __name__ == "__main__":
    main()