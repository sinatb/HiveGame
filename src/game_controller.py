import pygame
import movement
import gui
from game_state import *


def handle_event(gs, event):
    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    if is_ai_turn(gs):
        return

    pos = event.pos

    if pos in gui.INSPECTOR_MODE_BUTTON:
        gs.inspector_mode = not gs.inspector_mode

    elif gs.inspector_mode:
        handle_inspector_mode(gs, pos)

    elif pos in gui.PLAYER1_DECK:
        handle_p1_deck_click(gs, pos)

    elif pos in gui.PLAYER2_DECK:
        handle_p2_deck_click(gs, pos)

    elif pos in gui.BOARD_HITBOX:
        handle_board_click(gs, pos)

    elif pos in gui.PASS_TURN:
        if gs.turn <= 8:
            gs.debugger_text = 'Cannot change turn this early'
        else:
            gs.turn += 1
            gs.debugger_text = 'Turn changed'
            check_for_ai_turn(gs)
            gs.previous_action = PASS_ACTION
            print(f'User played {gs.previous_action}')


def handle_board_click(gs, pos):
    i, j = gui.extract_board_i_j(*pos)

    if not gs.board.in_range(i, j):
        return

    if (gs.board(i, j).isEmpty() or (gs.moved_piece != NO_PIECE and gs.moved_piece.type == COCKROACH)) and (
            gs.selected_char != NO_PIECE or gs.moved_piece != NO_PIECE):

        if gs.selected_char == NO_PIECE and gs.moved_piece != NO_PIECE:
            if gs.board(i, j) in gs.valid_moves:
                old_pos = gs.moved_piece.pos
                gs.board(i, j).top_piece = gs.moved_piece
                gs.debugger_text = PLACED
                gs.moved_piece = NO_PIECE
                gs.valid_moves = list()
                gs.previous_action = (POP, old_pos, (i, j))
                print(f'User played {gs.previous_action}')
            else:
                gs.debugger_text = 'This move is illegal'
        elif gs.selected_char != NO_PIECE and gs.moved_piece == NO_PIECE:
            if not current_player(gs).has_free_piece(gs.selected_char):
                gs.debugger_text = 'There is no such piece left'
                gs.selected_char = NO_PIECE
            elif gs.turn <= 2 and not gs.board(i, j) in gs.valid_moves:
                gs.debugger_text = 'Your first move has to be at the marked place'
            elif gs.turn > 2 and not movement.can_accept_new_piece(gs.board, gs.board(i, j),
                                                                   current_player(gs).num):
                gs.debugger_text = 'A new piece cannot be placed here'
            else:
                gs.board(i, j).top_piece = current_player(gs).get_free_piece(gs.selected_char)
                gs.previous_action = (NEW, gs.selected_char, (i, j))
                print(f'User played {gs.previous_action}')
                gs.debugger_text = PLACED
                gs.selected_char = NO_PIECE
                if gs.turn <= 2:
                    gs.valid_moves = list()

        if gs.debugger_text == PLACED:
            gs.turn += 1
            check_for_ai_turn(gs)
    elif gs.board(i, j).isNotEmpty() and gs.selected_char == NO_PIECE and gs.moved_piece == NO_PIECE:
        if not current_player(gs).num == gs.board(i, j).top_piece.player:
            gs.debugger_text = "Choose your own piece"
        elif not current_player(gs).has_placed_queen():
            gs.debugger_text = 'You cannot move any piece until queen is placed'
        else:
            place = gs.board(i, j)
            gs.valid_moves = movement.valid_moves_of(gs.board, place, place.top_piece.type, should_pop=True)
            if len(gs.valid_moves) <= 0:
                gs.debugger_text = 'This piece has no legal moves'
            else:
                gs.moved_piece = place.pop_top_piece()
                gs.debugger_text = "Moving piece"
    else:
        if gs.board(i, j).isNotEmpty():
            gs.debugger_text = "The place has already been taken"
            gs.selected_char = NO_PIECE
        else:
            print(i, j)
            gs.debugger_text = "Please select a piece"


def handle_p2_deck_click(gs, pos):
    if player1_turn(gs):
        gs.debugger_text = "You can't chose from player 2's pieces"
    else:
        i, j = gui.extract_p2_deck_i_j(*pos)
        if i == 0:
            if gs.has_to_enter_queen() and ALL_PIECES[j] != QUEEN:
                gs.debugger_text = 'You have to place your queen at this turn'
            else:
                gs.selected_char = ALL_PIECES[j]
                if gs.turn == 2:
                    gs.valid_moves = [gs.P2_FIRST_PLACE()]
                gs.debugger_text = "Player 2 has chosen " + gs.selected_char
        else:
            gs.debugger_text = "Choose valid Piece"


def handle_p1_deck_click(gs, pos):
    if not player1_turn(gs):
        gs.debugger_text = "You can't chose from player 1's pieces"
    else:
        i, j = gui.extract_p1_deck_i_j(*pos)
        if i == 0:
            if gs.has_to_enter_queen() and ALL_PIECES[j] != QUEEN:
                gs.debugger_text = 'You have to place your queen at this turn'
            else:
                gs.selected_char = ALL_PIECES[j]
                if gs.turn == 1:
                    gs.valid_moves = [gs.P1_FIRST_PLACE()]
                gs.debugger_text = "Player 1 has chosen " + gs.selected_char
        else:
            gs.debugger_text = "Chose valid Piece"


def handle_inspector_mode(gs, pos):
    if pos not in gui.BOARD_HITBOX:
        return
    i, j = gui.extract_board_i_j(*pos)
    if gs.board.in_range(i, j) and gs.board(i, j).isNotEmpty():
        gs.debugger_text = gs.board(i, j).stack_string()
