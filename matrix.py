import numpy as np

class CompatibilityError(Exception):
    pass

class Matrix:
    def __init__(self, row, col):
        if row == col == 1:
            raise TypeError("A scalar cannot be turned into a matrix")
        self.row = row
        self.col = col
        self.size = row * col
        self.matrix = np.zeros((self.row, self.col))

    def set(self, array):
        error = False if len(array) == len(self.matrix) and all(len(array[i]) == len(self.matrix[i]) for i in range(len(array))) else True
        if error:
            raise CompatibilityError("Provided array not compatible")
        for i in range(len(array)):
            for j in range(len(array[i])):
                self.matrix[i, j] = array[i][j]

    def __add__(self, other):
        error = False if self.row == other.row and self.col == other.col else True
        if error:
            raise CompatibilityError("Matrices cannot add together")
        result = Matrix(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                result.matrix[i, j] = self.matrix[i, j] + other.matrix[i, j]
        return result

    def __sub__(self, other):
        error = False if self.row == other.row and self.col == other.col else True
        if error:
            raise CompatibilityError("Matrices cannot subtract")
        result = Matrix(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                result.matrix[i, j] = self.matrix[i, j] - other.matrix[i, j]
        return result

    def __mul__(self, other):
        if self.col != other.row:
            raise CompatibilityError("Matrices cannot multiply")
        result = Matrix(self.row, other.col)
        for i in range(result.row):
            for j in range(result.col):
                for k in range(self.col):
                    result.matrix[i, j] += self.matrix[i, k] * other.matrix[k, j]
        return result

    def __rmul__(self, other):
            result = Matrix(self.row, self.col)
            for i in range(self.row):
                for j in range(self.col):
                    result.matrix[i, j] = other * self.matrix[i, j]
            return result

    def __pow__(self, other):
        if isinstance(other, int):
            result = Matrix(self.row, self.col)
            result += self
            for i in range(other - 1):
                result *= self
            return result
        else:
            return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Matrix):
            if self.row == other.row and self.col == other.row:
                for i in range(self.row):
                    for j in range(self.col):
                        if self.matrix[i, j] != other.matrix[i, j]:
                            return False
                return True
            else:
                return False
        return NotImplemented

    def wipeColumn(self, column):
        if self.col < column - 1:
            raise IndexError("Column out of range")
        result = Matrix(self.row, self.col - 1)
        for i in range(self.row):
            offset = 0
            for j in range(self.col):
                if j == column:
                    offset = -1
                else:
                    result.matrix[i, j + offset] = self.matrix[i, j]
        return result

    def wipeRow(self, row):
        if self.row < row - 1:
            raise IndexError("Row out of range")
        result = Matrix(self.row - 1, self.col)
        offset = 0
        for i in range(self.row):
            if i != row:
                for j in range(self.col):
                    result.matrix[i + offset, j] = self.matrix[i, j]
            else:
                offset = -1
        return result

    def wipeCross(self, row, column):
        return self.wipeColumn(column).wipeRow(row)

    def determinant(self):
        if not self.isSquare:
            raise ValueError("Determinant only possible with square matrices")
        if self.row == 2:
            det = self.matrix[0, 0] * self.matrix[1, 1] - self.matrix[0, 1] * self.matrix[1, 0]
            return round(det, 3) if round(det, 3) % 1 != 0 else round(det)
        else:
            det = 0
            for i in range(self.row):
                det += (-1)**i * self.matrix[i, 0] * self.wipeCross(i, 0).determinant()
            return round(det, 3) if round(det, 3) % 1 != 0 else round(det)

    def inverse(self):
        if self.row != self.col:
            raise ValueError("Inverse Matrices only possible with square matrices")
        if self.determinant() == 0:
            raise ValueError("The provided matrix does not have an Inverse")

        inverse = Matrix.identity(self.row)
        placeHolder = [[self.matrix[i, j] for j in range(self.col)] for i in range(self.row)]

        loop = 0
        while loop != self.row:
            repeat = False
            resolved = False
            if self.matrix[loop, loop] == 0:
                for row in range(self.row-loop-1):
                    if self.matrix[loop + row + 1, loop] != 0:
                        resolved = True
                        for col in range(self.col):
                            self.matrix[loop, col] += self.matrix[loop + row + 1, col]
                            inverse.matrix[loop, col] += inverse.matrix[loop + row + 1, col]
                        break
                if not resolved:
                    repeat = True
                    for row in range(loop):
                        loop -= 1
                        if self.matrix[loop - row - 1, loop] != 0:
                            for col in range(self.col):
                                self.matrix[loop, col] += self.matrix[loop - row - 1, col]
                                inverse.matrix[loop, col] += inverse.matrix[loop - row - 1, col]
                            break

            if not repeat:
                constant = self.matrix[loop, loop]
                for col in range(self.col):
                    self.matrix[loop, col] /= constant
                    inverse.matrix[loop, col] /= constant

                row = loop
                while row != 0:
                    constant = self.matrix[row-1, loop]
                    for col in range(self.col):
                        self.matrix[row-1, col] -= self.matrix[loop, col] * constant
                        inverse.matrix[row-1, col] -= inverse.matrix[loop, col] * constant
                    row -= 1

                row = loop
                while row != self.row - 1:
                    constant = self.matrix[row+1, loop]
                    for col in range(self.col):
                        self.matrix[row+1, col] -= self.matrix[loop, col] * constant
                        inverse.matrix[row+1, col] -= inverse.matrix[loop, col] * constant
                    row += 1

                loop += 1

        self.set(placeHolder)
        return inverse

    def reverse(self):
        reversed = Matrix(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                reversed.matrix[i, j] = self.matrix[i, self.col - (j+1)]
        return reversed

    def transpose(self):
        transposed = Matrix(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                transposed.matrix[i, j] = self.matrix[j, i]
        return transposed

    def isSquare(self):
        return self.row == self.col

    @classmethod
    def identity(cls, dimension):
        identity = cls(dimension, dimension)
        for i in range(dimension):
            identity.matrix[i, i] = 1
        return identity

    def __repr__(self):
        return "{}x{} Matrix Object".format(self.row, self.col)

    def __str__(self):
        text = ""
        for i in range(self.row):
            text += "|"
            for j in range(self.col):
                text += str(round(self.matrix[i, j], 3) if round(self.matrix[i, j], 2) % 1 != 0 else int(self.matrix[i, j])) + ("|" if j == self.col - 1 else "\t")
            text += "\n"
        return text