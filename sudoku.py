from collections import defaultdict
from typing import List
import copy

class Position:
    def __init__(self, row, col, number, state, rejected):
        self.row = row
        self.col = col
        self.number = number
        self.state = copy.deepcopy(state)
        self.rejected = copy.deepcopy(rejected)

class Board:
    def __init__(self, state):
        self.state = state
        self.options = [[[] for _ in range(9)] for _ in range(9)]
        self.rejected = [[[] for _ in range(9)] for _ in range(9)]
        self.guesses: List[Position] = []
        self.no_match = False
        self.complete = False
        self.inconsistency = False

sudoku_hard = [
    [0, 0, 0, 6, 0, 0, 4, 0, 0],
    [7, 0, 0, 0, 0, 3, 6, 0, 0],
    [0, 0, 0, 0, 9, 1, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 0, 1, 8, 0, 0, 0, 3],
    [0, 0, 0, 3, 0, 6, 0, 4, 5],
    [0, 4, 0, 2, 0, 0, 0, 6, 0],
    [9, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 1, 0, 0]
]

sudoku_medium = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

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

ROWS = 9
COLS = 9

def generate_cell_options(board, row, col) -> list:
    if board.state[row][col] != 0:
        print("pos already filled")
        return []
    options = []

    freq = defaultdict(int)
    square_row = int(row / 3)
    square_col = int(col / 3)

    for col_index in range(COLS):
        item = board.state[row][col_index]
        freq[item] += 1
    for row_index in range(ROWS):
        item = board.state[row_index][col]
        freq[item] += 1

    for col_index in range(3):
        for row_index in range(3):
            x = square_row * 3 + row_index
            y = square_col * 3 + col_index
            freq[board.state[x][y]] += 1

    for number in range(0,10):
        if freq[number] == 0:
            if item not in options:
                if number not in board.rejected[row][col]:
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
        for col_index in range(COLS):
            item = board[row_index][col_index]
            freq[item] += 1
            if freq[item] != 1:
                print("not complete")
                return False

    for col_index in range(COLS): # s/b different
        freq = defaultdict(int)
        #print(f"check col {col_index}")
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

def check_inconsistency(board) -> bool:

    for row_index in range(ROWS):
        freq = defaultdict(int)
        for col_index in range(COLS):
            item = board.state[row_index][col_index]
            freq[item] += 1
        for key, value in freq.items():
            if key != 0 and value > 1:
                print(f"inconsistency in row: {row_index}: there are {value} number {key}")
                return True
    for col_index in range(COLS):
        freq = defaultdict(int)
        for row_index in range(ROWS):
            item = board.state[row_index][col_index]
            freq[item] += 1
        for key, value in freq.items():
            if key != 0 and value > 1:
                print(f"inconsistency in col: {col_index}: there are {value} number {key}")
                return True
    return False

def forward_pass(board) -> Board:
    find_options(board)
    change = False
    for row in range(ROWS):
        for col in range(COLS):
            options = board.options[row][col]
            
            # inconsistency
            if board.state[row][col] == 0 and len(options) == 0:
                for x in board.options:
                    print(x)
                for x in board.state:
                    print(x)
                print(f"inconsistency at {row},{col}")
                board.inconsistency = True
                return board

            if len(options) == 1:
#                print(f"changed {row} {col}")
                board.state[row][col] = board.options[row][col][0]
                board.options[row][col] = []
                print(f"changed {row} {col}")
                if check_inconsistency(board):
                    board.inconsistency = True
                    return board
                change = True
    if not change:
        print("no change made")
        board.no_match = True
        return board

    if is_solved(board.state):
        board.complete = True
    return board

board = Board(sudoku_hard)

def run_state(board) -> Board:
    complete = False
    while not complete:
        board = forward_pass(board)
        complete = board.complete

        if board.inconsistency:
            board.inconsistency = False
            if len(board.guesses) > 0:
                last_pos = board.guesses.pop()
                print(f"inconsistency: {last_pos.number} at {last_pos.row},{last_pos.col}")
                board.state = last_pos.state
                board.rejected = last_pos.rejected
                board.rejected[last_pos.row][last_pos.col].append(last_pos.number)
            else:
                board.no_match = True

        if board.no_match:
            for row in range(ROWS):
                for col in range(COLS):
                    if len(board.options[row][col]) == 0:
                        continue
                    for option in board.options[row][col]:
                        if option in board.rejected[row][col]:
                            continue
                        board.no_match = False
                        pos = Position(row, col, option, board.state, board.rejected)
                        board.state[row][col] = option
                        print(f"lets guess at {option} at {row},{col}")
                        board.guesses.append(pos)
                        board = run_state(board)
                        break
                if not board.no_match:
                    break
            if not board.no_match:
                break


            print("can't find a match")
            break
    return board

run_state(board)

for row in board.state:
    print(row)
