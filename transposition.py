import board 
import random
BLACK = (0,0,0)
RED = (250,0,0)

# how to ensure all this handles what the best next board is depending on the turn?
#   - have hash table for both maximizing player and minimizing player


# need to write zobrist key function for board state:
#   - function needs to ensure that no board will have the same hash value 
#   - start w empty string to rep int
#   - loop over cells in board
#   - if cell.checker == None: add 1 to the zobrist key string 
#   - if cell.checker == red: if not king: add 2 to the zobrist key string, else: add 3 to string 
#   - if cell.checker == black: if not king: add 4 to the zobrist key string, else: add 5 to string 
#  convert string to int; shud b 64 digit int 

# might need this to diversify zobrist keys; we'll see after testing 
def randIntForPieceType():
    # have list of random numbers for each diff type of cell
    cells = []
    for i in range(5):
        cells.append(random.randint(0, 999999999))
    return cells
cells = randIntForPieceType()
def zobristKey(board):
    toReturn = ''
    # toReturn = 0
    for c in range(8):
        for r in range(8):
            if board[c][r].checker == None:
                toReturn += '1'
                # toReturn += str(cells[0])

            if board[c][r].checker:
                if board[c][r].checker.player == RED:
                    if board[c][r].checker.king:
                        toReturn += '3'
                        # toReturn += str(cells[2])
                    else:
                        toReturn += '2'
                        # toReturn += str(cells[1])
                else:
                    if board[c][r].checker.king:
                        toReturn += '5'
                        # toReturn += str(cells[4])
                    else:
                        toReturn += '4'
                        # toReturn += str(cells[3])

    return int(toReturn)

# need to write hash function for zobrist key:
#   - zobristkey % hashtable.size = index to store board w this key in hash table
# within the array, a value array[hash(zobrist(board))] will be equal to the minimax value (zobristKey, score,best subsequent boardstate) for the inputted board
# if that board has been seen, and None/0 otherwise 

def hashZobrist(zobristKey, hashTable):
    hashIndex = zobristKey % len(hashTable)
    return hashIndex

# write function for checking: takes in board state 
#   - if array[hashfunction(board)] != None:
#   -   return array[hashfunction(board)]
# 

def transpoCheck(board, hashTable):
    zobrist = zobristKey(board)
    boardIndex = hashZobrist(zobrist, hashTable)
    if hashTable[boardIndex] != None:
        # check if zobrist key is same 
        if hashTable[boardIndex][0] == zobrist:
            # return result valid for minimax (score, best subsequent boardState)
            return (hashTable[boardIndex][1], hashTable[boardIndex][2])
    return None
    

# lets do some testing below 

# arrayTest = [None] * 999

# testBoard = board.Board()
# print(zobristKey(testBoard.board))
# print(hashZobrist(zobristKey(testBoard.board), arrayTest))


# to implement these methods/transposition tables in minimax I need to: 
#   - everytime a minimax returns a (score, move) pair, I need to store the following in a tuple within transpo table
#       - zobrist key of board whose ideal result is being store 
#       - score 
#       - move (best successor board state)
#   - 


# SIUUUIUUUUU
# Update (12/2):
#   - as of now, transposition tables seem to be working, however, there is a high probability that is is buggy when having AI vs AI 
#   - going forward, think abt how we can modify minimax such that transposition table will replace old (seen many turns ago) board states, 
#     with more recent ones when it updates the table 
#   - this shud improve how it optimizes throughout the game 
#   - also do runtime analysis and incoporate into charts 
#   - update: definitely buggy, but very nichely; works for the most part when minimax is pit against human opponet
#   - will look for more buggy cases tmrw 