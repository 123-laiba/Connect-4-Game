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

def heuristic(board, piece):
    # give a score to the whole board
    # positive = good for AI, negative = bad for AI
    total_score = 0
 
    # prefer center column (better positions come from center)
    center_col = COLS // 2
    center_array = [board[r][center_col] for r in range(ROWS)]
    center_count = center_array.count(piece)
    total_score += center_count * 6
 
    # check horizontal windows
    for r in range(ROWS):
        for c in range(COLS - 3):
            window = [board[r][c+i] for i in range(4)]
            total_score += score_window(window, piece)
 
    # check vertical windows
    for c in range(COLS):
        for r in range(ROWS - 3):
            window = [board[r+i][c] for i in range(4)]
            total_score += score_window(window, piece)
 
    # check diagonal going down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            total_score += score_window(window, piece)
 
    # check diagonal going down-left
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            window = [board[r+i][c-i] for i in range(4)]
            total_score += score_window(window, piece)
 
    return total_score

def minimax(board, depth, alpha, beta, is_maximizing):
    # minimax with alpha-beta pruning
    # alpha = best score AI has found so far (starts at -infinity)
    # beta  = best score human has found so far (starts at +infinity)
    # we prune (skip) branches when beta <= alpha
 
    # base cases - stop recursing when game is over or depth is 0
    if check_win(board, AI):
        return (None, 100000)  # AI wins, super good
    if check_win(board, HUMAN):
        return (None, -100000)  # human wins, super bad
    if is_board_full(board):
        return (None, 0)  # tie
    if depth == 0:
        # cant go deeper so just score the current board
        return (None, heuristic(board, AI))
 
    valid_cols = get_valid_columns(board)
    best_col = valid_cols[0]  # just pick first valid as default
 
    if is_maximizing:
        # AI turn - we want the highest score
        best_score = -999999
        for col in valid_cols:
            row = get_next_open_row(board, col)
            # try this move
            drop_piece(board, row, col, AI)
            # recursively check what happens
            _, score = minimax(board, depth - 1, alpha, beta, False)
            # undo the move
            board[row][col] = EMPTY
 
            if score > best_score:
                best_score = score
                best_col = col
 
            # update alpha (best we can guarantee for AI)
            alpha = max(alpha, best_score)
 
            # prune-the human already has a better option elsewhere
            # so they will never let the game reach this state
            # no point checking the rest of the moves here
            if beta <= alpha:
                break  # prune this branch
 
        return (best_col, best_score)
 
    else:
        # human turn - we assume human plays best move (minimize score for AI)
        best_score = 999999
        for col in valid_cols:
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, HUMAN)
            _, score = minimax(board, depth - 1, alpha, beta, True)
            board[row][col] = EMPTY
 
            if score < best_score:
                best_score = score
                best_col = col
 
            # update beta (best the human can guarantee)
            beta = min(beta, best_score)
 
            # prune! AI already has a better option elsewhere
            # it will never choose a path that lets human get here
            if beta <= alpha:
                break  # prune this branch
 
        return (best_col, best_score)