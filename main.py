from gui import Window
from game import Game


if __name__ == "__main__":
    game = Game()
    window = Window(game)
    window.start()
