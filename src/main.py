import gui
from src.game_controller import GameState
import concurrent.futures


def main():
    running = True
    gs = GameState()
    gui.draw_field(gs)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        gs.executor = executor
        # game loop
        while running:
            running = gui.tick(gs)


if __name__ == "__main__":
    main()
