from constants import *
from src.piece import Piece


class Player:
    def __init__(self, num):
        self.num = num
        self._pieces = {QUEEN: [Piece(QUEEN, self.num)],
                        ANT: [Piece(ANT, self.num) for _ in range(3)],
                        GRASSHOPPER: [Piece(GRASSHOPPER, self.num) for _ in range(3)],
                        COCKROACH: [Piece(COCKROACH, self.num) for _ in range(2)],
                        SPIDER: [Piece(SPIDER, self.num) for _ in range(2)]
                        }

    def has_free_piece(self, piece_name):
        return self.get_free_piece_count(piece_name) > 0

    def get_free_piece(self, piece_name):
        return self._pieces[piece_name].pop()

    def get_free_piece_count(self, piece_name):
        return len(self._pieces[piece_name])
