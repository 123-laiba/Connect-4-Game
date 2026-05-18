# gui.py
# this file handles the tkinter window and drawing the board
# also handles mouse clicks from the player

import tkinter as tk
from tkinter import messagebox
from game_logic import *
from ai import get_ai_move

# some color constants so its easier to change later
COLOR_BG = "#1a1a2e"        # dark blue background
COLOR_BOARD = "#16213e"     # slightly lighter for the board
COLOR_EMPTY = "#0f3460"     # empty cell color
COLOR_HUMAN = "#e94560"     # red/pink for human
COLOR_AI = "#f5a623"        # orange/yellow for AI
COLOR_HIGHLIGHT = "#ffffff" # white for hover highlight

CELL_SIZE = 90    # size of each cell in pixels
RADIUS = 35       # radius of the circles (pieces)
PADDING = 10      # padding around the board


class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4 - Human vs AI")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        # game state
        self.board = make_board()
        self.game_over = False
        self.human_turn = True  # human goes first

        self.setup_ui()
        self.draw_board()

    def setup_ui(self):
        # top info label
        self.info_label = tk.Label(
            self.root,
            text="Your Turn! (Red)",
            font=("Arial", 16, "bold"),
            fg=COLOR_HUMAN,
            bg=COLOR_BG,
            pady=10
        )
        self.info_label.pack()

        # canvas for the board
        canvas_width = COLS * CELL_SIZE + PADDING * 2
        canvas_height = ROWS * CELL_SIZE + PADDING * 2

        self.canvas = tk.Canvas(
            self.root,
            width=canvas_width,
            height=canvas_height,
            bg=COLOR_BOARD,
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=5)

        # bind mouse events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_hover)

        # restart button at the bottom
        restart_btn = tk.Button(
            self.root,
            text="New Game",
            font=("Arial", 12),
            bg="#0f3460",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.restart_game
        )
        restart_btn.pack(pady=10)

        # keep track of hover column for highlighting
        self.hover_col = -1

    def get_col_from_x(self, x):
        # convert pixel x position to column number
        col = (x - PADDING) // CELL_SIZE
        if 0 <= col < COLS:
            return col
        return -1

    def draw_board(self):
        # clear and redraw everything
        self.canvas.delete("all")

        for r in range(ROWS):
            for c in range(COLS):
                # calculate pixel positions
                x1 = c * CELL_SIZE + PADDING
                y1 = r * CELL_SIZE + PADDING
                x_center = x1 + CELL_SIZE // 2
                y_center = y1 + CELL_SIZE // 2

                # pick color based on whats in this cell
                piece = self.board[r][c]
                if piece == HUMAN:
                    color = COLOR_HUMAN
                elif piece == AI:
                    color = COLOR_AI
                else:
                    # highlight the column the mouse is hovering over
                    if c == self.hover_col and self.human_turn and not self.game_over:
                        color = "#1a4a8a"  # slightly lighter to show hover
                    else:
                        color = COLOR_EMPTY

                # draw the circle
                self.canvas.create_oval(
                    x_center - RADIUS,
                    y_center - RADIUS,
                    x_center + RADIUS,
                    y_center + RADIUS,
                    fill=color,
                    outline=""
                )

    def on_hover(self, event):
        # highlight column when mouse moves over it
        col = self.get_col_from_x(event.x)
        if col != self.hover_col:
            self.hover_col = col
            self.draw_board()

    def on_click(self, event):
        # handle when player clicks on the board
        if self.game_over or not self.human_turn:
            return

        col = self.get_col_from_x(event.x)
        if col == -1:
            return

        if not is_valid_column(self.board, col):
            # column is full, ignore
            return

        # human makes their move
        row = get_next_open_row(self.board, col)
        drop_piece(self.board, row, col, HUMAN)
        self.draw_board()

        # check if human won
        if check_win(self.board, HUMAN):
            self.info_label.config(text="You Win! 🎉", fg=COLOR_HUMAN)
            self.game_over = True
            messagebox.showinfo("Game Over", "Congratulations! You beat the AI!")
            return

        # check tie
        if is_board_full(self.board):
            self.info_label.config(text="It's a Tie!", fg="white")
            self.game_over = True
            messagebox.showinfo("Game Over", "It's a draw!")
            return

        # now its AI turn
        self.human_turn = False
        self.info_label.config(text="AI is thinking...", fg=COLOR_AI)
        self.root.update()  # update the screen so the label shows

        # small delay so it doesnt feel instant
        self.root.after(300, self.ai_move)

    def ai_move(self):
        # let the AI make its move
        col = get_ai_move(self.board)

        if col is not None and is_valid_column(self.board, col):
            row = get_next_open_row(self.board, col)
            drop_piece(self.board, row, col, AI)
            self.draw_board()

        # check if AI won
        if check_win(self.board, AI):
            self.info_label.config(text="AI Wins!", fg=COLOR_AI)
            self.game_over = True
            messagebox.showinfo("Game Over", "The AI won this time. Try again!")
            return

        # check tie
        if is_board_full(self.board):
            self.info_label.config(text="It's a Tie!", fg="white")
            self.game_over = True
            messagebox.showinfo("Game Over", "It's a draw!")
            return

        # back to human turn
        self.human_turn = True
        self.info_label.config(text="Your Turn! (Red)", fg=COLOR_HUMAN)

    def restart_game(self):
        # reset everything for a new game
        self.board = make_board()
        self.game_over = False
        self.human_turn = True
        self.hover_col = -1
        self.info_label.config(text="Your Turn! (Red)", fg=COLOR_HUMAN)
        self.draw_board()