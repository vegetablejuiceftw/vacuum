from agent import Point
from players.prefer_last import RandomPreferLastMoveAgent


class LazyRandomPreferLastMoveAgent(RandomPreferLastMoveAgent):
    NAME = "Lazy"
    AUTHOR = "lazy@thorgate.eu"

    def __init__(self) -> None:
        super().__init__()
        self.steps = 0

    def step(self, perception: Point) -> str:
        self.steps += 1

        if perception.dirty:
            return self.ACTION.SUCK

        if self.steps % 3 == 0:
            return self.ACTION.NOOP

        return super().step(perception)


Robot = LazyRandomPreferLastMoveAgent
