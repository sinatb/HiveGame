import movement
import random
from state import from_game_state
import game_controller
from constants import *
import math


def random_agent(gs, player):
    initial_state = from_game_state(gs)
    legal_actions = movement.legal_actions_of(initial_state, player)
    return legal_actions[random.randrange(len(legal_actions))]


def alpha_beta_agent(gs, player):
    val, action = alpha_beta(from_game_state(gs), 4, -math.inf, math.inf, player.num, return_action=True)
    return action


def alpha_beta(node, depth, a, b, max_player_num, return_action=False):
    if depth == 0 or game_controller.game_status(node) != ONGOING:
        val = heuristic(node, max_player_num)
        return (val, None) if return_action else val

    player = node.current_player()
    legal_actions = movement.legal_actions_of(node, player)

    if len(legal_actions) == 0:
        if node.leading_actions[-1] == PASS_ACTION:
            print('What the hell')
            print(node.leading_actions)
            return heuristic(node, max_player_num)
        return alpha_beta(node.apply(PASS_ACTION), depth, a, b, max_player_num, return_action=return_action)

    if player.num == max_player_num:
        val = -math.inf
        max_action = None

        for action in legal_actions:
            child = node.apply(action)
            # val = max(val, alpha_beta(child, depth - 1, a, b, max_player_num))

            child_val = alpha_beta(child, depth - 1, a, b, max_player_num)
            if child_val >= val:
                val = child_val
                max_action = action

            if val >= b:
                break
            a = max(a, val)

        return (val, max_action) if return_action else val
    else:
        val = math.inf
        min_action = None

        for action in legal_actions:
            child = node.apply(action)
            # val = min(val, alpha_beta(child, depth - 1, a, b, max_player_num))

            child_val = alpha_beta(child, depth - 1, a, b, max_player_num)
            if child_val <= val:
                val = child_val
                min_action = action

            if val <= a:
                break
            b = min(b, val)

        return (val, min_action) if return_action else val


def heuristic(state, player_num, coefficients=None):
    status = game_controller.game_status(state)

    if status == DRAW:
        return 0.0

    if status != ONGOING:
        win = (player_num == 1 and status == PLAYER1_WIN) or (player_num == 2 and status == PLAYER2_WIN)
        return math.inf if win else -math.inf

    if coefficients is None:
        coefficients = (1, 2, 3, 1, 3, 2, 3)  # all positive

    a, b, c, d, e, f, g = coefficients

    own_player, enemy_player = (state.p1, state.p2) if player_num == 1 else (state.p2, state.p1)

    result = 0.0
    result += a * (n_onboard_pieces(state, own_player) - n_onboard_pieces(state, enemy_player))
    result += b * (n_pinned_pieces(state, enemy_player) - n_pinned_pieces(state, own_player))
    result += c * (float(is_queen_movable(state, own_player)) - float(is_queen_movable(state, enemy_player)))
    result += d * (n_accepting_edges(state, own_player) - n_accepting_edges(state, enemy_player))
    result += e * (n_free_ants(state, own_player) - n_free_ants(state, enemy_player))

    def qss(ec, enc):  # queen safety score
        return ec + f * enc

    result += g * (
            qss(*queen_neighbors_crawlability(state, own_player)) - qss(
        *queen_neighbors_crawlability(state, enemy_player))
    )
    return result


def count(predicate, iterable):
    result = 0
    for i in iterable:
        result += bool(predicate(i))
    return result


def n_free_ants(state, player):
    return count(
        lambda piece: piece.type == ANT and movement.is_movable(state.board, state.board(*piece.pos)),
        player.onboard_pieces())


def n_pinned_pieces(state, player):
    return count(
        lambda piece: not movement.is_movable(state.board, state.board(*piece.pos)),
        player.onboard_pieces())


def queen_neighbors_crawlability(state, player):
    if not player.has_placed_queen():
        return 3, 0

    empty_crawlable, empty_not_crawlable = 0, 0

    for hexplace in state.board.get_empty_neighbors(state.board(*player.queen.pos)):
        is_crawlable = any(map(
            movement.is_crawlable(state.board, hexplace),
            state.board.get_neighbors(hexplace)))

        empty_crawlable += is_crawlable
        empty_not_crawlable += not empty_not_crawlable

    return empty_crawlable, empty_not_crawlable


def n_accepting_edges(state, player):
    some_point_inside = next(player.onboard_pieces()).pos
    return (1 + n_ondeck_pieces(state, player) / 11) * count(
        lambda edge: movement.can_accept_new_piece(state.board, edge, player.num),
        movement.find_outer_edge(state.board, some_point_inside))


def n_onboard_pieces(state, player):
    return count(
        lambda x: True,
        player.onboard_pieces()
    )


def is_queen_movable(state, player):
    if not player.has_placed_queen():
        return True
    return movement.is_movable(state.board, state.board(*player.queen.pos))


def n_ondeck_pieces(state, player):
    result = 0
    for _, n in player.ondeck_pieces():
        result += n
    return result
