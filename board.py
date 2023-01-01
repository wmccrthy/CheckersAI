import pygame as pg
import random
import sys
from itertools import cycle


pg.init()
clock = pg.time.Clock()
window_width = 800
window_height = 800
window = pg.display.set_mode((window_width, window_height))
cell_width = window_width/8
cell_height = window_height/8
# colors
BLACK = (0,0,0)
RED = (250,0,0)

font = pg.font.SysFont('chalkboardse', 20)
bigFont = pg.font.SysFont('chalkboardse', 40)



# 
class Cell:
    def __init__(self, c, r):
        self.x = c
        self.y = r

        self.checker = None
        # single item list used to store whatever (if any) checker is in the cell
 
    def placePiece(self, piece):
        self.checker = CheckerPiece(self.x, self.y, piece.player, piece.king)
    def removePiece(self):
        self.checker = None
    # methods for placing and removing piece from cell; 
    # going to modify cell draw method such that it draws circle of piece, if there is one to draw
    

    def withinRange(self, coord):
        if self.checker != None:
            if abs(self.checker.x - coord[0]) < 1  and abs(self.checker.y - coord[1]) < 1:
                # self.prior_x = self.x
                # self.prior_y = self.y 
                return True
        return False

    
    def draw(self, window):
        x = pg.mouse.get_pos()[0]
        y = pg.mouse.get_pos()[1]
        c = int (x / cell_width)
        r = int (y / cell_height)

        # highlights piece cell  being hovered over 
        if self.withinRange((c,r)):
            pg.draw.rect(window, (250, 250, 250), (self.x * cell_width, self.y * cell_height, cell_width-2, cell_height-2))
        else:
            # implement logic to draw alternating colors 
            if self.y%2 == 0:
                if self.x%2== 0:
                    pg.draw.rect(window, (0,0,0), (self.x * cell_width, self.y * cell_height, cell_width-2, cell_height-2))
                else:
                    pg.draw.rect(window,(239,159,95), (self.x * cell_width, self.y * cell_height, cell_width-2, cell_height-2))
            else:
                if self.x%2== 0:
                    pg.draw.rect(window,(239,159,95), (self.x * cell_width, self.y * cell_height, cell_width-2, cell_height-2))
                else:
                    pg.draw.rect(window, (0,0,0), (self.x * cell_width, self.y * cell_height, cell_width-2, cell_height-2))
        if self.checker != None:
            if self.checker.king:
                pg.draw.circle(window, self.checker.player, (self.checker.x * cell_width + cell_width/2, self.checker.y * cell_height + cell_height/2), (cell_width/3))
                pg.draw.circle(window, (250,250,250), (self.checker.x * cell_width + cell_width/2, self.checker.y * cell_height + cell_height/2), (cell_width/9))
            else:
                if self.checker.player == RED:
                    pg.draw.circle(window, (0,0,0), (self.checker.x * cell_width + cell_width/2, self.checker.y * cell_height + cell_height/2), (cell_width/3)+1)
                else:
                     pg.draw.circle(window, (200,200,200), (self.checker.x * cell_width + cell_width/2, self.checker.y * cell_height + cell_height/2), (cell_width/3)+1)
                pg.draw.circle(window, self.checker.player, (self.checker.x * cell_width + cell_width/2, self.checker.y * cell_height + cell_height/2), (cell_width/3))
                

    def drawMoves(self, window, board):
        if self.checker != None:
            moves = self.checker.getValidMoves(board)
            # moves = self.checker.getValidMovesOPT(board)
            for move in moves:
                if self.checker.player == BLACK:
                    # pg.draw.circle(window, (0, 0, 0), (move[0] * cell_width + cell_width/2, move[1] * cell_height + cell_height/2), cell_height/9+.5)
                    pg.draw.circle(window, (250, 250, 250), (move[0] * cell_width + cell_width/2, move[1] * cell_height + cell_height/2), cell_height/9)
       
                else:
                    # pg.draw.circle(window, (0, 0, 0), (move[0] * cell_width + cell_width/2, move[1] * cell_height + cell_height/2), cell_height/9+.5)
                    pg.draw.circle(window, (250, 250, 250), (move[0] * cell_width + cell_width/2, move[1] * cell_height + cell_height/2), cell_height/9)
        # highlight cells that can be moved into 

           
        # also highlight the cell currently selected 
        if self.checker != None:
            pg.draw.rect(window, (220, 220, 220), (self.x * cell_width, self.y * cell_height, cell_width-2, cell_height-2))
            pg.draw.circle(window, self.checker.player, (self.checker.x * cell_width + cell_width/2, self.checker.y * cell_height + cell_height/2), (cell_width/2.6))
            if self.checker.king:
                pg.draw.circle(window, (250,250,250), (self.checker.x * cell_width + cell_width/2, self.checker.y * cell_height + cell_height/2), (cell_width/9.3))
        

class CheckerPiece:
    def __init__(self, c, r, color, kingStatus=False):
        self.x = c
        self.y = r

        self.player = color
        self.king = kingStatus


    def getValidMoves(self, board):
        moves = []
        skipped = []
        # to store pairs of moves that capture pieces w pieces captured such that if move is selected, we remove relevant 

        # moves appended in (x, y) coordinate tuples 
        # piece.getValidMoves returns list of all possible coordinates to which a piece can go
       
        leftrng = min(3, abs(self.x-0)+1)
        rightrng = min(3, abs(self.x-7)+1)
        if self.king:
                for i in range(1,rightrng):
                # check for own color in diags
                    if self.y - i >= 0:
                        if self.x+i <8:
                            if board[self.x+i][self.y-i].checker != None:
                                if board[self.x+i][self.y-i].checker.player == self.player:
                                    break
                            if board[self.x+i][self.y-i].checker == None:
                                # if i == 2; meaning this move is a jump, check if can double jump
                                if i == 2 and 0 <= self.x+i+2 < 8 and 0<= self.y-i+2 < 8:
                                    if board[self.x+i+1][self.y-i-1].checker != None and board[self.x+i+1][self.y-i-1].checker.player  != self.player and board[self.x+i+2][self.y-i-2].checker == None:
                                        moves.append((self.x+i+2, self.y-i-2))
                                moves.append((self.x+i,self.y-i))
                            
                                break
               
                for i in range(1, leftrng):
                    if self.y - i >= 0:
                        if self.x - i >= 0:
                            if board[self.x-i][self.y-i].checker != None:
                                if board[self.x-i][self.y-i].checker.player == self.player:
                                    break
                            if board[self.x-i][self.y-i].checker == None:
                                if i == 2 and 0 <= self.x-i+2 < 8 and 0<= self.y-i+2 < 8:
                                    if board[self.x-i-1][self.y-i-1].checker != None and board[self.x-i-1][self.y-i-1].checker.player  != self.player and board[self.x-i-2][self.y-i-2].checker == None:
                                        moves.append((self.x-i-2, self.y-i-2))
                                moves.append((self.x-i, self.y-i))
                                break
                
                for i in range(1,rightrng):
                # check for own color in diags
                # print(self.x+i, self.y+i)
                    if self.y + i < 8:
                        if self.x + i < 8: 
                            if board[self.x+i][self.y+i].checker != None:
                                if board[self.x+i][self.y+i].checker.player == self.player:
                                    break
                            if board[self.x+i][self.y+i].checker == None:
                                if i == 2 and 0 <= self.x+i+2 < 8 and 0<= self.y+i+2 < 8:
                                    if board[self.x+i+1][self.y+i+1].checker != None and board[self.x+i+1][self.y+i+1].checker.player  != self.player and board[self.x+i+2][self.y+i+2].checker == None:
                                        moves.append((self.x+i+2, self.y+i+2))
                                moves.append((self.x+i,self.y+i))
                                break
                for i in range(1, leftrng):
                    if self.y + i < 8:
                        if self.x -i >= 0:
                            if board[self.x-i][self.y+i].checker != None:
                                if board[self.x-i][self.y+i].checker.player == self.player:
                                    break
                            if board[self.x-i][self.y+i].checker == None:
                                if i == 2 and 0 <= self.x-i+2 < 8 and 0<= self.y+i+2 < 8:
                                    if board[self.x-i-1][self.y+i+1].checker != None and board[self.x-i-1][self.y+i+1].checker.player  != self.player and board[self.x-i-2][self.y+i+2].checker == None:
                                        moves.append((self.x-i-2, self.y+i+2))
                                moves.append((self.x-i, self.y+i))
                                break
            


        if self.player == RED:
            for i in range(1,rightrng):
                # check for own color in diags
                if self.y - i >= 0:
                    if self.x + i < 8:  
                        if board[self.x+i][self.y-i].checker != None:
                            if board[self.x+i][self.y-i].checker.player == RED:
                                break
                        if board[self.x+i][self.y-i].checker == None:
                            # if i == 2; meaning this move is a jump, check if can double jump
                            if i == 2 and 0 <= self.x+i+2 < 8 and 0<= self.y-i+2 < 8:
                                if board[self.x+i+1][self.y-i-1].checker != None and board[self.x+i+1][self.y-i-1].checker.player  == BLACK and board[self.x+i+2][self.y-i-2].checker == None:
                                    moves.append((self.x+i+2, self.y-i-2))
                            moves.append((self.x+i,self.y-i))
                        
                            break
               
            for i in range(1, leftrng):
                if self.y - i >= 0:
                    if self.x - i >= 0:
                        if board[self.x-i][self.y-i].checker != None:
                            if board[self.x-i][self.y-i].checker.player == RED:
                                break
                        if board[self.x-i][self.y-i].checker == None:
                            if i == 2 and 0 <= self.x-i+2 < 8 and 0<= self.y-i+2 < 8:
                                if board[self.x-i-1][self.y-i-1].checker != None and board[self.x-i-1][self.y-i-1].checker.player  == BLACK and board[self.x-i-2][self.y-i-2].checker == None:
                                    moves.append((self.x-i-2, self.y-i-2))
                            moves.append((self.x-i, self.y-i))
                            break

        if self.player == BLACK:
            
            for i in range(1,rightrng):

                # check for own color in diags
                # print(self.x+i, self.y+i)
                if self.y + i < 8:
                    if self.x+i < 8:
                        if board[self.x+i][self.y+i].checker != None:
                            if board[self.x+i][self.y+i].checker.player == BLACK:
                                break
                        if board[self.x+i][self.y+i].checker == None:
                            if i == 2 and 0 <= self.x+i+2 < 8 and 0<= self.y+i+2 < 8:
                                if board[self.x+i+1][self.y+i+1].checker != None and board[self.x+i+1][self.y+i+1].checker.player  == RED and board[self.x+i+2][self.y+i+2].checker == None:
                                    moves.append((self.x+i+2, self.y+i+2))
                            moves.append((self.x+i,self.y+i))
                            break
            for i in range(1, leftrng):
                if self.y + i < 8:
                    if self.x - i >= 0:
                        if board[self.x-i][self.y+i].checker != None:
                            if board[self.x-i][self.y+i].checker.player == BLACK:
                                break
                        if board[self.x-i][self.y+i].checker == None:
                            if i == 2 and 0 <= self.x-i+2 < 8 and 0<= self.y+i+2 < 8:
                                if board[self.x-i-1][self.y+i+1].checker != None and board[self.x-i-1][self.y+i+1].checker.player  == RED and board[self.x-i-2][self.y+i+2].checker == None:
                                    moves.append((self.x-i-2, self.y+i+2))
                            moves.append((self.x-i, self.y+i))
                            break
            
                    # have handled x being out of range, need to handle y out of range 
                    # also need to handle king, but he can b separate case and apply to both colors 

        for move in moves:
            if move[0] < 0 or move[1] < 0:
                moves.remove(move)
            
        return moves  
    

    

# make board have array of pieces 

class Board:
    def __init__(self):
        self.board = []
        # the 2d list that represents the game board 
        # board stores rows, which store the columns 
        for col in range(8):
            curRow = []
            for row in range(8):
                curCell = Cell(col, row)
                if row == 0 or row == 2:
                    if col % 2 != 0:
                        curCell.checker = CheckerPiece(col, row, BLACK)
                if row == 1:
                    if col % 2 == 0:
                        curCell.checker = CheckerPiece(col, row, BLACK)
                if row == 5 or row == 7:
                    if col % 2 == 0:
                        curCell.checker = CheckerPiece(col, row, RED)
                if row == 6:
                    if col % 2 != 0:
                        curCell.checker = CheckerPiece(col, row, RED)
                curRow.append(curCell)
            self.board.append(curRow)
        
        self.black_count = self.red_count =  12
        self.black_pawns = self.red_pawns = 0
        self.black_kings = self.red_kings = 0
        self.red_back = self.black_back = 0
        self.red_mid = self.black_mid = 0
        self.red_outsidemid = self.black_outsidemid = 0
        self.red_vuln = self.black_vuln = 0

        # need to figure out way to keep track of vulnerable pieces 
        # use getAllSuccessors function; loop through successors, number of vulnerable pieces of color
        # should be equal to the ddifference between self.red/black_count and the successor w the smallest
        # count of same color


        # self.black_adv = self.red_adv = 0
        
        self.num_plys = 0

        self.players = cycle([RED, BLACK])
        self.turn = self.players.__next__()
        


        # self.move(self.board[0][0],  4, 4, self.board[0][0].checker)

    def drawBoard(self, window):
        for c in range(8):
            for r in range(8):
                cell = self.board[c][r]
                cell.draw(window)
                # cell.drawMoves(window)

          
              
    # this method moves piece from the passed cell into cell at c, r
    def move(self, cell, c, r, piece):
        if (c,r) not in piece.getValidMoves(self.board):
            return
        # if (c,r) not in piece.getValidMovesOPT(self.board):
            # return
        self.board[c][r].placePiece(piece)
        cell.removePiece()
        if piece.player == BLACK and r == 7:
            self.board[c][r].checker.king = True
        if piece.player == RED and r == 0:
            self.board[c][r].checker.king = True

    def mouseRC(self, pos):
        x = pg.mouse.get_pos()[0]
        y = pg.mouse.get_pos()[1]
        x = int (x / cell_width)
        y = int (y / cell_height)
        return x,y 

    def getPiece(self, c, r): 
        return self.board[c][r].checker
    
    def removePiece(self,c, r):
        self.board[c][r].checker = None 
    
    def drawMoves(self, c, r):
        self.board[c][r].drawMoves(window, self.board)


    def getDiagonals(self, c, r, mc, mr):
        diagonals = []
        x_vals = []
        y_vals = []
        xStep = 1
        if mc < c:
            xStep = -1
        
        yStep = 1
        if mr < r:
            yStep = -1
    
        for x in range(c, mc, xStep):
            x_vals.append(x)
        for y in range(r, mr, yStep):
            y_vals.append(y)
        
        # print(x_vals)
        # print(y_vals)
        for i in range(len(y_vals)):
            diagonals.append((x_vals[i], y_vals[i]))
        # use list of moves w coordinates (column, row)
        # 
        return diagonals

    # get all pieces of certain color
    def getAllPieces(self, player):
        pieces = []
        for c in range(8):
            for r in range(8):
                if self.board[c][r].checker != None:
                    if self.board[c][r].checker.player == player:
                        pieces.append(self.board[c][r].checker)
        return pieces

    def isPieceVuln(self, piece):
        vulnerable = False

        if piece.y < 1 or piece.y > 6 or piece.x < 1 or piece.x > 6:
            return vulnerable

        top_left = (piece.x-1, piece.y-1)
        top_right = (piece.x+1, piece.y-1)
        bottom_left = (piece.x-1, piece.y+1)
        bottom_right = (piece.x+1, piece.y+1)

        # if piece in topleft  
        if self.getPiece(top_left[0], top_left[1]) != None:
            if self.getPiece(top_left[0], top_left[1]).player != piece.player:
                # if reach here, top left is opposing piece
                if self.getPiece(bottom_right[0], bottom_right[1]) == None:
                    vulnerable = True
                    return vulnerable
        # if top right
        if self.getPiece(top_right[0], top_right[1]) != None:
            if self.getPiece(top_right[0], top_right[1]).player != piece.player:
                # if reach here, top left is opposing piece
                if self.getPiece(bottom_left[0], bottom_left[1]) == None:
                    vulnerable = True
                    return vulnerable

        # if bottom left
        if self.getPiece(bottom_left[0], bottom_left[1]) != None:
            if self.getPiece(bottom_left[0], bottom_left[1]).player != piece.player:
                # if reach here, top left is opposing piece
                if self.getPiece(top_right[0], top_right[1]) == None:
                    vulnerable = True
                    return vulnerable
        
        # if bottom right 
        if self.getPiece(bottom_right[0], bottom_right[1]) != None:
            if self.getPiece(bottom_right[0], bottom_right[1]).player != piece.player:
                # if reach here, top left is opposing piece
                if self.getPiece(top_left[0], top_left[1]) == None:
                    vulnerable = True
                    return vulnerable
                
        return vulnerable

            

    def updateKingCount(self):
        
        # to gain loose/usually correct value for vulnerable pieces, do it in here. 
        # Check the direct diagonals of each piece, if it has piece of other color on one side,
        # check the opposite diagonal to see if it can be jumped; incorporate fact that only king can 
        # go backwards in this 

        for piece in self.getAllPieces(BLACK):
            if self.isPieceVuln(piece):
                self.black_vuln += 1
            if piece.king:
                self.black_kings += 1
            if piece.y == 0:
                self.black_back += 1
            if piece.y == 3 or piece.y == 4:
                if piece.x < 2 or piece.x > 5:
                    self.black_outsidemid += 1
                else:
                    self.black_mid += 1     

        
            # if piece.y >= 5:
            #     self.black_adv += .3*(piece.y)
        for piece in self.getAllPieces(RED):
            if self.isPieceVuln(piece):
                self.red_vuln += 1
            if piece.king:
                self.red_kings += 1
            if piece.y == 7:
                self.red_back += 1
            if piece.y == 3 or piece.y == 4:
                if piece.x < 2 or piece.x > 5:
                    self.red_outsidemid += 1
                else:
                    self.red_mid += 1


            # if piece.y < 3:
            #     self.red_adv += .3*(7-piece.y)
        
        self.black_pawns = self.black_count - self.black_kings
        self.red_pawns = self.red_count - self.red_kings 


    def resetCount(self):
        self.black_kings = self.red_kings = 0
        self.red_back = self.black_back = 0
        self.red_mid = self.black_mid = 0
        self.red_outsidemid = self.black_outsidemid = 0
        self.black_adv = self.red_adv = 0
        self.black_vuln = self.red_vuln = 0

    def evalFunction(self): 
        score = 0
       
        # # if no ply has been comleted yet; score moves randomly such that board 
        # if self.terminalTest():
        #     if self.turn == RED:
        #         return 100
        #     else:
        #         return -100

                
        # if self.num_plys == 0:
        #     score = random.randint(-12, 12)
        #     return score 
        # if self.num_plys > 20:
        #     score += 2*(self.red_count - self.black_count)
        #     for posR in self.getAllPieces(RED):
        #         for pos in self.getAllPieces(BLACK):
        #             if self.black_count > self.red_count:
        #                 score += util.manhattanDistance((posR.x,posR.y), (pos.x, pos.y))
        #             if self.red_count > self.black_count:
        #                 score -= util.manhattanDistance((posR.x, posR.y),(pos.x, pos.y))
        #             score /= abs(self.red_count - self.black_count)+.01
        #     return score

        # if len(self.getAllPieces(RED)) + len(self.getAllPieces(BLACK)) < 15:
        #     score += 1.5*(self.red_count - self.black_count)

        #     # incorporate factor that scores positions based on overall distance to other pieces; 
        #     # 
        #     # for posR in self.getAllPieces(RED):
        #     #     for pos in self.getAllPieces(BLACK):
        #     #         if self.black_count > self.red_count:
        #     #             score += util.manhattanDistance((posR.x,posR.y), (pos.x, pos.y))
        #     #         if self.red_count > self.black_count:
        #     #             score -= util.manhattanDistance((posR.x, posR.y),(pos.x, pos.y))

     
        # for piece in self.getAllPieces(RED):
        #     if piece.king:
        #         score += 2
        #     score += 5+(7-piece.y)
        # for piece in self.getAllPieces(BLACK):
        #     if piece.king:
        #         score -= 2
        #     score -= (5+piece.y)


        # revised eval function according to paper I found 

        if self.num_plys == 0:
            score = random.randint(-12, 12)
            return score 

        # increase score according to factors of red player (maximizing player):
        
        score += 5*self.red_pawns
        score += 7.75 * self.red_kings
        score += 4 * self.red_back
        score += 2.5 * self.red_mid
        score += 0.5 * self.red_outsidemid
        score -= 3* self.red_vuln

        # decrease score according to factors of black player (minimizing player):
        score -= 5*self.black_pawns
        score -= 7.75 * self.black_kings
        score -= 4 * self.black_back
        score -= 2.5 * self.black_mid
        score -= 0.5 * self.black_outsidemid
        score += 3 * self.black_vuln

        return score 
    

    def terminalTest(self):
        num_moves = 0
        for i in range(2):
            if len(self.getAllPieces(self.players.__next__())) == 0:
                return True
            for piece in self.getAllPieces(self.players.__next__()):
                num_moves += len(piece.getValidMoves(self.board))
        if num_moves == 0:
            return True

        return False