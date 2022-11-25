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

font = pg.font.SysFont('chalkboardse', 15)
bigFont = pg.font.SysFont('chalkboardse', 40)

def play(): 
    max_transposition = util.Counter()
    min_transposition = util.Counter()

    menu = True
    oneP  = False
    twoP = False
    zeroP = False 

    while menu:
        window.fill(BLACK)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_0:
                    zeroP = True
                    oneP = True
                    menu = False
                if event.key == pg.K_1:
                    oneP = True
                    menu = False
                if event.key == pg.K_2:
                    twoP = True
                    menu = False
        
        header  = bigFont.render("Checkers", True, (250,250,250))
        instruc  = font.render("Press 0 to watch the AI play. Press 1 to play vs the AI. Press 2 to play two player. Press r to reset board", True, (250,250,250))
        window.blit(header, (window_width/2-header.get_width()/2, window_height/2-header.get_height()/2-80))
        window.blit(instruc, (window_width/2-instruc.get_width()/2, window_height/2-header.get_height()/2))
        pg.display.flip()


            
    test = board.Board()
    selected = False
    run = True
    window.fill((0,0,0))
    old_board = None
    while True:
        window.fill((0,0,0))
        while run:
            # clock.tick(60)
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

            # to debug minimax, have an input that allows you to undo a turn, will allow me to see precisely where
            # and thus hopefully deduce why minimax might be going wrong; ok, definitely minimax that is bugging; question is
            # WHY
            # was in valid moves generation, indices were going out of bounds but it is now fixed 
            # right now, valid moves is very unoptimal. unfortunate 
            
            if oneP:
                if test.turn == BLACK:
                    selected = False
                    old_board = test
                    new_board = minimax.minValue(test, 4, -99999, 99999, min_transposition, max_transposition)[1]
                    # new_board = minimax.EminValue(test, 3)[1]
                    test = new_board
                    clock.tick(60)
                    test.num_plys += 1
                    print("Turn: " + str(test.turn))
                    print("SCORE: " + str(test.evalFunction()))
                    print("Plys Completed: " + str(test.num_plys))
                else: 
                    if zeroP:
                        selected = False
                        # if test.turn != RED:
                            # test.turn = test.players.__next__()
                        # new_board = minimax.maxValue(test, 4, -99999, 99999, max_transposition, min_transposition)[1]
                        new_board = minimax.EmaxValue(test, 3)[1]
                        test = new_board
                        # test.turn = test.players.__next__()
                        print("Turn: " + str(test.turn))
                        print("SCORE: " + str(test.evalFunction()))


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
                    if event.key == pg.K_BACKSPACE:
                        test = old_board
                        test.turn = test.players.__next__()
                if event.type == pg.MOUSEBUTTONDOWN and selected:
                    param = pg.mouse.get_pos()
                    mc, mr = test.mouseRC(param)
                    if test.getPiece(c,r) == None:
                            continue

                    if (mc,mr) not in test.getPiece(c,r).getValidMoves(test.board):
                        continue

                    # if (mc, mr) not in test.getPiece(c,r).getValidMovesOPT(test.board):
                    #     continue 
                    if test.getPiece(c,r).player == test.turn:
                        removed = 0

                        # removal new
                        # for m_s in test.getPiece(c,r).getValidMovesOPT(test.board):
                        #     # if move chosen is move on
                        #     if m_s[0] == (mc,mr):
                        #         # iterate thorugh skipped pos for that move and remove them
                        #         for skip in m_s[1]:
                        #             test.removePiece(skip[0], skip[1])
                        test.move(test.board[c][r], mc,mr, test.getPiece(c,r))
                        for pos in test.getDiagonals(c,r, mc, mr):
                            x = pos[0]
                            y = pos[1]
                            if test.board[x][y].checker != None:
                                if test.board[x][y].checker.player == BLACK and test.turn == RED:
                                    test.black_count -= 1
                                if test.board[x][y].checker.player == RED and test.turn == BLACK:
                                    test.red_count -= 1
                                if test.getPiece(x,y).player != test.turn:
                                    test.removePiece(x, y)
                                    removed += 1
                       
                        print("Black Pieces: " + str(test.black_count) + " Black Kings: " + str(test.black_kings))
                        print("Red Pieces: " + str(test.red_count) + " Red Kings: " + str(test.red_kings))
                        print("Score: " + str(test.evalFunction()))
                        # if removed != 1:
                        test.turn = test.players.__next__()
                    
                        selected = False

            test.drawBoard(window)
            if selected:
                # if the piece selected is whose turn it is
                if test.getPiece(c,r) != None and test.getPiece(c,r).player == test.turn: 
                    test.drawMoves(c, r)
                
        while not run:
            # window.fill((0,0,0))
            winner = font.render(res, True, (250,250,250), (0,0,0))
            rest = font.render("Press r to restart", True, (250,250,250), (0,0,0))
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