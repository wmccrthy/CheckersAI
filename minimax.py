import pygame as pg 
import board
from copy import deepcopy
RED = (250,0,0)
BLACK = (0,0,0)

def evalFunction(board): 
        score = 0
        # if self.black_count == 1:
        #     score -= self.black_count
        #     return score
        # if self.red_count == 1:
        #     score += self.red_count
        #     return score
    
        for piece in board.getAllPieces(RED):
            if piece.king:
                score += 2
            else:
                score += 1
        for piece in board.getAllPieces(BLACK):
            if piece.king:
                score -= 2
            else:
                score -= 1
        score += board.red_adv/(abs(board.red_count-board.black_count)+1)
        score -= board.black_adv/(abs(board.red_count-board.black_count)+1)

        return score
        

def getAllSuccessors(board, color):
    moves = []
    for piece in board.getAllPieces(color):
        validMoves = piece.getValidMoves(board.board)
        for move in validMoves:
            tempBoard = deepcopy(board)
            updatedPiece = tempBoard.getPiece(piece.x, piece.y)
            newBoard = getSuccessor(updatedPiece, move, tempBoard)
            moves.append(newBoard)
    moves.sort(key=evalFunction)

    return moves

def getSuccessor(piece, move, board):
    # simulates a move, to be used in get all moves 
    x = piece.x
    y = piece.y
    board.move(board.board[x][y], move[0],move[1], board.getPiece(x,y))
    for pos in board.getDiagonals(x,y, move[0], move[1]):
        x = pos[0]
        y = pos[1]
        if board.board[x][y].checker != None:
            if board.board[x][y].checker.player == BLACK:
                board.black_count -= 1
            if board.board[x][y].checker.player == RED:
                board.red_count -= 1
            board.removePiece(x, y)
   
    return board

def maxValue(board, depth, alpha, beta, transpo, other):
    if depth <= 0 or board.terminalTest():
        # print(board.evalFunction())
        return (board.evalFunction(), board)
    score = -99999
    move = board
    if transpo[board] != 0:
        return transpo[board]
    for new_board in getAllSuccessors(board, RED):
        if new_board.terminalTest():
            return (100, new_board)
        score2, action2 = minValue(new_board, depth-1, alpha, beta, other, transpo)
        if score2 > score:
            score, move = score2, action2
        if score2 == score:
            move = new_board
        if score > beta:
            transpo[board] = (score, move)
            return (score, move)
        alpha = max(alpha, score)
    transpo[board] = (score, move)
    return (score,move)



def minValue(board, depth, alpha, beta, transpo, other):
    if depth <= 0 or board.terminalTest():
        # print(board.evalFunction())
        return (board.evalFunction(), board)
    score = 99999
    move = board
    
    # perform transposition check
    if transpo[board] != 0:
        return transpo[board]

    for new_board in getAllSuccessors(board, BLACK):
        if new_board.terminalTest():
            return (-100, new_board)
        score2, action2 = maxValue(new_board, depth-1, alpha, beta, other, transpo)
        if score2 < score:
            score, move = score2, action2
        if score2 == score:
            move = new_board
        if score < alpha:
            transpo[board] = (score, move)
            return (score, move)
        beta = min(beta, score)

    transpo[board] = (score, move)  
    return (score,move)


def EmaxValue(board, depth):
    if depth <= 0 or board.terminalTest():
        # print(board.evalFunction())
        return (board.evalFunction(), board)
    score = -99999
    for new_board in getAllSuccessors(board, RED):
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
    move = None
    for new_board in getAllSuccessors(board, BLACK):
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
    score = 99999
    for new_board in getAllSuccessors(board, RED):
        score2, action2 = EmaxValue(new_board, depth-1)
        score += score2/len(getAllSuccessors(board,RED))
       
    return (score, None)
def expectiValue(board, depth):
    if depth <= 0 or board.terminalTest():
        # print(board.evalFunction())
        return (board.evalFunction(), board)
    score = 99999
    for new_board in getAllSuccessors(board, BLACK):
        score2, action2 = EmaxValue(new_board, depth-1)
        score += score2/len(getAllSuccessors(board,BLACK))
       
    return (score, None)
    
def getAction(board,depth):
    score, move  = minValue(board, depth, -99999, 99999)
    return move


