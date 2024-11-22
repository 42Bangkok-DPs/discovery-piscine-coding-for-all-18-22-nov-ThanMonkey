#!/usr/bin/env python3
def validate_board(board):
    """
    ตรวจสอบว่ากระดานเป็นสี่เหลี่ยมจัตุรัส
    """
    size = len(board)
    return all(len(row) == size for row in board)

def find_king(board):
    """ค้นหาตำแหน่งของ King"""
    kings = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == "♕":
                kings.append((i, j))
    if len(kings) != 1:
        raise ValueError("ต้องมี King บนกระดานเพียง 1 ตัว")
    return kings[0]

def is_king_checked(board):
    """
    ตรวจสอบว่า King โดนรุกหรือไม่
    """
    king_position = find_king(board)
    king_row, king_col = king_position

    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # แนวตั้ง-แนวนอน
        (-1, -1), (1, 1), (-1, 1), (1, -1)  # แนวทแยง
    ]

    for dr, dc in directions:
        r, c = king_row, king_col
        while 0 <= r < len(board) and 0 <= c < len(board):
            r += dr
            c += dc
            if r < 0 or c < 0 or r >= len(board) or c >= len(board):
                break
            if board[r][c] == "⠀":  # ช่องว่าง
                continue
            if board[r][c] in {"♚", "♖"} and (dr == 0 or dc == 0):  # Queen หรือ Rook โจมตีแนวตรง
                return True
            if board[r][c] in {"♚", "♗"} and (dr != 0 and dc != 0):  # Queen หรือ Bishop โจมตีทแยง
                return True
            break  # หยุดเมื่อเจอหมากอื่นที่ไม่เกี่ยวข้อง

    pawn_directions = [(1, -1), (1, 1)]  # Pawn เดินโจมตีทแยง
    for dr, dc in pawn_directions:
        pr, pc = king_row + dr, king_col + dc
        if 0 <= pr < len(board) and 0 <= pc < len(board) and board[pr][pc] == "♙":
            return True

    return False

