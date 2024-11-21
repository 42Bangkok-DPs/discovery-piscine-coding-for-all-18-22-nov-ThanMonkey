#!/usr/bin/env python3
from checkmate import is_king_checked

if __name__ == "__main__":
    # Input board as a list of strings (rows)
    board = [
        "....",
        ".K..",
        "....",
        "...."
    ]
    
    is_king_checked(board)