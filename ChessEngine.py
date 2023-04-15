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
        
    def makeMove(self,gameMove): # Not works for castling, en passant and pawn promotion
        self.board[gameMove.startRow][gameMove.startCol] = "--"
        self.board[gameMove.endRow][gameMove.endCol] = gameMove.pieceMoved
        self.moveLog.append(gameMove)
        #swap player turns
        self.whiteToMove = not self.whiteToMove
        
    def undoMove(self):
        if len(self.moveLog)!=0:
            lastMove = self.moveLog.pop()
            self.board[lastMove.startRow][lastMove.startCol] = lastMove.pieceMoved
            self.board[lastMove.endRow][lastMove.endCol] = lastMove.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            
    def getValidMoves(self): #All moves without checks subset of POSSIBLE MOVES
        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves(self): #All moves with checks
        moves = np.array([])
        np.append(moves,[])
        for i in range(len(self.board)): #rows
            for j in range(len(self.board[0])): #cols
                pieceColor = self.board[i][j][0]
                if(self.whiteToMove and pieceColor == "w") or (not self.whiteToMove and pieceColor == "b"):
                    piece = self.board[i][j][1]
                    if piece == 'P':
                        self.getPawnMoves(i,j,moves)
                    elif piece == 'R':
                        self.getRookMoves(i,j,moves)
                    elif piece == 'N':
                        self.getKnightMoves(i,j,moves)
                    elif piece == 'B':
                        self.getBishopMoves(i,j,moves)
                    elif piece == 'K':
                        self.getKingMoves(i, j, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(i, j, moves)

    def getPawnMoves(self,row,col,moves):
        pass
    
    def getRookMoves(self,row,col,moves):
        pass
    
    def getKnightMoves(self,row,col,moves):
        pass
    
    def getBishopMoves(self,row,col,moves):
        pass
    
    def getKingMoves(self,row,col,moves):
        pass
    
    def getQueenMoves(self,row,col,moves):
        pass
            
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
        self.pieceCaptured = board[self.endRow][self.endCol]
        
    def toChessNotation(self):
        rankFileStart = self.colToFiles[self.startCol] + self.rowsToRank[self.startRow]
        rankFileEnd = self.colToFiles[self.endCol] + self.rowsToRank[self.endRow]
        return str(rankFileStart+rankFileEnd)
    
