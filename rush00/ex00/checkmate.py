def is_square_board(board):

    n = len(board)
    return all(len(row) == n for row in board)

def has_one_king(board):

    king_count = sum(row.count('K') for row in board)
    return king_count == 1

def is_king_checked(board):

    if not is_square_board(board):
        print("error: The board must be a square")
        return

    if not has_one_king(board):
        print("error: The board must contain exactly one King")
        return

    n = len(board)  # ขนาดของกระดาน

    # หาตำแหน่งของกษัตริย์
    king_pos = None
    for i, row in enumerate(board):
        if 'K' in row:
            king_pos = (i, row.index('K'))
            break

    kx, ky = king_pos

    def is_in_bounds(x, y):
        return 0 <= x < n and 0 <= y < n

    # ทิศทางสำหรับ Pawn, Bishop, Rook และ Queen
    pawn_dirs = [(1, -1), (1, 1)]  # Pawn
    bishop_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Bishop
    rook_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Rook
    queen_dirs = bishop_dirs + rook_dirs  # Queen + Bishop + Rook

    # Ckeck Pawn
    for dx, dy in pawn_dirs:
        nx, ny = kx + dx, ky + dy
        if is_in_bounds(nx, ny) and board[nx][ny] == 'P':
            print("Success")
            return

    # Check Bishop, Rook, และ Queen
    for piece, directions in [('B', bishop_dirs), ('R', rook_dirs), ('Q', queen_dirs)]:
        for dx, dy in directions:
            x, y = kx, ky
            while True:
                x, y = x + dx, y + dy
                if not is_in_bounds(x, y):
                    break
                if board[x][y] == piece:
                    print("Success")
                    return
                elif board[x][y] != '.':  # Has obstruction
                    break


    print("Fail")