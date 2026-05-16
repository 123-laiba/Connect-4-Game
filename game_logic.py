# game_logic.py
# this file handles all the board stuff like checking wins and valid moves

ROWS = 6
COLS = 7

# who is playing
HUMAN = 1
AI = 2
EMPTY = 0


def make_board():
    # 6x7 grid filled with zeros
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(EMPTY)
        board.append(row)
    return board


def is_valid_column(board, col):
    # check if the top row of this column is empty
    # if its empty then we can still drop a piece here
    return board[0][col] == EMPTY


def get_valid_columns(board):
    # return a list of columns where we can drop a piece
    valid = []
    for col in range(COLS):
        if is_valid_column(board, col):
            valid.append(col)
    return valid


def get_next_open_row(board, col):
    # pieces fall down so we need to find the lowest empty spot
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return -1  # column is full (shouldnt happen if we check valid first)


def drop_piece(board, row, col, piece):
    # just place the piece on the board
    board[row][col] = piece


def check_win(board, piece):
    # check all 4 directions for a win

    # horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == piece and
                    board[r][c+1] == piece and
                    board[r][c+2] == piece and
                    board[r][c+3] == piece):
                return True

    # vertical check
    for r in range(ROWS - 3):
        for c in range(COLS):
            if (board[r][c] == piece and
                    board[r+1][c] == piece and
                    board[r+2][c] == piece and
                    board[r+3][c] == piece):
                return True

    # diagonal going down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == piece and
                    board[r+1][c+1] == piece and
                    board[r+2][c+2] == piece and
                    board[r+3][c+3] == piece):
                return True

    # diagonal going down-left
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if (board[r][c] == piece and
                    board[r+1][c-1] == piece and
                    board[r+2][c-2] == piece and
                    board[r+3][c-3] == piece):
                return True

    return False


def is_board_full(board):
    # check if there are no valid moves left
    return len(get_valid_columns(board)) == 0


def is_terminal(board):
    # game is over if someone won or board is full
    return check_win(board, HUMAN) or check_win(board, AI) or is_board_full(board)