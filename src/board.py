from src.hex_place import HexPlace


class Board:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.places = [[HexPlace((y, x)) for x in range(self.n)] for y in range(self.m)]

    def get_neighbors(self, hex_place):
        return list(filter(None, [self.pos_z_of(hex_place),
                                  self.pos_y_of(hex_place),
                                  self.pos_x_of(hex_place),
                                  self.neg_z_of(hex_place),
                                  self.neg_y_of(hex_place),
                                  self.neg_x_of(hex_place)]))

    def get_empty_neighbors(self, hex_place):
        filtered = filter(lambda p: p.isEmpty(), self.get_neighbors(hex_place))
        return list(filtered)

    def get_full_neighbors(self, hex_place):
        filtered = filter(lambda p: p.isNotEmpty(), self.get_neighbors(hex_place))
        return list(filtered)

    def pos_x_of(self, hex_place):
        i, j = hex_place.pos
        ii, jj = (i, j + 1)
        return self.places[ii][jj] if self.in_range(ii, jj) else None

    def neg_x_of(self, hex_place):
        i, j = hex_place.pos
        ii, jj = (i, j - 1)
        return self.places[ii][jj] if self.in_range(ii, jj) else None

    def pos_y_of(self, hex_place):
        i, j = hex_place.pos
        ii, jj = (i - 1, j) if i % 2 == 1 else (i - 1, j + 1)
        return self.places[ii][jj] if self.in_range(ii, jj) else None

    def neg_y_of(self, hex_place):
        i, j = hex_place.pos
        ii, jj = (i + 1, j - 1) if i % 2 == 1 else (i + 1, j)
        return self.places[ii][jj] if self.in_range(ii, jj) else None

    def pos_z_of(self, hex_place):
        i, j = hex_place.pos
        ii, jj = (i - 1, j - 1) if i % 2 == 1 else (i - 1, j)
        return self.places[ii][jj] if self.in_range(ii, jj) else None

    def neg_z_of(self, hex_place):
        i, j = hex_place.pos
        ii, jj = (i + 1, j) if i % 2 == 1 else (i + 1, j + 1)
        return self.places[ii][jj] if self.in_range(ii, jj) else None

    def in_range(self, i, j):
        return 0 <= i < self.m and 0 <= j < self.n
