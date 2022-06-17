import movement
import random
import state
import game_controller
from constants import *
import math


def random_agent(gs, player):
    initial_state = state.from_game_state(gs)
    legal_actions = movement.legal_actions_of(initial_state, player)
    return legal_actions[random.randrange(len(legal_actions))]


def alpha_beta_agent(gs, player):
    val, action = alpha_beta(state.from_game_state(gs), 5, -math.inf, math.inf, player.num, return_action=True)
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


def heuristic(s, player_num):
    status = game_controller.game_status(s)
    if status == DRAW or status == ONGOING:
        return 0.0

    win = (player_num == 1 and status == PLAYER1_WIN) or (player_num == 2 and status == PLAYER2_WIN)
    return math.inf if win else -math.inf
