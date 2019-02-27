from typing import NamedTuple
import random

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


class Point(NamedTuple):
    dirty: bool
    uuid: str  # generated from str(uuid.uuid4)


class Robot:
    AUTHOR = "roseme@taltech.ee"
    NAME = "Munchtime"
    ACTION = Action
    prev_room = None
    prev_action = None
    rooms = dict()

    def __str__(self) -> str:
        return str(self.NAME)

    def step(self, perception: Point) -> str:
        if perception.dirty:
            return Action.SUCK
        else:
            if perception.uuid in self.rooms.keys() and self.prev_room == perception.uuid:
                (self.rooms[perception.uuid]).remove(self.prev_action)
            self.prev_room = perception.uuid
            self.prev_action = random.choice(self.rooms.get(perception.uuid, [Action.LEFT, Action.RIGHT, Action.DOWN, Action.UP]))
            return self.prev_action

    