from tkinter import Tk, Canvas
from random import randint

import sys
from typing import List

from game import Game
from settings import *


class Window:
    def __init__(self, game: Game = None) -> None:
        super().__init__()

        self.master = Tk()
        self.board = Canvas(
            self.master,
            width=GRID_SIZE_X * GRID_WIDTH + 4,
            height=GRID_SIZE_Y * GRID_WIDTH + 4,
        )
        self.grid_width = 20 * GRID_WIDTH
        self.score_board = Canvas(
            self.master,
            width=self.grid_width,
            height=GRID_SIZE_Y * GRID_WIDTH,
        )

        self.board.grid(row=0, column=0, padx=(2, 0), pady=(2, 0))
        self.score_board.grid(row=0, column=1)

        self.bind_events()
        self.render_grid()
        self.run = False
        self.game = game
        self.loop()

    def close(self, event):
        self.master.withdraw()  # if you want to bring it back
        sys.exit()  # if you want to exit the entire thing

    def toggle(self, event):
        if not self.run:
            self.run = True
        else:
            self.run = False

    def bind_events(self):
        self.master.bind('<Escape>', self.close)
        self.master.bind('<Return>', self.toggle)

    @staticmethod
    def handle_color(color):
        if type(color) == tuple:
            color = "#%02x%02x%02x" % color
        return color

    def render_tile(
            self, x: int, y: int,
            shape=Shape.RECTANGLE, color="white", width=1, margin=0, tag=None, outline=None, **_):
        color = self.handle_color(color)

        delta = 2
        if shape == Shape.RECTANGLE:
            self.board.create_rectangle(
                (x + margin) * GRID_WIDTH + delta,
                (y + margin) * GRID_WIDTH + delta,
                (x + 1 - margin) * GRID_WIDTH + delta,
                (y + 1 - margin) * GRID_WIDTH + delta,
                fill=color,
                width=width,
                tag=tag,
                outline=outline,
            )

        if shape == Shape.CIRCLE:
            self.board.create_oval(
                (x + margin) * GRID_WIDTH + delta,
                (y + margin) * GRID_WIDTH + delta,
                (x + 1 - margin) * GRID_WIDTH + delta,
                (y + 1 - margin) * GRID_WIDTH + delta,
                fill=color,
            )

    def render_scores(self, players):
        players = sorted(players, reverse=True, key=lambda p: p['score'])
        for row, player in enumerate(players):
            string = "{} {}:  {}   {:.0f}%".format(
                row + 1,
                player['name'][:16],
                player['score'],
                player['score'] / (player['cost'] or 1) * 100,
            )

            row_y = 16 + (GRID_WIDTH // 0.8) * row

            self.score_board.create_text(
                self.grid_width / 2 + GRID_WIDTH, row_y, text=string, font="Times %s bold" % GRID_WIDTH)
            self.score_board.create_oval(
                2,
                row_y - GRID_WIDTH // 2,
                2 + GRID_WIDTH,
                row_y + GRID_WIDTH // 2,
                fill=self.handle_color(player['color']),
            )

    def render(self, tiles: List[dict] = None, players: List[dict] = None) -> None:
        self.render_grid()

        for item in tiles or []:
            self.render_tile(**item)

        self.render_scores(players or [])

    def render_grid(self) -> None:
        for x in range(GRID_SIZE_X):
            for y in range(GRID_SIZE_Y):
                self.render_tile(x, y)

    def delayed_render(self):
        self.game.receive()
        self.board.delete("all")
        self.score_board.delete("all")
        self.render(*self.game.render())
        self.loop()

    def loop(self):
        if not self.game:
            print("no game")
        elif self.run:
            self.game.send()
            self.master.after(LOOP_DELAY, self.delayed_render)
            return
        else:
            self.game.ping()
            self.master.after(LOOP_DELAY, self.loop)

    def start(self):
        self.render_grid()
        if self.game:
            self.render(*self.game.render())
        self.master.mainloop()


# wrap into a function to clean the global namespace
def main():
    from color_picker import ColorChoice

    walls = {
        (randint(0, GRID_SIZE_X - 1), randint(0, GRID_SIZE_Y - 1))
        for _ in range(GRID_SIZE_X * GRID_SIZE_Y // 6)
    }
    walls.discard((0, 0))

    color_picker = ColorChoice(list(colors.values()))

    walls = [
        dict(x=x, y=y, color=color_picker.get())
        for x, y in walls
    ]

    players = [
        dict(x=0, y=0, color=(0, 100, 100), margin=0.2, score=1, cost=10, name="Test", shape=Shape.CIRCLE)
    ]

    window = Window()
    window.render(walls + players, players)
    window.master.mainloop()


if __name__ == '__main__':
    main()
