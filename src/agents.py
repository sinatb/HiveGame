import movement
import random
from state import from_game_state
import game_controller
from constants import *
import math
import time


def random_agent(gs, player):
    initial_state = from_game_state(gs)
    legal_actions = movement.legal_actions_of(initial_state, player)
    return legal_actions[random.randrange(len(legal_actions))]


class AlphaBetaAgent:
    def __init__(self, coefficients):
        self.coefficients = coefficients
        self.root = None
        self.previous_action = None

    def run(self, gs, player):
        print('AI turn:')
        s = time.time()
        val, action = self.alpha_beta(from_game_state(gs), 4, -math.inf, math.inf, player.num, return_action=True)
        print(f'found move in {round(time.time() - s, 1)}s')
        print()
        return action

    def alpha_beta(self, node, depth, a, b, max_player_num, return_action=False):
        if depth == 0 or game_controller.game_status(node) != ONGOING:
            val = self.heuristic(node, max_player_num)
            return (val, None) if return_action else val

        player = node.current_player()
        maximizing = player.num == max_player_num

        action_children = node.children.items()
        if not node.children:
            legal_actions = movement.legal_actions_of(node, player)
            if len(legal_actions) == 0:
                return self.alpha_beta(node.apply(PASS_ACTION), depth, a, b, max_player_num,
                                       return_action=return_action)

            self.reduce_actions(node, legal_actions, player)
            action_children = zip(legal_actions, map(node.apply, legal_actions))

        val = -math.inf if maximizing else math.inf
        minmax_action = None

        for action, child in action_children:
            child = node.apply(action)
            # val = max(val, alpha_beta(child, depth - 1, a, b, max_player_num))

            child_val = self.alpha_beta(child, depth - 1, a, b, max_player_num)
            if (maximizing and child_val >= val) or (not maximizing and child_val <= val):
                val = child_val
                minmax_action = action

            if (maximizing and val >= b) or (not maximizing and val <= a):
                break
                
            if maximizing:
                a = max(a, val)
            else:
                b = min(b, val)

        return (val, minmax_action) if return_action else val

    def heuristic(self, state, player_num):
        status = game_controller.game_status(state)

        if status == DRAW:
            return 0.0

        if status != ONGOING:
            win = (player_num == 1 and status == PLAYER1_WIN) or (player_num == 2 and status == PLAYER2_WIN)
            return math.inf if win else -math.inf

        a, b, c, d, e, f, g = self.coefficients

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

    def reduce_actions(self, state, actions, player):
        old_len = len(actions)
        new_ant_limit = 3
        new_ant_count = 0
        pop_ant_count = 0
        pop_ant_removed = 0
        i = 0
        while i < len(actions):
            a = actions[i]
            if a[0] == NEW and a[1] == ANT:
                new_ant_count += 1
                if new_ant_count > new_ant_limit:
                    del actions[i]
                    i -= 1
            elif a[0] == POP and state.board(*a[1]).top_piece.type == ANT:
                pop_ant_count += 1
                old_h = self.heuristic(state, player.num)
                new_h = self.heuristic(state.apply(a, add_to_children=False), player.num)

                if new_h - old_h < 1.5:
                    pop_ant_removed += 1
                    del actions[i]
                    i -= 1
            i += 1

        rc = old_len - len(actions)
        if rc > 0:
            print(f'\treduction count: {rc}. pop ant stats: {pop_ant_removed}/{pop_ant_count}')


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
