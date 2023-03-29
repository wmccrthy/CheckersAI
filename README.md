# CheckersAI
*IN PROGRESS*
A checkers game made with pygame that uses minimax and expectimax to implement artificial intelligence for the computer player. Minimax is implemented with alpha beta pruning.
Supports solo play vs the AI or two player. Still buggy, need to fix small things and polish. 

board.py contains: 
  - object oriented set up of program; this includes a board, cell, and checker piece class as well as relevant functions and variables. 
 
 play.py contains: 
  - the control flow for the game; essentially holds the game loop and data relevant to each game. 
  
 minimax.py contains: 
  - the primary and accessory functions that implement the minimax and expectimax algorithms with presorting, alpha-beta pruning and transposition tables.
  
transposition.py contains:
  - the functions used to implement an augmented form of zobrist hashing, used for the implementation of transposition tables within the minimax algorithm. 
  
  
