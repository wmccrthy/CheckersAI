import board 
import minimax
import util
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

def play(): 
    max_transposition = util.Counter()
    min_transposition = util.Counter()

    menu = True
    oneP  = False
    twoP = False
    while menu:
        window.fill(BLACK)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    oneP = True
                    menu = False
                if event.key == pg.K_2:
                    twoP = True
                    menu = False
        
        header  = bigFont.render("Checkers", True, (250,250,250))
        instruc  = font.render("Press 1 to play vs the AI. Press 2 to play two player. Press r to reset board", True, (250,250,250))
        window.blit(header, (window_width/2-header.get_width()/2, window_height/2-header.get_height()/2-80))
        window.blit(instruc, (window_width/2-instruc.get_width()/2, window_height/2-header.get_height()/2))
        pg.display.flip()


            
    test = board.Board()
    selected = False
    run = True
    window.fill((150,150,150))
    while run:
        clock.tick(60)
        pg.display.flip()

        test.resetCount()
        test.updateKingCount()

        if test.terminalTest():
            window.fill((0,0,0))
            if test.evalFunction() > 0:
                print("GAME OVER | WINNER: RED | SCORE: " + str(test.evalFunction()))
                res = "GAME OVER | WINNER: RED | SCORE: " + str(test.evalFunction())
            else:
                res = "GAME OVER | WINNER: BLACK | SCORE: " + str(test.evalFunction())
                print("GAME OVER | WINNER: BLACK | SCORE: " + str(test.evalFunction()))
            run = False

        if oneP:
            if test.turn == BLACK:
                selected = False
                new_board = minimax.minValue(test, 3, -99999, 99999, min_transposition, max_transposition)[1]
                # new_board = minimax.EminValue(test, 3)[1]
                # new_board = minimax.expectiValue(test, 3)[1]
                test = new_board
                test.turn = test.players.__next__()
                print("Turn: " + str(test.turn))
                print("SCORE: " + str(test.evalFunction()))
        # else:
        #     selected = False
        #     new_board = minimax.EmaxValue(test, 3)[1]
        #     test = new_board
        #     test.turn = test.players.__next__()
        #     print("Turn: " + str(test.turn))
        #     print("SCORE: " + str(test.evalFunction()))


        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    param = pg.mouse.get_pos()
                    c, r = test.mouseRC(param)
                    if test.getPiece(c,r) == None:
                        continue
                    selected = True
                if event.key == pg.K_r:
                    test = board.Board()
            if event.type == pg.MOUSEBUTTONDOWN and selected:
                param = pg.mouse.get_pos()
                mc, mr = test.mouseRC(param)
                if test.getPiece(c,r) == None:
                        continue
                if (mc,mr) not in test.getPiece(c,r).getValidMoves(test.board):
                    continue
                if test.getPiece(c,r).player == test.turn:
                    test.move(test.board[c][r], mc,mr, test.getPiece(c,r))
                
                    for pos in test.getDiagonals(c, r, mc, mr):
                        x = pos[0]
                        y = pos[1]
                        if test.board[x][y].checker != None:
                            if test.board[x][y].checker.player == BLACK:
                                test.black_count -= 1
                            if test.board[x][y].checker.player == RED:
                                test.red_count -= 1
                        test.removePiece(x, y)
                    print("Black Pieces: " + str(test.black_count) + " Black Kings: " + str(test.black_kings))
                    print("Red Pieces: " + str(test.red_count) + " Red Kings: " + str(test.red_kings))
                    print("Score: " + str(test.evalFunction()))
                    

                    test.turn = test.players.__next__()
                
                    selected = False

                # need to implement rule that skipped pieces are removed (done as of 11/20)
                # need to implement king functionality (done as of 11/20)
                #these are final steps before game is essentailly fully playabale; need to then implement system for winning / losing 
                
                # start thinking abt eval function, how to implement minimax 
        
        test.drawBoard(window)
        if selected:
            # if the piece selected is whose turn it is
            if test.getPiece(c,r) != None and test.getPiece(c,r).player == test.turn: 
                test.drawMoves(c, r)
               
    while not run:
        window.fill((0,0,0))
        winner = font.render(res, True, (250,250,250))
        rest = font.render("Press r to restart", True, (250,250,250))
        window.blit(winner, (window_width/2-winner.get_width()/2, window_height/2-winner.get_height()/2))
        window.blit(rest, (window_width/2-winner.get_width()/2, window_height/2-winner.get_height()/2+25))

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    test = board.Board()
                    run = True
        
play()