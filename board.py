import pygame as pg
import random
import sys
from itertools import cycle
import minimax
import util

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
            pg.draw.rect(window, (150, 150, 150), (self.x * cell_width, self.y * cell_height, cell_width-2, cell_height-2))
        else:
            # implement logic to draw alternating colors 
            if self.y%2 == 0:
                if self.x%2== 0:
                    pg.draw.rect(window, (0,0,0), (self.x * cell_width, self.y * cell_height, cell_width-2, cell_height-2))
                else:
                    pg.draw.rect(window, (210,180,140), (self.x * cell_width, self.y * cell_height, cell_width-2, cell_height-2))
            else:
                if self.x%2== 0:
                    pg.draw.rect(window,(210,180,140), (self.x * cell_width, self.y * cell_height, cell_width-2, cell_height-2))
                else:
                    pg.draw.rect(window, (0,0,0), (self.x * cell_width, self.y * cell_height, cell_width-2, cell_height-2))
        if self.checker != None:
            if self.checker.king:
                pg.draw.circle(window, self.checker.player, (self.checker.x * cell_width + cell_width/2, self.checker.y * cell_height + cell_height/2), (cell_width/2.5))
                pg.draw.circle(window, (250,250,250), (self.checker.x * cell_width + cell_width/2, self.checker.y * cell_height + cell_height/2), (cell_width/9))
            else:
                if self.checker.player == RED:
                    pg.draw.circle(window, (0,0,0), (self.checker.x * cell_width + cell_width/2, self.checker.y * cell_height + cell_height/2), (cell_width/2.5)+1)
                else:
                     pg.draw.circle(window, (200,200,200), (self.checker.x * cell_width + cell_width/2, self.checker.y * cell_height + cell_height/2), (cell_width/2.5)+1)
                pg.draw.circle(window, self.checker.player, (self.checker.x * cell_width + cell_width/2, self.checker.y * cell_height + cell_height/2), (cell_width/2.5))
                

    def drawMoves(self, window, board):
        if self.checker != None:
            moves = self.checker.getValidMoves(board)
            for move in moves:
                if self.checker.player == BLACK:
                    pg.draw.circle(window, (0, 0, 0), (move[0] * cell_width + cell_width/2, move[1] * cell_height + cell_height/2), cell_height/9+1)
                    pg.draw.circle(window, (150, 150, 150), (move[0] * cell_width + cell_width/2, move[1] * cell_height + cell_height/2), cell_height/9)
       
                else:
                    pg.draw.circle(window, (0, 0, 0), (move[0] * cell_width + cell_width/2, move[1] * cell_height + cell_height/2), cell_height/9+1)
                    pg.draw.circle(window, (150, 150, 150), (move[0] * cell_width + cell_width/2, move[1] * cell_height + cell_height/2), cell_height/9)
        # highlight cells that can be moved into 

           
        # also highlight the cell currently selected 
        if self.checker != None:
            pg.draw.rect(window, (150, 150, 150), (self.x * cell_width, self.y * cell_height, cell_width-2, cell_height-2))
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
        self.skipped = []
        # to store pairs of moves that capture pieces w pieces captured such that if move is selected, we remove relevant 

        # moves appended in (x, y) coordinate tuples 
        # piece.getValidMoves returns list of all possible coordinates to which a piece can go
       
        leftrng = min(3, abs(self.x-0)+1)
        rightrng = min(3, abs(self.x-7)+1)
        if self.king:
                for i in range(1,rightrng):
                # check for own color in diags
                    if self.y - i >= 0:
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
        self.black_kings = self.red_kings = 0
        self.black_adv = self.red_adv = 0

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

    def updateKingCount(self):
        for piece in self.getAllPieces(BLACK):
            if piece.king:
                self.black_kings += 1
            if piece.y >= 4:
                self.black_adv += .3*(piece.y)
        for piece in self.getAllPieces(RED):
            if piece.king:
                self.red_kings += 1
            if piece.y < 4:
                self.red_adv += .3*(7-piece.y)

    def resetCount(self):
        self.black_kings = 0
        self.red_kings = 0
        self.red_adv = 0
        self.black_adv = 0

    def evalFunction(self): 
        score = 0
        # if self.black_count == 1:
        #     score -= self.black_count
        #     return score
        # if self.red_count == 1:
        #     score += self.red_count
        #     return score
    
        for piece in self.getAllPieces(RED):
            if piece.king:
                score += 5
            else:
                score += 2
        for piece in self.getAllPieces(BLACK):
            if piece.king:
                score -= 5
            else:
                score -= 2
        score += self.red_adv/(abs(self.red_count-self.black_count)+1)
        score -= self.black_adv/(abs(self.red_count-self.black_count)+1)
        
        
        # score action based on its score; actions will be stored in the resultant board state which will be evaluated by the function
        # factors to evaluate based on:
        #   - number of pieces of certain color
        #   - number of kings of certain color 
        #   - number of pieces past certain row (in upper half of board)
        #   - very lowlight weighted: number of valid moves of certain color 
        #   - is eval function within the board state itself? 
        # `

        # eval function works fine right now but can definitely be better 
        # modify to counts to have different weight in different circumstances 
        # so, depending on number of pieces of certain color, change weights 
        # for example if black has many pieces and red has few, weight the value of red pieces more such that alg is incentivized 
        # to play aggressive and take out the few remaining pieces 

        return score 
    

    def terminalTest(self):
        num_moves = 0
        for i in range(2):
            if len(self.getAllPieces(self.players.__next__())) == 0:
                return True
        #     for piece in self.getAllPieces(self.players.__next__()):
        #         num_moves += len(piece.getValidMoves(self.board))
        # if num_moves == 0:
        #     return True

        return False