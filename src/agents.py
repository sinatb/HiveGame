import movement
import random
import state


def random_agent(gs, player):
    initial_state = state.from_game_state(gs)
    legal_actions = movement.legal_actions_of(initial_state, player)
    return legal_actions[random.randrange(len(legal_actions))]
