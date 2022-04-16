class Player:
    def __init__(self, num):
        self.pieces = {'Q': 1, 'A': 3, 'G': 3, 'C': 2, 'S': 2}
        self.num = num

    def place_piece(self, piece_name, board, i, j):
        if (self.pieces[piece_name] > 0):

            self.pieces[piece_name] -= 1
            board.set_piece(i, j, piece_name)
            board.places[i][j].player_num = self.num
            return True
        else:
            return False

    def add_piece(self, piece_name):
        self.pieces[piece_name] += 1

