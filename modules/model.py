class Matrix(list):
    def __init__(self, m, n):
        super().__init__([0 for j in range(n)] for i in range(m))


class Model():
    def __init__(self):
        self.board = Matrix(3, 3)
