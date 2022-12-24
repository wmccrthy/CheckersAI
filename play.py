import board 
import minimax
import pygame as pg
import sys
import time
from statistics import mean
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

    max_transposition = [None] * 4999
    min_transposition = [None] * 4999

    # run test game before hand to fill transposition tables so ai starts out at optimal speed 
    test_runs = board.Board()
    test_games = 0
    while test_games < 3:
        if test_runs.terminalTest() or test_runs.num_plys > 75:
            print("Test Game Over: " + str(test_runs.black_count))
            test_games += 1
            test_runs = board.Board()
        if test_runs.turn == BLACK:
             test_runs = minimax.minValue(test_runs, 1, -99999, 99999, min_transposition, max_transposition)[1]
             test_runs.num_plys += 1
        else:
            test_runs = minimax.EmaxValue(test_runs, 1)[1]
            # test_runs = minimax.maxValue(test_runs, 1, -99999, 99999, max_transposition, min_transposition)[1]
        test_runs.resetCount()
        test_runs.updateKingCount()


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
        
        minimax_runtimes = []
        expectiminimax_runtimes = []
        # lists used for computing avg computation time of algorithms after terminal state reached 

        while run:
            # pg.display.quit()
            pg.display.flip()

            if test.terminalTest():
                # window.fill((0,0,0))
                if test.red_count > test.black_count:
                    print("GAME OVER | WINNER: RED | SCORE: " + str(test.evalFunction()))
                    res = "GAME OVER | WINNER: RED | SCORE: " + str(test.evalFunction())
                else:
                    print("GAME OVER | WINNER: BLACK | SCORE: " + str(test.evalFunction()))
                    res = "GAME OVER | WINNER: BLACK | SCORE: " + str(test.evalFunction())
                if oneP:
                    print("Average Minimax Decision Time: " + str(mean(minimax_runtimes)) + " Seconds | Best Time: " + str(min(minimax_runtimes)) + " Seconds | Worst Time: " + str(max(minimax_runtimes)) + " Seconds")
                    if zeroP:
                        print("Average Expectimax Decision Time: " + str(mean(expectiminimax_runtimes)) + " Seconds | Best Time: " + str(min(expectiminimax_runtimes)) + " Seconds | Worst Time: " + str(max(expectiminimax_runtimes)) + " Seconds")
                    print()
                run = False
                break

            # to debug minimax, have an input that allows you to undo a turn, will allow me to see precisely where
            # and thus hopefully deduce why minimax might be going wrong; ok, definitely minimax that is bugging; question is
            # WHY
            # was in valid moves generation, indices were going out of bounds but it is now fixed 
            # right now, valid moves is very unoptimal. unfortunate 
            
            if oneP:
                if test.turn == BLACK:
                    start = time.perf_counter()
                    selected = False
                    old_board = test
                    ensure_numplys = test.num_plys
                    new_board = minimax.minValue(test, 4, -99999, 99999, min_transposition, max_transposition)[1]
                    # change depth to make opponent harder 
                    # change to new_board = minimax.Eminvalue() to play against expectiminimax
                    test = new_board
                    runtime = time.perf_counter() - start
                    minimax_runtimes.append(runtime)
                    test.num_plys = ensure_numplys + 1
                    test.resetCount()
                    test.updateKingCount()
                    print("MINIMAX TURN: ")
                    print("Black Pieces: " + str(test.black_count) + " Black Kings: " + str(test.black_kings) + " Black Pawns: " + str(test.black_pawns) + " Black Back: " + str(test.black_back) + " Black Mid: " + str(test.black_mid) + " Black Vuln: " + str(test.black_vuln) )
                    print("Red Pieces: " + str(test.red_count) + " Red Kings: " + str(test.red_kings) + " Red Pawns: " + str(test.red_pawns) + " Red Back: " + str(test.red_back) + " Red Mid: " + str(test.red_mid) + " Red Vuln: " + str(test.red_vuln))
                    print("Score: " + str(test.evalFunction()))
                    print("Plys Completed: " + str(test.num_plys))
                    print("Time Taken to Compute Move: " + str(runtime) + " seconds")
                    print()

                 
                elif zeroP: 
                    selected = False
                    # new_board = minimax.maxValue(test, 2, -99999, 99999, max_transposition, min_transposition)[1]
                    start = time.perf_counter()
                    new_board = minimax.EmaxValue(test, 1)[1]
                    test = new_board
                    test.resetCount()
                    test.updateKingCount()
                    runtime = time.perf_counter() - start
                    expectiminimax_runtimes.append(runtime)
                    print("EXPECTIMAX TURN: ")
                    print("Black Pieces: " + str(test.black_count) + " Black Kings: " + str(test.black_kings) + " Black Pawns: " + str(test.black_pawns) + " Black Back: " + str(test.black_back) + " Black Mid: " + str(test.black_mid) + " Black Vuln: " + str(test.black_vuln) )
                    print("Red Pieces: " + str(test.red_count) + " Red Kings: " + str(test.red_kings) + " Red Pawns: " + str(test.red_pawns) + " Red Back: " + str(test.red_back) + " Red Mid: " + str(test.red_mid) + " Red Vuln: " + str(test.red_vuln))
                    print("Score: " + str(test.evalFunction()))
                    print("Plys Completed: " + str(test.num_plys))
                    print("Time Taken to Compute Move: " + str(runtime) + " seconds")
                    print()

  
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

                    if test.getPiece(c,r).player == test.turn:
                        removed = 0

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
                        
                        test.turn = test.players.__next__() 

                       
                        # purely to count vulnerables 
                        selected = False
                        print("PLAYER TURN: ")
                        print("Black Pieces: " + str(test.black_count) + " Black Kings: " + str(test.black_kings) + " Black Pawns: " + str(test.black_pawns) + " Black Back: " + str(test.black_back) + " Black Mid: " + str(test.black_mid) + " Black Vuln: " + str(test.black_vuln) )
                        print("Red Pieces: " + str(test.red_count) + " Red Kings: " + str(test.red_kings) + " Red Pawns: " + str(test.red_pawns) + " Red Back: " + str(test.red_back) + " Red Mid: " + str(test.red_mid) + " Red Vuln: " + str(test.red_vuln))
                        print("Turn: " + str(test.turn))
                        print("Score: " + str(test.evalFunction()))
                        print("Plys Completed: " + str(test.num_plys))
                        print()

            test.resetCount()
            test.updateKingCount()
            
           
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