import random
from typing import NamedTuple


class Action:
    SUCK = 'suck'
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'
    NOOP = 'noop'

    COST_MAP = {
        SUCK: 2,
        LEFT: 1,
        RIGHT: 1,
        UP: 1,
        DOWN: 1,
        NOOP: 0,
    }


class Point(NamedTuple):
    dirty: bool
    uuid: str  # generated from str(uuid.uuid4)


class Agent:
    AUTHOR = 'fred@thorgate.eu'
    NAME = 'Agent'
    ACTION = Action

    def __str__(self) -> str:
        return str(self.NAME)

    def step(self, perception: Point) -> str:
        if perception.dirty:
            return Action.SUCK
        return Action.NOOP


class Robot(Agent):
    AUTHOR = 'rrebase@thorgate.eu'
    NAME = 'Almost Random Robot'

    def __init__(self) -> None:
        super().__init__()
        self.last_pos = None
        self.last_move = None

    def __str__(self) -> str:
        return str(self.NAME)

    def ran_into_wall(self, current_pos) -> bool:
        if not self.last_pos:
            return False
        return self.last_pos == current_pos

    # Some ugly if statement logic, better than total random :)
    def step(self, perception: Point) -> str:
        if perception.dirty:
            return Action.SUCK

        sensible_choices = [
            Agent.ACTION.LEFT,
            Agent.ACTION.UP,
            Agent.ACTION.RIGHT,
            Agent.ACTION.DOWN,
        ]

        if self.ran_into_wall(perception) and self.last_move:
            sensible_choices.remove(self.last_move)

        move = random.choice(sensible_choices)

        self.last_pos = perception
        self.last_move = move

        return move
