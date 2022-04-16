from src.hex_place import HexPlace


class Board:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.places = [[HexPlace((x, y)) for x in range(self.n)] for y in range(self.m)]

    def get_neighbors(self, hex_place):
        i, j = hex_place.pos
        if i % 2 == 0:
            return [self.places[i - 1][j - 1],
                    self.places[i - 1][j],
                    self.places[i][j + 1],
                    self.places[i + 1][j],
                    self.places[i + 1][j - 1],
                    self.places[i][j - 1]]
        else:
            return [self.places[i - 1][j],
                    self.places[i - 1][j + 1],
                    self.places[i][j + 1],
                    self.places[i + 1][j + 1],
                    self.places[i + 1][j],
                    self.places[i][j - 1]]

