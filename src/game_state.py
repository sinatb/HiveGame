from constants import *
from board import Board
from player import Player
import agents


class GameState:
    def __init__(self, game_mode=PVP):
        self.game_mode = game_mode
        self.turn = 1
        self.selected_char = NO_PIECE
        self.moved_piece = NO_PIECE
        self.debugger_text = "Debugger"
        self.valid_moves = list()
        self.inspector_mode = False
        self.board = Board(22, 22)
        self.p1 = Player(1)
        self.p2 = Player(2)
        self.agent = agents.AlphaBetaAgent(DEFAULT_COEFFICIENTS)
        self.run_agent = self.agent.run
        self.agent_future = None
        self.previous_action = None

    def P1_FIRST_PLACE(self):
        return self.board(10, 11)

    def P2_FIRST_PLACE(self):
        return self.board.neg_z_of(self.P1_FIRST_PLACE())

    def has_to_enter_queen(self):
        return (self.turn == 7 and not self.p1.has_placed_queen()) or (
                self.turn == 8 and not self.p2.has_placed_queen()
        )

    def current_player(self):
        return current_player(self)


def is_ai_turn(gs):
    return (gs.game_mode == AI_AS_FIRST_PLAYER and player1_turn(gs)) or (
            gs.game_mode == AI_AS_SECOND_PLAYER and not player1_turn(gs))


def check_for_ai_turn(gs):
    if not is_ai_turn(gs) or game_status(gs) != ONGOING:
        return

    player = current_player(gs)
    future = gs.executor.submit(gs.run_agent, gs, player)

    def callback(_future):
        action = _future.result()
        apply_action(gs, action)
        gs.debugger_text = f'AI played {action}'

    future.add_done_callback(callback)
    gs.agent_future = future

    gs.debugger_text = 'AI is thinking...'


def player1_turn(gs):
    return gs.turn % 2 == 1


def current_player(gs):
    return gs.p1 if player1_turn(gs) else gs.p2


def game_status(gs):
    if not gs.p1.has_placed_queen() or not gs.p2.has_placed_queen():
        return ONGOING
    queen1_in_siege = len(gs.board.get_empty_neighbors(gs.board(*gs.p1.queen.pos))) == 0
    queen2_in_siege = len(gs.board.get_empty_neighbors(gs.board(*gs.p2.queen.pos))) == 0
    if not queen1_in_siege and not queen2_in_siege:
        return ONGOING
    elif queen1_in_siege and not queen2_in_siege:
        return PLAYER2_WIN
    elif not queen1_in_siege and queen2_in_siege:
        return PLAYER1_WIN
    else:
        return DRAW


def apply_action(state, action):
    # pop_action = (POP, (1, 1), (1, 2))
    # new_action = (NEW, QUEEN, (1, 1))

    player = current_player(state)
    state.turn += 1

    if action[0] == POP:
        assert state.board(*action[1]).top_piece.player == player.num

        top_piece = state.board(*action[1]).pop_top_piece()
        state.board(*action[2]).top_piece = top_piece
        return

    if action[0] == NEW:
        piece = player.get_free_piece(action[1])
        state.board(*action[2]).top_piece = piece
