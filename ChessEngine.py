import numpy as np

class GameState():
    def __init__(self):
        # 8X8 2D MATRIX
        self.board = np.array([
            ["bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"], #empty
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "wN", "--", "--", "--", "--"],
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
        moves = []
        for i in range(len(self.board)): #rows
            for j in range(len(self.board[0])): #cols
                pieceColor = self.board[i][j][0]
                if(self.whiteToMove and pieceColor == "w") or (not self.whiteToMove and pieceColor == "b"):
                    piece = self.board[i][j][1]
                    if piece == 'P':
                        self.getPawnMoves(i, j, moves)
                    elif piece == 'R':
                        self.getRookMoves(i, j, moves)
                        print(moves)
                    elif piece == 'N':
                        self.getKnightMoves(i, j ,moves)
                    elif piece == 'B':
                        self.getBishopMoves(i ,j ,moves)
                    elif piece == 'K':
                        self.getKingMoves(i, j, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(i, j, moves)
        return moves

    def getPawnMoves(self,row,col,moves):
        #WHITE - start on row 6
        if self.whiteToMove:
            # 1 square upward
            if self.board[row - 1][col]== "--":
                oneUp = GameMove(self.board,(row,col),(row - 1,col))
                moves.append(oneUp)
            # 2 square upward if on row 6
            if row == 6 and self.board[row - 1][col] == "--" and self.board[row - 2][col] == "--":
                twoUp = GameMove(self.board, (row, col), (row - 2, col))
                moves.append(twoUp)
            # Diagonal take
            if col-1>=0 and self.board[row - 1][col - 1][0] == "b":
                diagUpLeft = GameMove(self.board, (row, col), (row - 1, col - 1))
                moves.append(diagUpLeft)
            if col+1<=7 and self.board[row - 1][col + 1][0] == "b":
                diagUpRight = GameMove(self.board, (row, col), (row - 1, col + 1))
                moves.append(diagUpRight)
            
        #BLACK - start on row 1
        if not self.whiteToMove:
            # 1 square downward
            if ( self.board[row+1][col]=="--"):
                oneDown = GameMove(self.board,(row,col),(row + 1,col))
                moves.append(oneDown)
            # 2 square downward if on row 1
            if ( row == 1 and self.board[row + 1][col] == "--" and self.board[row + 2][col] == "--"):
                twoDown = GameMove(self.board, (row, col), (row + 2, col))
                moves.append(twoDown)
            # Diagonal take
            if col-1>=0 and self.board[row + 1][col - 1][0]== "w":
                diagUpLeft = GameMove(self.board, (row, col), (row + 1, col - 1))
                moves.append(diagUpLeft)
            if col+1<=7 and self.board[row + 1][col + 1][0] == "w":
                diagUpRight = GameMove(self.board, (row, col), (row + 1, col + 1))
                moves.append(diagUpRight)
        
    
    def getRookMoves(self,row,col,moves):
        target = "b" if self.whiteToMove else "w"
        #DOWN
        for i in range(row+1,8):
            if self.board[i][col] == "--":
                rookDown = GameMove(self.board,(row,col),(i,col))
                moves.append(rookDown)
            elif self.board[i][col][0] == target:
                rookDown = GameMove(self.board,(row,col),(i,col))
                moves.append(rookDown)
                break
            else:
                break
        #UP
        for i in range(row-1,-1,-1):
            if self.board[i][col] == "--":
                rookUp = GameMove(self.board,(row,col),(i,col))
                moves.append(rookUp)
            elif self.board[i][col][0] == target:
                rookUp = GameMove(self.board,(row,col),(i,col))
                moves.append(rookUp)
                break
            else:
                break
        #LEFT
        for i in range(col-1,-1,-1):
            if self.board[row][i] == "--":
                rookLeft = GameMove(self.board,(row,col),(row,i))
                moves.append(rookLeft)
            elif self.board[row][i][0] == target:
                rookLeft = GameMove(self.board,(row,col),(row,i))
                moves.append(rookLeft)
                break
            else:
                break
        #RIGHT
        for i in range(col+1,8):
            if self.board[row][i] == "--":
                rookRight = GameMove(self.board,(row,col),(row,i))
                moves.append(rookRight)
            elif self.board[row][i][0] == target:
                rookRight = GameMove(self.board,(row,col),(row,i))
                moves.append(rookRight)
                break
            else:
                break
 
    def getKnightMoves(self,row,col,moves):
        me = "b" if self.whiteToMove else "w"
        # case 1 : self.board[row + 1][ col + 2]
        if row + 1<=7 and col +2<=7 and self.board[row + 1][col + 2] != me:
            knightCase1 = GameMove(self.board,(row,col),(row + 1,col + 2))
            moves.append(knightCase1)
        # case 2 : self.board[row + 1][col - 2]
        if row + 1<=7 and col -2>=0 and self.board[row + 1][col - 2] !=me:
            knightCase2 = GameMove(self.board,(row,col),(row + 1,col - 2))
            moves.append(knightCase2)
        # case 3 : self.board[row - 1][col + 2]
        if row - 1>=0 and col +2<=7 and self.board[row - 1][col + 2] !=me:
            knightCase3 = GameMove(self.board,(row,col),(row - 1,col + 2))
            moves.append(knightCase3)
        # case 4 : self.board[row - 1][col - 2]
        if row - 1>=0 and col -2>=0 and self.board[row - 1][col - 2] !=me:
            knightCase4 = GameMove(self.board,(row,col),(row - 1,col - 2))
            moves.append(knightCase4)
        # case 5 : self.board[row + 2][col + 1]
        if row + 2<=7 and col +1<=7 and self.board[row + 2][col + 1] !=me:
            knightCase5 = GameMove(self.board,(row,col),(row + 2,col + 1))
            moves.append(knightCase5)
        # case 6 : self.board[row + 2][col - 1]
        if row + 2<=7 and col -1>=0 and self.board[row + 2][col - 1] !=me:
            knightCase6 = GameMove(self.board,(row,col),(row + 2,col - 1))
            moves.append(knightCase6)
        # case 7 : self.board[row - 2][col + 1]
        if row -2 >=0 and col +1<=7  and self.board[row - 2][col + 1] !=me:
            knightCase7 = GameMove(self.board,(row,col),(row - 2,col + 1))
            moves.append(knightCase7)
        # case 8 : self.board[row - 2][col - 1]
        if row -2 >=0 and col -1>=0 and self.board[row - 2][col - 1] !=me:
            knightCase8 = GameMove(self.board,(row,col),(row - 2,col - 1))
            moves.append(knightCase8)
    
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
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        # print(self.moveID)
        
    def toChessNotation(self):
        rankFileStart = self.colToFiles[self.startCol] + self.rowsToRank[self.startRow]
        rankFileEnd = self.colToFiles[self.endCol] + self.rowsToRank[self.endRow]
        return str(rankFileStart+rankFileEnd)
    
    #OPERATOR OVERLOADING "="
    def __eq__(self,other):
        if isinstance(other,GameMove): #if other is an instance of GameMove Class
            return ((self.moveID == other.moveID))
        return False
