import movement
import random


def random_agent(gs, player):
    legal_actions = movement.legal_actions_of(gs, player)
    return legal_actions[random.randrange(len(legal_actions))]
