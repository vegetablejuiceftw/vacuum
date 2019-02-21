from random import randint, choice

from agent import Agent, Point


class RandomPreferLastMoveAgent(Agent):
    NAME = "LastMove"
    AUTHOR = "last.move@thorgate.eu"

    def __init__(self) -> None:
        super().__init__()
        self.last_move = self.ACTION.RIGHT
        self.last_spot = None

    def step(self, perception: Point) -> str:
        pos = perception.uuid
        current_pos = self.last_spot
        self.last_spot = pos

        if perception.dirty:
            self.last_spot = current_pos
            return self.ACTION.SUCK
        # seems we hit a wall :O
        elif pos == current_pos or not randint(0, 5):
            # turn around
            self.last_move = choice(
                list({self.ACTION.RIGHT, self.ACTION.LEFT, self.ACTION.UP, self.ACTION.DOWN} - {self.last_move}))
            return self.last_move
        else:
            return self.last_move


Robot = RandomPreferLastMoveAgent
