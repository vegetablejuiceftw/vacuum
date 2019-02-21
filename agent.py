from random import choice, sample
from typing import NamedTuple
from uuid import uuid4

from settings import *


class Point(NamedTuple):
    dirty: bool
    uuid: str  # from str(uuid.uuid4)


class Agent:
    AUTHOR = "fred@thorgate.eu"
    NAME = "Agent"
    ACTION = Action

    def __init__(self) -> None:
        self.name = self.NAME

    def __str__(self) -> str:
        return str(self.name)

    def step(self, perception: Point) -> str:
        if perception.dirty:
            return Action.SUCK
        return Action.NOOP  # replace this with actual movement logic


class RandomAgent(Agent):

    def __init__(self) -> None:
        super().__init__()
        # generate name
        self.name = "".join(sample("ox -|." * 10, 8))

    def step(self, perception: Point) -> str:
        from time import sleep
        from random import uniform
        sleep(uniform(0, 0.05))
        if perception.dirty:
            return Action.SUCK
        else:
            return choice([Action.RIGHT, Action.LEFT, Action.UP, Action.DOWN])


if __name__ == '__main__':
    Robot = RandomAgent
    # # # # # #
    dusty_room_map = {}
    dim = 3
    for x in range(1, 1 + dim):
        for y in range(1, 1 + dim):
            dusty_room_map[(x, y)] = Point(True, str(uuid4()))

    # random wall
    del dusty_room_map[(2, 3)]

    agent = Robot()  # Your improved agent
    agent_pos = (1, 1)
    agent_score = 0
    agent_steps = 0

    # while any rooms are dirty, run simulation
    while any(room.dirty for room in dusty_room_map.values()):
        # count the iterations
        agent_steps += 1

        current_room = dusty_room_map[agent_pos]

        agent_action = agent.step(current_room)

        x, y = agent_pos
        left_pos = (x - 1, y)
        right_pos = (x + 1, y)
        up_pos = (x, y - 1)
        down_pos = (x, y + 1)

        if agent_action == Action.LEFT and left_pos in dusty_room_map:
            agent_pos = left_pos

        elif agent_action == Action.RIGHT and right_pos in dusty_room_map:
            agent_pos = right_pos

        elif agent_action == Action.UP and up_pos in dusty_room_map:
            agent_pos = up_pos

        elif agent_action == Action.DOWN and down_pos in dusty_room_map:
            agent_pos = down_pos

        elif agent_action == Action.SUCK:
            agent_score += current_room.dirty
            dusty_room_map[agent_pos] = Point(False, current_room.uuid)

        for x_pos in range(1, dim + 1):
            print("")
            for y_pos in range(1, dim + 1):
                pos = (x_pos, y_pos)
                point = dusty_room_map.get(pos)

                if not point:
                    print("#", end=" ")
                elif point.dirty:
                    print("o", end=" ")
                elif pos == agent_pos:
                    print("R", end=" ")
                else:
                    print(".", end=" ")

        print("agent is in:{} total dirt:{} last action:{}".format(
            agent_pos,
            sum(room.dirty for room in dusty_room_map.values()),
            agent_action,
        ))
    print("Done")
