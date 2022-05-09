import pygame
import math
from constants import *
from board import Board
from player import Player
import movement
from src import gui


class GameState:
    def __init__(self):
        self.turn = 1
        self.selected_char = NO_PIECE
        self.moved_piece = NO_PIECE
        self.debugger_text = "Debugger"
        self.valid_moves = list()
        self.inspector_mode = False
        self.board = Board(22, 22)
        self.p1 = Player(1)
        self.p2 = Player(2)

    def P1_FIRST_PLACE(self):
        return self.board.places[10][11]

    def P2_FIRST_PLACE(self):
        return self.board.neg_z_of(self.P1_FIRST_PLACE())


def player1_turn(gs):
    return gs.turn % 2 == 1


def current_player(gs):
    return gs.p1 if player1_turn(gs) else gs.p2


def game_status(gs):
    if not gs.p1.has_placed_queen() or not gs.p2.has_placed_queen():
        return ONGOING
    ii, jj = gs.p1.queen.pos
    queen1_in_siege = len(gs.board.get_empty_neighbors(gs.board.places[ii][jj])) == 0
    ii, jj = gs.p2.queen.pos
    queen2_in_siege = len(gs.board.get_empty_neighbors(gs.board.places[ii][jj])) == 0
    if not queen1_in_siege and not queen2_in_siege:
        return ONGOING
    elif queen1_in_siege and not queen2_in_siege:
        return PLAYER2_WIN
    elif not queen1_in_siege and queen2_in_siege:
        return PLAYER1_WIN
    else:
        return DRAW


def handle_event(gs, event):
    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    (x, y) = event.pos
    print(f'Clicked on ({x}, {y})')

    if SCREEN_WIDTH - 100 < x < SCREEN_WIDTH and SCREEN_HEIGHT - 100 < y < SCREEN_HEIGHT:
        gs.inspector_mode = not gs.inspector_mode
    if not gs.inspector_mode:
        if (950 < x < SCREEN_WIDTH) and (0 < y < SCREEN_HEIGHT / 2):
            if not player1_turn(gs):
                gs.debugger_text = "You can't chose from player 1's pieces"
            else:
                i = math.floor((y - 40) / 47)
                j = math.floor((x - 950) / 50)
                if i == 0:
                    if gs.turn == 7 and ALL_PIECES[j] != QUEEN and not gs.p1.has_placed_queen():
                        gs.debugger_text = 'You have to place your queen at this turn'
                    else:
                        gs.selected_char = ALL_PIECES[j]
                        if gs.turn == 1:
                            gs.valid_moves = [gs.P1_FIRST_PLACE()]
                        gs.debugger_text = "Player 1 has chosen " + gs.selected_char
                else:
                    gs.debugger_text = "Chose valid Piece"

        elif (950 < x < SCREEN_WIDTH) and (SCREEN_HEIGHT / 2 < y < SCREEN_HEIGHT):
            if player1_turn(gs):
                gs.debugger_text = "You can't chose from player 2's pieces"
            else:
                i = math.floor((y - 440) / 47)
                j = math.floor((x - 950) / 50)
                if i == 0:
                    if gs.turn == 8 and ALL_PIECES[j] != QUEEN and not gs.p2.has_placed_queen():
                        gs.debugger_text = 'You have to place your queen at this turn'
                    else:
                        gs.selected_char = ALL_PIECES[j]
                        if gs.turn == 2:
                            gs.valid_moves = [gs.P2_FIRST_PLACE()]
                        gs.debugger_text = "Player 2 has chosen " + gs.selected_char
                else:
                    gs.debugger_text = "Choose valid Piece"

        elif (0 < x < 950) and (0 < y < 750):
            i = math.floor(y / 32)
            j = math.floor((x - 35 + (0 if (i % 2 == 0) else 20)) / 40)
            if (0 <= j < 22 and (gs.board.places[i][j].isEmpty() or (
                    gs.moved_piece != NO_PIECE and gs.moved_piece.type == COCKROACH)) and
                    (gs.selected_char != NO_PIECE or gs.moved_piece != NO_PIECE)):

                if gs.selected_char == NO_PIECE and gs.moved_piece != NO_PIECE:
                    if gs.board.places[i][j] in gs.valid_moves:
                        gs.board.places[i][j].top_piece = gs.moved_piece
                        gs.debugger_text = PLACED
                        gs.moved_piece = NO_PIECE
                        gs.valid_moves = list()
                    else:
                        gs.debugger_text = 'This move is illegal'
                elif gs.selected_char != NO_PIECE and gs.moved_piece == NO_PIECE:
                    if not current_player(gs).has_free_piece(gs.selected_char):
                        gs.debugger_text = 'There is no such piece left'
                        gs.selected_char = NO_PIECE
                    elif gs.turn <= 2 and not gs.board.places[i][j] in gs.valid_moves:
                        gs.debugger_text = 'Your first move has to be at the marked place'
                    elif gs.turn > 2 and not movement.can_accept_new_piece(gs.board, gs.board.places[i][j],
                                                                           current_player(gs).num):
                        gs.debugger_text = 'A new piece cannot be placed here'
                    else:
                        gs.board.places[i][j].top_piece = current_player(gs).get_free_piece(gs.selected_char)
                        gs.debugger_text = PLACED
                        gs.selected_char = NO_PIECE
                        if gs.turn <= 2:
                            gs.valid_moves = list()

                gs.turn += 1 if (gs.debugger_text == PLACED) else 0
            elif gs.board.places[i][j].isNotEmpty() and gs.selected_char == NO_PIECE and gs.moved_piece == NO_PIECE:
                if not current_player(gs).num == gs.board.places[i][j].top_piece.player:
                    gs.debugger_text = "Choose your own piece"
                elif not current_player(gs).has_placed_queen():
                    gs.debugger_text = 'You cannot move any piece until queen is placed'
                else:
                    place = gs.board.places[i][j]
                    gs.valid_moves = movement.valid_moves_of(gs.board, place, place.top_piece.type, should_pop=True)
                    if len(gs.valid_moves) <= 0:
                        gs.debugger_text = 'This piece has no legal moves'
                    else:
                        gs.moved_piece = place.pop_top_piece()
                        gs.debugger_text = "Moving piece"
            else:
                if gs.board.places[i][j].isNotEmpty():
                    gs.debugger_text = "The place has already been taken"
                    gs.selected_char = NO_PIECE
                else:
                    print(i, j)
                    gs.debugger_text = "Please select a piece"
        elif 810 < x < 940 and 760 < y < 785:
            if gs.turn <= 8:
                gs.debugger_text = 'Cannot change turn this early'
            else:
                gs.turn += 1
                gs.debugger_text = 'Turn changed'
    else:
        if (0 < x < 950) and (0 < y < 750):
            i = math.floor(y / 32)
            j = math.floor((x - 35 + (0 if (i % 2 == 0) else 20)) / 40)
            if 0 <= j < 22 and gs.board.places[i][j].isNotEmpty():
                gs.debugger_text = gs.board.places[i][j].stack_string()

    gui.draw_field(gs)
