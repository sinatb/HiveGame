from constants import *
from src.piece import Piece


class Player:
    def __init__(self, num):
        self.num = num
        self.queen = Piece(QUEEN, self.num)
        self._pieces = {QUEEN: [self.queen],
                        ANT: [Piece(ANT, self.num) for _ in range(3)],
                        GRASSHOPPER: [Piece(GRASSHOPPER, self.num) for _ in range(3)],
                        COCKROACH: [Piece(COCKROACH, self.num) for _ in range(2)],
                        SPIDER: [Piece(SPIDER, self.num) for _ in range(2)]
                        }
        self._onboard = []

    def has_free_piece(self, piece_name):
        return self.get_free_piece_count(piece_name) > 0

    def get_free_piece(self, piece_name):
        piece = self._pieces[piece_name].pop()
        self._onboard.append(piece)
        return piece

    def get_free_piece_count(self, piece_name):
        return len(self._pieces[piece_name])

    def has_placed_queen(self):
        return self.get_free_piece_count(QUEEN) == 0

    def onboard_pieces(self):
        return iter(self._onboard)

    def ondeck_pieces(self):
        return map(lambda kv: (kv[0], len(kv[1])), self._pieces.items())
