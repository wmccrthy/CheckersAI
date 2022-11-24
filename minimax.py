import pygame as pg 
import board as Board
from copy import deepcopy
RED = (250,0,0)
BLACK = (0,0,0)

# bug right now is in minimax; problem it is rarely returning a board state 
# that is multiple turns ahead of the passed in state i cant figure out what
# precise conditions are leading to bug as of now 


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
                score += 5
            else:
                score += 2
        for piece in board.getAllPieces(BLACK):
            if piece.king:
                score -= 5
            else:
                score -= 2
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
    start_x = piece.x
    start_y = piece.y
    prnt = str(piece.x) + "," + str(piece.y)
    if board.turn == piece.player:
        # if abs(move[0] - start_x) > 2 or abs(move[1] - start_y > 2):
        #     print("Move from: " + prnt + " to: " + str(move))
        board.move(board.board[start_x][start_y], move[0],move[1], board.getPiece(start_x,start_y))
        for pos in board.getDiagonals(start_x, start_y, move[0], move[1]):
            x = pos[0]
            y = pos[1]
            if board.board[x][y].checker != None:
                if board.board[x][y].checker.player == BLACK and piece.player == RED:
                    board.black_count -= 1
                if board.board[x][y].checker.player == RED and piece.player == BLACK:
                    board.red_count -= 1
                if board.getPiece(x,y).player != piece.player:
                    board.removePiece(x, y)
        board.turn = board.players.__next__()
    return board

def maxValue(board, depth, alpha, beta, transpo, other):
    if depth <= 0 or board.terminalTest():
        # print(board.evalFunction())
        return (board.evalFunction(), board)
    score = -99999
    move = board
    if board in transpo:
        return transpo[board]
    for new_board in getAllSuccessors(board, RED):
        # save time by returning states that that terminate game
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
    if board in transpo:
        return transpo[board]

    for new_board in getAllSuccessors(board, BLACK):
        # save time by returning states that end game 
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
    score = 0
    for new_board in getAllSuccessors(board, RED):
        score2, action2 = EminValue(new_board, depth-1)
        score += score2/len(getAllSuccessors(board,RED))
       
    return (score, None)

def expectiValue(board, depth):
    if depth <= 0 or board.terminalTest():
        # print(board.evalFunction())
        return (board.evalFunction(), board)
    score = 0
    for new_board in getAllSuccessors(board, BLACK):
        score2, action2 = EmaxValue(new_board, depth-1)
        score += score2/len(getAllSuccessors(board,BLACK))
       
    return (score, None)
    
def getAction(board,depth):
    score, move  = minValue(board, depth, -99999, 99999)
    return move


