 # this file has the minimax algorithm with alpha-beta pruning and the heuristic function
# the AI uses this to decide where to drop its piece
#
# alpha-beta pruning explanation:
# normal minimax checks EVERY possible move which is slow
# alpha-beta pruning skips branches that we already know wont be picked
# alpha = best score the maximizer (AI) has found so far
# beta  = best score the minimizer (human) has found so far
# if beta <= alpha we can stop early because the other player will never let this happen
# same result as minimax but much faster!
 
from game_logic import *
 
DEPTH = 5 
 
 
def score_window(window, piece):
    # score a group of 4 cells
    # window is just a list of 4 values from the board
    score = 0
    opp = HUMAN if piece == AI else AI
 
    if window.count(piece) == 4:
        score += 100  # we won!
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10  # 3 in a row is good
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5   # 2 in a row is ok
 
    # block opponent if they have 3 in a row
    if window.count(opp) == 3 and window.count(EMPTY) == 1:
        score -= 80
 
    return score
