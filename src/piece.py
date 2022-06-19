class Piece:
    def __init__(self, piece_type, player):
        self.type = piece_type
        self.player = player
        self.pos = None

    def __str__(self):
        return f'({self.type}, {self.player}, {self.pos})'

    def __repr__(self):
        return str(self)
