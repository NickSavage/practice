from collections import defaultdict

class Board:
    def __init__(self, state):
        self.state = state
        self.options = [[[] for _ in range(9)] for _ in range(9)]

sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

complete_sudoku_board = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

ROWS = 9
COLS = 9

def generate_cell_options(board, row, col) -> list:
    if board.state[row][col] != 0:
        print("pos already filled")
        return []
    options = []
    freq = defaultdict(int)
    for col_index in range(COLS):
        item = board.state[row][col_index]
        freq[item] += 1
    for row_index in range(ROWS):
        item = board.state[row_index][col]
        freq[item] += 1
    square_row = int(row / 3)
    square_col = int(col / 3)
    for col_index in range(3):
        for row_index in range(3):
            x = square_row * 3 + row_index
            y = square_col * 3 + col_index
            item = board.state[x][y]
            print(row, col, square_row, square_col, x, y, item)
            freq[item] += 1

    for number in range(0,10):
        if freq[number] == 0:
            if item not in options:
                options.append(number)
    return options

def find_options(board) -> None:
    for row in range(ROWS):
        for col in range(COLS):
            if board.state[row][col] != 0:
                board.options[row][col] = []
                continue
            board.options[row][col] = generate_cell_options(board, row, col)

def is_solved(board) -> bool:
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    for row_index in range(ROWS):
        freq = defaultdict(int)
        print(f"check row {row_index}")
        for col_index in range(COLS):
            item = board[row_index][col_index]
            freq[item] += 1
            if freq[item] != 1:
                print("not complete")
                return False

    for col_index in range(COLS): # s/b different
        freq = defaultdict(int)
        print(f"check col {col_index}")
        for col_index in range(ROWS):
            item = board[row_index][col_index]
            freq[item] += 1
            if freq[item] != 1:
                print("not complete")
                return False

    for square_row_index in range(int(ROWS / 3)):
        for square_col_index in range(int(COLS / 3)):
            freq = defaultdict(int)
            x = square_row_index * 3
            y = square_col_index * 3
            for i in range(3):
                for j in range(3):
                    item = board[x + i][y + j]
                    freq[item] += 1
                    if freq[item] != 1:
                        print("not complete")
                        return False
            pass

    return True

assert is_solved(sudoku_board) == False
assert is_solved(complete_sudoku_board)
board = Board(sudoku_board)

for row in board.state:
    print(row)

while True:
    find_options(board)

    for row in board.options:
        print(row)

    print()
    change = False
    for row in range(ROWS):
        for col in range(COLS):
            options = board.options[row][col]
            if len(options) == 1:
                print(f"changed {row} {col}")
                board.state[row][col] = board.options[row][col][0]
                board.options[row][col] = []
                change = True
                break
        if change:
            break
    if not change:
        print("no change made")
        break

    for row in board.state:
        print(row)
    if is_solved(board.state):
        print("solved!")
        break 
for row in board.state:
    print(row)
