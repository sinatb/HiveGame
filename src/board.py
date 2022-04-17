from src.hex_place import HexPlace


class Board:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.places = [[HexPlace((x, y)) for x in range(self.n)] for y in range(self.m)]

    def get_neighbors(self, hex_place):
        return [self.pos_z_of(hex_place),
                self.pos_y_of(hex_place),
                self.pos_x_of(hex_place),
                self.neg_z_of(hex_place),
                self.neg_y_of(hex_place),
                self.neg_x_of(hex_place)]

    def get_empty_neighbors(self, hex_place):
        filtered = filter(lambda p: p.isEmpty(), self.get_neighbors(hex_place))
        return list(filtered)

    def pos_x_of(self, hex_place):
        i, j = hex_place.pos
        ii, jj = (i, j + 1)
        return self.places[ii][jj]

    def neg_x_of(self, hex_place):
        i, j = hex_place.pos
        ii, jj = (i, j - 1)
        return self.places[ii][jj]

    def pos_y_of(self, hex_place):
        i, j = hex_place.pos
        ii, jj = (i - 1, j) if i % 2 == 0 else (i - 1, j + 1)
        return self.places[ii][jj]

    def neg_y_of(self, hex_place):
        i, j = hex_place.pos
        ii, jj = (i + 1, j - 1) if i % 2 == 0 else (i + 1, j)
        return self.places[ii][jj]

    def pos_z_of(self, hex_place):
        i, j = hex_place.pos
        ii, jj = (i - 1, j - 1) if i % 2 == 0 else (i - 1, j)
        return self.places[ii][jj]

    def neg_z_of(self, hex_place):
        i, j = hex_place.pos
        ii, jj = (i + 1, j) if i % 2 == 0 else (i + 1, j + 1)
        return self.places[ii][jj]
