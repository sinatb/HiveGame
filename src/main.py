import gui
from src.game_controller import GameState


def main():
    running = True
    gs = GameState()
    gui.draw_field(gs)

    # game loop
    while running:
        running = gui.tick(gs)


if __name__ == "__main__":
    main()
