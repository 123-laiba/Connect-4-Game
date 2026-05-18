# main.py
# run this file to start the game

import tkinter as tk
from gui import Connect4GUI


def main():
    root = tk.Tk()
    game = Connect4GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()