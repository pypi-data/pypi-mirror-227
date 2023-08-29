class SudokuValidator:
    def __init__(self, board):
        self.board = board

    def is_valid(self):
        if len(self.board) != 9:
            return False

        for row in self.board:
            if len(row) != 9:
                return False

        for i in range(9):
            if not self.is_valid_row(i) or not self.is_valid_column(i) or not self.is_valid_subgrid(i):
                return False

        return True

    def is_valid_row(self, row):
        nums = set()
        for num in self.board[row]:
            if num in nums or not 1 <= num <= 9:
                return False
            nums.add(num)
        return True

    def is_valid_column(self, col):
        nums = set()
        for row in self.board:
            num = row[col]
            if num in nums or not 1 <= num <= 9:
                return False
            nums.add(num)
        return True

    def is_valid_subgrid(self, subgrid):
        nums = set()
        start_row = (subgrid // 3) * 3
        start_col = (subgrid % 3) * 3

        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                num = self.board[i][j]
                if num in nums or not 1 <= num <= 9:
                    return False
                nums.add(num)
        return True

# Ejemplo de uso
sudoku_board = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
]

def cargar_un_numero(posicion_x, posicion_y, numero):
    if type(posicion_x) != int:
        raise Exception("posicion_x debe ser un entero")
    if type(posicion_y) != int:
        raise Exception("posicion_y debe ser un entero")
    if type(numero) != int:
        raise Exception("El numero debe ser un entero")
    if posicion_x < 1 or posicion_x > 9:
        raise Exception("posicion_x debe estar entre 1 y 9")
    if posicion_y < 1 or posicion_y > 9:
        raise Exception("posicion_y debe estar entre 1 y 9")
    sudoku_board[posicion_x-1][posicion_y-1] = numero

def reset_board():
    for i in range(9):
        for j in range(9):
            sudoku_board[i][j] = -1

def chequear_sudoku():
    for i in range(9):
        for j in range(9):
            if sudoku_board[i][j] == -1:
                raise Exception("no se han cargado todos los numeros")
    validator = SudokuValidator(sudoku_board)
    response = validator.is_valid()
    reset_board()
    return response
