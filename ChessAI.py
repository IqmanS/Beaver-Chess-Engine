import random
# White Winning +ve Value
# Black Winning -ve Value
pieceScore  = {
    "K":0,
    "Q":9,
    "R":5,
    "B":3,
    "N":3,
    "P":1
}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def RandomAI(validMoves):
    return random.choice(validMoves)

def ScoreMaterial(board):
    score = 0
    for row in board:
        for ele in row:
            if ele[0]=="w":
                score+= pieceScore[ele[1]]
            elif ele[0]=="b":
                score-= pieceScore[ele[1]]
    return score

def ScoreBoard(gameState):
    if gameState.checkmate:
        if gameState.whiteToMove:
            return -CHECKMATE   #blackwins
        else:
            return CHECKMATE    #blackwins
    elif gameState.stalemate:
        return STALEMATE        #score 0
    score = 0
    for row in gameState.board:
        for ele in row:
            if ele[0] == "w":
                score += pieceScore[ele[1]]
            elif ele[0] == "b":
                score -= pieceScore[ele[1]]
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

def DepthTwoMinMaxAI(gameState,validMoves):
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
                score = CHECKMATE
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

def MinMaxAI(gameState,validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    RecursiveMinMax(gameState,validMoves,DEPTH,gameState.whiteToMove)
    return nextMove

def RecursiveMinMax(gameState,validMoves,depth,whiteToMove):
    global nextMove
    
    if depth == 0:
        return ScoreMaterial(gameState.board)
    if whiteToMove: #MAXIMIZER
        maxScore = -CHECKMATE
        for move in validMoves:
            gameState.makeMove(move)
            nextMoves = gameState.getValidMoves()
            score = RecursiveMinMax(gameState,nextMoves,depth-1,not whiteToMove)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gameState.undoMove()
        return maxScore
    else:           #MINIMIZER
        minScore = CHECKMATE
        for move in validMoves:
            gameState.makeMove(move)
            nextMoves = gameState.getValidMoves()
            score = RecursiveMinMax(gameState,nextMoves,depth-1,not whiteToMove)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gameState.undoMove()
        return minScore
        
def NegaMaxAI(gameState,validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    RecursiveNegaMax(gameState, validMoves, DEPTH, (1 if gameState.whiteToMove else -1))
    return nextMove

def RecursiveNegaMax(gameState,validMoves,depth,turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * ScoreBoard(gameState)
    maxScore = -CHECKMATE # init with worst possible value
    for move in validMoves:
        gameState.makeMove(move)
        nextMoves = gameState.getValidMoves()
        score = -1 *  RecursiveNegaMax(gameState, nextMoves, depth - 1,-1*turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gameState.undoMove()
    return maxScore

def AlphaBetaPruningAI(gameState,validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    RecursiveAlphaBetaPruning(gameState, validMoves,DEPTH,-CHECKMATE,CHECKMATE, (1 if gameState.whiteToMove else -1))
    return nextMove

def RecursiveAlphaBetaPruning(gameState,validMoves,depth,alpha,beta,turnMultiplier):
    #alpha is max rn and beta is min score rn
    global nextMove
    if depth == 0:
        return turnMultiplier * ScoreBoard(gameState)
    # order moves - implement later for better efficiency
    maxScore = -CHECKMATE # init with the worst possible value
    for move in validMoves:
        gameState.makeMove(move)
        nextMoves = gameState.getValidMoves()
        score = -1 *  RecursiveAlphaBetaPruning(gameState, nextMoves,
                                                depth=depth - 1,
                                                alpha=-beta,
                                                beta=-alpha,
                                                turnMultiplier=-1*turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gameState.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >=beta:
            break
    return maxScore