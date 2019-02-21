from random import choice, sample
from typing import NamedTuple


class Point(NamedTuple):
    dirty: bool
    uuid: str  # from str(uuid.uuid4)


class Action:
    SUCK = "suck"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    NOOP = "noop"

    COST_MAP = {
        SUCK: 2,
        LEFT: 1,
        RIGHT: 1,
        UP: 1,
        DOWN: 1,
        NOOP: 0,
    }


class Agent:
    AUTHOR = "fred@thorgate.eu"
    NAME = "Agent"
    ACTION = Action

    def __str__(self) -> str:
        return str(self.NAME)

    def step(self, perception: Point) -> str:
        if perception.dirty:
            return Action.SUCK
        return Action.NOOP  # replace this with actual movement logic


class RandomAgent(Agent):

    def __init__(self) -> None:
        super().__init__()
        # generate name
        self.name = "".join(sample("ox -|." * 10, 8))

    def __str__(self) -> str:
        return str(self.name)

    def step(self, perception: Point) -> str:
        from time import sleep
        from random import uniform
        sleep(uniform(0, 0.05))
        if perception.dirty:
            return Action.SUCK
        else:
            return choice([Action.RIGHT, Action.LEFT, Action.UP, Action.DOWN])

Robot = RandomAgent