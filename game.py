from random import randint, sample, choice, shuffle
from time import sleep, time
from typing import List, Tuple
from uuid import uuid4

from color_picker import ColorChoice
from agent import Point
from player_manager import import_players, PlayerProcessManager
from settings import *


class Game:

    def __init__(self) -> None:
        self.color_picker = ColorChoice(list(colors.values()))

        # generate base grid
        self.grid = set()
        for x in range(GRID_SIZE_X):
            for y in range(GRID_SIZE_Y):
                self.grid.add((x, y))

        self.ids = {
            coord: uuid4()
            for coord in self.grid
        }

        # generate players, uses multiprocessing wrapper
        agent_coords = {self.rand_coord() for _ in range(10)}
        agents: List[PlayerProcessManager] = import_players()
        self.agents = {
            (x, y): dict(color=self.color_picker.get(), collected=0, cost=0, agent=agent)
            for (x, y), agent in zip(agent_coords, agents)
        }

        # generate walls, keep them separate
        walls = {
            self.rand_coord()
            for _ in range(int(GRID_SIZE_X * GRID_SIZE_Y * 0.3))
        }

        self.delta_set = set()
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx or dy:
                    self.delta_set.add((dx, dy))

        for w in set(walls):
            for dx, dy in self.delta_set:
                if w in walls:
                    delta = (w[0] + dx, w[1] + dy)
                    walls.discard(delta)

        walls -= agent_coords

        self.wall_coords = walls

        self.dirt_coords = set()

    @staticmethod
    def rand_coord():
        return randint(0, GRID_SIZE_X - 1), randint(0, GRID_SIZE_Y - 1)

    def ping(self):
        # keep the player processes alive, by providing a heart beat
        for agent_dict in self.agents.values():
            agent: PlayerProcessManager = agent_dict['agent']
            agent.put(ManagementMessage.PING)

    def step(self):
        self.send()
        self.receive()

    def send(self):
        for pos, agent_dict in self.agents.items():
            dirty = pos in self.dirt_coords
            agent: PlayerProcessManager = agent_dict['agent']

            x, y = pos
            uuid = self.ids[(x, y)]

            point = Point(uuid=uuid, dirty=dirty)
            agent.put(point)

    def wait(self, steps):
        for check_index in range(steps):
            ms_step = 5
            if all(agent_dict["agent"].has() for agent_dict in self.agents.values()):
                print("done in %dms" % (check_index * ms_step))
                break
            sleep(0.001 * ms_step)
        else:
            print("some agents failed to provide answer in time :O")

    def receive(self):
        start = time()
        self.wait(10)

        new_agent_state = {}
        new_dirt_coords = set(self.dirt_coords)

        agents = list(self.agents.items())
        shuffle(agents)

        for pos, agent_dict in agents:
            dirty = pos in self.dirt_coords
            color = agent_dict['color']
            agent = agent_dict['agent']
            collected = agent_dict['collected']
            cost = agent_dict['cost']

            x, y = pos

            agent_action = agent.get()
            print("\t", str(agent), agent_action)

            if agent_action not in Action.COST_MAP:
                agent_action = Action.NOOP

            open_points = self.grid - self.agents.keys() - self.wall_coords - new_agent_state.keys()
            new_coord = pos
            if agent_action == Action.RIGHT and (x + 1, y) in open_points:
                new_coord = (x + 1, y)

            elif agent_action == Action.LEFT and (x - 1, y) in open_points:
                new_coord = (x - 1, y)

            elif agent_action == Action.UP and (x, y - 1) in open_points:
                new_coord = (x, y - 1)

            elif agent_action == Action.DOWN and (x, y + 1) in open_points:
                new_coord = (x, y + 1)

            elif agent_action == Action.SUCK:
                collected += dirty
                new_dirt_coords.discard(pos)

            elif agent_action == Action.NOOP:
                pass

            cost += Action.COST_MAP[agent_action]

            new_agent_state[new_coord] = dict(color=color, collected=collected, cost=cost, agent=agent)

        self.dirt_coords = new_dirt_coords
        self.agents = new_agent_state

        grid_size = len(self.grid)
        dirt_count = len(self.dirt_coords)
        if dirt_count < grid_size * 0.5 and randint(0, 2) == 0 or dirt_count < grid_size * 0.3:
            open_spots = self.grid - self.wall_coords - self.agents.keys() - self.dirt_coords
            prefered = []

            for open_point in open_spots:
                for dx, dy in self.delta_set:
                    delta = (open_point[0] + dx, open_point[1] + dy)
                    if delta in self.dirt_coords:
                        prefered.append(open_point)
            if prefered:
                self.dirt_coords |= set(sample(prefered, 2))
            else:
                self.dirt_coords |= set(sample(open_spots, 2))

        print("### Game step done, %0.3f\n" % (time() - start))

    def render(self) -> Tuple[List, List]:
        # reduce the game information into a dictionary
        # used for gui
        walls = [dict(x=x, y=y, color="black") for x, y in self.wall_coords]

        agents = [
            dict(
                x=x, y=y,
                color=agent["color"], margin=0.1, shape=Shape.CIRCLE,
                score=agent['collected'], cost=agent['cost'],
                name=str(agent['agent'])
            )
            for (x, y), agent in self.agents.items()
        ]

        dirt = [dict(x=x, y=y, color="orange", margin=0.1) for x, y in self.dirt_coords]
        return walls + dirt + agents, agents


if __name__ == '__main__':
    game = Game()
    game.step()
    game.render()
