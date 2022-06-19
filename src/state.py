from board import Board
from hex_place import HexPlace
from player import Player
import game_controller


class LazyBoard(Board):

    # noinspection PyMissingConstructor
    def __init__(self, n, m, player1, player2, not_empty_places):
        self.n = n
        self.m = m
        self._place_of = dict()

        for hexplace in not_empty_places:
            pieces = []

            for piece in hexplace.stack():
                if piece.player == 1:
                    pieces.append(player1.get_free_piece(piece.type))
                else:
                    pieces.append(player2.get_free_piece(piece.type))

            new_hex_place = HexPlace(hexplace.pos, pieces=pieces)
            self._place_of[new_hex_place.pos] = new_hex_place

    def __call__(self, *args):
        pos = args[0], args[1]
        
        if not self.in_range(*pos):
            return None

        if pos not in self._place_of:
            self._place_of[pos] = HexPlace(pos)

        return self._place_of[pos]

    def not_empty_places(self):
        return list(filter(HexPlace.isNotEmpty, self._place_of.values()))


class State:
    def __init__(self, n, m, not_empty_places, turn, p1_first_pos, p2_first_pos):
        self.turn = turn
        self.p1 = Player(1)
        self.p2 = Player(2)
        self.leading_actions = []
        self._P1_FIRST_POS = p1_first_pos
        self._P2_FIRST_POS = p2_first_pos
        self.board = LazyBoard(n, m, self.p1, self.p2, not_empty_places)

    def has_to_enter_queen(self):
        return (self.turn == 7 and not self.p1.has_placed_queen()) or (
                self.turn == 8 and not self.p2.has_placed_queen()
        )

    def P1_FIRST_PLACE(self):
        return self.board(*self._P1_FIRST_POS)

    def P2_FIRST_PLACE(self):
        return self.board(*self._P2_FIRST_POS)

    def apply(self, action, clone=True):
        result = self.clone() if clone else self
        game_controller.apply_action(result, action)
        result.leading_actions = self.leading_actions + [action]
        return result

    def clone(self):
        return State(
            self.board.n,
            self.board.m,
            self.board.not_empty_places(),
            self.turn,
            self._P1_FIRST_POS,
            self._P2_FIRST_POS
        )

    def current_player(self):
        return game_controller.current_player(self)

    def print(self):
        print(f'turn: {self.turn}')
        for hexplace in self.board.not_empty_places():
            print(f'{hexplace.pos}: {list(hexplace.stack())}')
        for player in [self.p1, self.p2]:
            print(f'Player {player.num}')
            print(player._pieces)
            print()


def from_game_state(gs):
    return State(
        gs.board.n,
        gs.board.m,
        gs.board.not_empty_places(),
        gs.turn,
        gs.P1_FIRST_PLACE().pos,
        gs.P2_FIRST_PLACE().pos
    )
