import pygame as pg 
import board as Board
from copy import deepcopy
import random
import transposition
RED = (250,0,0)
BLACK = (0,0,0)

# bug right now is in minimax; problem it is rarely returning a board state 
# that is multiple turns ahead of the passed in state i cant figure out what
# precise conditions are leading to bug as of now 


def evalFunction(self): 
        score = 0
   
        if self.num_plys == 0:
            score = random.randint(-12, 12)
            return score 

        # increase score according to factors of red player (maximizing player):
        score += 5*self.red_pawns
        score += 7.75 * self.red_kings
        score += 4 * self.red_back
        score += 2.5 * self.red_mid
        score += 0.5 * self.red_outsidemid
        score += 3 * self.black_vuln

        # decrease score according to factors of black player (minimizing player):
        score -= 5*self.black_pawns
        score -= 7.75 * self.black_kings
        score -= 4 * self.black_back
        score -= 2.5 * self.black_mid
        score -= 0.5 * self.black_outsidemid

        score -= 3 * self.red_vuln

        return score  

def getAllSuccessors(board, color, maximize):
    moves = []
    for piece in board.getAllPieces(color):
        validMoves = piece.getValidMoves(board.board)
        for move in validMoves:
            tempBoard = deepcopy(board)
            updatedPiece = tempBoard.getPiece(piece.x, piece.y)
            newBoard = getSuccessor(updatedPiece, move, tempBoard, board)
            moves.append(newBoard)

    # after checking/retrieving all possible successor board states and 
    # finding the minimum num of the other color possible at successor state,
    # update the vulnerable count accordingly  
    # print("Red Vuln Check: " + str(board.red_vuln))

    if maximize:
        moves.sort(key=evalFunction, reverse = True)
    else:
        moves.sort(key=evalFunction)

    return moves

def getSuccessor(piece, move, board, old=None):
    # simulates a move, to be used in get all moves 
    start_x = piece.x
    start_y = piece.y

    redV = 0
    blackV = 0
    
    if board.turn == piece.player:
        board.move(board.board[start_x][start_y], move[0],move[1], board.getPiece(start_x,start_y))
        for pos in board.getDiagonals(start_x, start_y, move[0], move[1]):
            x = pos[0]
            y = pos[1]
            if board.board[x][y].checker != None:
                if board.board[x][y].checker.player == BLACK and piece.player == RED:
                    board.black_count -= 1
                    # blackV += 1
                if board.board[x][y].checker.player == RED and piece.player == BLACK:
                    board.red_count -= 1
                    # redV += 1
                if board.getPiece(x,y).player != piece.player:
                    board.removePiece(x, y)

        board.resetCount()
        board.updateKingCount()
        
        # if old != None:
        #     old.red_vuln = redV
        #     old.black_vuln = blackV
        
        # make sure board updates scored factors when returning successor 

        board.turn = board.players.__next__()
    return board

def maxValue(board, depth, alpha, beta, transpo, other):
    if depth <= 0 or board.terminalTest():
        # print(board.evalFunction())
        return (board.evalFunction(), board)
    score = -99999
    move = board

    zobrist = transposition.zobristKey(board.board)
    transpoInd = transposition.hashZobrist(zobrist, transpo)
    
    potentialReturn = transposition.transpoCheck(board.board, transpo)
    if potentialReturn != None:
        return potentialReturn
        
    for new_board in getAllSuccessors(board, RED, True):
        # save time by returning states that that terminate game
        if new_board.terminalTest():
            return (100, new_board)
        score2, action2 = minValue(new_board, depth-1, alpha, beta, other, transpo)
        if score2 > score:
            score, move = score2, action2
        if score2 == score:
            move = new_board
        if score > beta:
            transpo[transpoInd] = (zobrist, score, move)
            return (score, move)
        alpha = max(alpha, score)

    transpo[transpoInd] = (zobrist, score, move)

    return (score,move)



def minValue(board, depth, alpha, beta, transpo, other):
    if depth <= 0 or board.terminalTest():
        # print(board.evalFunction())
        return (board.evalFunction(), board)
    score = 99999
    move = board
    
    zobrist = transposition.zobristKey(board.board)
    transpoInd = transposition.hashZobrist(zobrist, transpo)
    
    potentialReturn = transposition.transpoCheck(board.board, transpo)
    if potentialReturn != None:
        return potentialReturn

    for new_board in getAllSuccessors(board, BLACK, False):
        # save time by returning states that end game 
        if new_board.terminalTest():
            return (-100, new_board)
        score2, action2 = maxValue(new_board, depth-1, alpha, beta, other, transpo)
        if score2 < score:
            score, move = score2, action2
        if score2 == score:
            move = new_board
        if score < alpha:
            transpo[transpoInd] = (zobrist, score, move)
            return (score, move)
        beta = min(beta, score)

    transpo[transpoInd] = (zobrist, score, move) 
    return (score,move)


def EmaxValue(board, depth):
    if depth <= 0 or board.terminalTest():
        # print(board.evalFunction())
        return (board.evalFunction(), board)
    score = -99999
    for new_board in getAllSuccessors(board, RED, True):
        score2, action2 = expectiValue(new_board, depth-1)
        if score2 > score:
            score, move = score2, action2
        if score2 == score:
            move = new_board
     
    return (score,move) 

def EminValue(board, depth):
    if depth <= 0 or board.terminalTest():
        # print(board.evalFunction())
        return (board.evalFunction(), board)
    score = 99999
    for new_board in getAllSuccessors(board, BLACK, False):
        score2, action2 = min_expectiValue(new_board, depth-1)
        if score2 < score:
            score, move = score2, action2
        if score2 == score:
            move = new_board
     
    return (score,move) 

 
def min_expectiValue(board, depth):
    if depth <= 0 or board.terminalTest():
        # print(board.evalFunction())
        return (board.evalFunction(), board)
    score = 0
    for new_board in getAllSuccessors(board, RED, False):
        score2, action2 = EminValue(new_board, depth-1)
        score += score2/len(getAllSuccessors(board,RED, False))
       
    return (score, None)

def expectiValue(board, depth):
    if depth <= 0 or board.terminalTest():
        # print(board.evalFunction())
        return (board.evalFunction(), board)
    score = 0
    for new_board in getAllSuccessors(board, BLACK, True):
        score2, action2 = EmaxValue(new_board, depth-1)
        score += score2/len(getAllSuccessors(board,BLACK, True))
       
    return (score, None)
    
def getAction(board,depth):
    score, move  = minValue(board, depth, -99999, 99999)
    return move


