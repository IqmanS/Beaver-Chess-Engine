import random
# White Winning +ve Value
# Black Winning -ve Value
pieceScore  = {
    "K":0,
    "Q":10,
    "R":5,
    "B":3,
    "N":3,
    "P":1
}
CHECKMATE = 1000
STALEMATE = 0

def RandomAI(validMoves):
    return random.choice(validMoves)

def ScoreBoard(board):
    score = 0
    for row in board:
        for ele in row:
            if ele[0]=="w":
                score+= pieceScore[ele[1]]
            elif ele[0]=="b":
                score-= pieceScore[ele[1]]
    return score

def GreedyAI(gameState,validMoves):
    turnSign = 1 if gameState.whiteToMove else -1
    # IF AI = WHITE THEN 1, IF AI = BLACK THEN -1
    bestScore = - CHECKMATE #init the worst possible score
    bestMove = None
    
    for aiMove in validMoves:
        gameState.makeMove(aiMove)
        if gameState.checkmate:
            bestScore = turnSign * CHECKMATE
        elif gameState.stalemate:
            bestScore = STALEMATE
        score = turnSign * ScoreBoard(gameState.board)
        if (score > bestScore):
            bestScore = score
            bestMove = aiMove
        gameState.undoMove()
    return bestMove

def MinMaxAI(gameState,validMoves):
    turnSign = 1 if gameState.whiteToMove else -1
    MinMaxScore = CHECKMATE  # init the worst possible score
    bestAIMove = None
    random.shuffle(validMoves)
    for aiMove in validMoves:
        gameState.makeMove(aiMove)
        # FIND OPPONENTS MAX SCORE
        oppMoves = gameState.getValidMoves()
        oppMaxScore = -CHECKMATE
        for oppMove in oppMoves:
            gameState.makeMove(oppMove)
            if gameState.checkmate:
                score = -turnSign * CHECKMATE
            elif gameState.stalemate:
                score = STALEMATE
            else:
                score = -turnSign * ScoreBoard(gameState.board)
            if (score > oppMaxScore):
                oppMaxScore = score
            gameState.undoMove()
            
        # FIND YOUR MIN SCORE
        if oppMaxScore < MinMaxScore:
            MinMaxScore = oppMaxScore
            bestAIMove = aiMove
        gameState.undoMove()
    return bestAIMove
    