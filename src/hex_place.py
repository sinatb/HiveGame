
class HexPlace:
    def __init__(self, pos, pieces=None):
        self.pos = pos
        self._pieces = pieces if pieces is not None else []
        for p in self._pieces:
            p.pos = self.pos

    def _get_top_piece(self):
        return self._pieces[-1]

    def _set_top_piece(self, piece):
        piece.pos = self.pos
        self._pieces.append(piece)

    def pop_top_piece(self):
        return self._pieces.pop()

    def isEmpty(self):
        return len(self._pieces) <= 0

    def isNotEmpty(self):
        return not self.isEmpty()

    top_piece = property(_get_top_piece, _set_top_piece)

    def stack_string(self):
        return str.join(' ', map(lambda piece: f'{piece.type}({piece.player})', self._pieces))

    def stack(self):
        return iter(self._pieces)
