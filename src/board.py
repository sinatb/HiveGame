from src.hex_place import HexPlace


class Board:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.places = [[0 for x in range(self.n)] for y in range(self.m)]

    def get_neighbor(self, i, j):
        if (i % 2 == 0):
            return ["U" if i - 1 < 0 else self.places[i - 1][j - 1].piece,
                    "U" if i - 1 < 0 else self.places[i - 1][j].piece,
                    "U" if j + 1 > self.m - 1 else self.places[i][j + 1].piece,
                    "U" if i + 1 > self.n - 1 else self.places[i + 1][j].piece,
                    "U" if j - 1 < 0 else self.places[i + 1][j - 1].piece,
                    "U" if j - 1 < 0 else self.places[i][j - 1].piece]
        else:
            return ["U" if i - 1 < 0 else self.places[i - 1][j].piece,
                    "U" if (i - 1 < 0 or j + 1 > self.m - 1) else self.places[i - 1][j + 1].piece,
                    "U" if j + 1 > self.m - 1 else self.places[i][j + 1].piece,
                    "U" if (i + 1 > self.n - 1 or j + 1 > self.m - 1) else self.places[i + 1][j + 1].piece,
                    "U" if (j - 1 < 0 or i + 1 > self.m - 1) else self.places[i + 1][j].piece,
                    "U" if j - 1 < 0 else self.places[i][j - 1].piece]

    def set_piece(self, i, j, p):
        self.places[i][j].piece = p

    def draw(self):
        for i in range(0, self.n):
            for j in range(0, self.m):
                self.places[i][j] = HexPlace()

    def print_board(self):
        for i in range(0, self.n):
            print("")
            for j in range(0, self.m):
                print(self.places[i][j].piece, end=" ")


