import numpy as np

class GameState():
    def __init__(self):
        # 8X8 2D MATRIX
        self.board = np.array([
            ["bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"], #empty
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"],
        ])
        self.whiteToMove = True
        self.moveLog = []
        
    def makeMove(self,gameMove):
        self.board[gameMove.startRow][gameMove.startCol] = "--"
        self.board[gameMove.endRow][gameMove.endCol] = gameMove.pieceMoved
        self.moveLog.append(gameMove.toChessNotation())
        
        #swap player turns
        self.whiteToMove = not self.whiteToMove
        
        
class GameMove():
    
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRank = {v:k for k,v in ranksToRows.items()}
    filesToCol = {"a":7,"b":6,"c":5,"d":4,"e":3,"f":2,"g":1,"h":0}
    colToFiles = {v: k for k, v in filesToCol.items()}
    
    def __init__(self,board,startSquare,endSquare):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.placeCaptured = board[self.endRow][self.endCol]
        
    def toChessNotation(self):
        rankFileStart = self.colToFiles[self.startCol] + self.rowsToRank[self.startRow]
        rankFileEnd = self.colToFiles[self.endCol] + self.rowsToRank[self.endRow]
        return str(rankFileStart+rankFileEnd)
    
