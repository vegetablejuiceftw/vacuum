import pathlib

# this file importer is python 3.3+ compatible
# but there is a preferred solution for 3.5+
from importlib.machinery import SourceFileLoader
from multiprocessing import Process, Queue
from queue import Empty
from time import sleep
from typing import List, Optional, Union

from agent import Point
from settings import ManagementMessage


class PlayerProcessManager:

    def __init__(self, idx, path) -> None:
        self.input = Queue()
        self.output = Queue()
        self.idx, self.path = idx, path
        self.p = Process(target=self.handle, args=(idx, path, self.input, self.output))
        self.p.start()

        try:
            self.name = self.output.get(timeout=200)
        except Empty:
            self.name = "[Failed to load %s]" % path

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def handle(idx, path, input: Queue, output: Queue):
        module = import_player_module(idx, path)
        player = module.Robot()
        name = str(player)
        output.put(name)

        print("\t", "connected", name)

        while True:
            try:
                message: Union[Point, int] = input.get(timeout=10)
            except Empty:
                print("\t", "Timeout", name)
                return

            if message == ManagementMessage.PING:
                continue
            else:
                point: Point = message

            action = player.step(point)
            # print("\t", name, point, action)
            PlayerProcessManager.clear(output)
            output.put(action)

    @staticmethod
    def clear(q: Queue):
        # MP queue does not have a clear function :/
        try:
            while True:
                q.get_nowait()
        except Empty:
            pass

    def put(self, point: Point) -> None:
        self.clear(self.input)
        self.clear(self.output)
        self.input.put(point)

    def get(self) -> Optional[str]:
        try:
            return self.output.get_nowait()
        except Empty:
            return None

    def has(self):
        return not self.output.empty()

    def __del__(self):
        print("Dead", self.idx, self.path)
        self.p.join()


def import_player_module(idx: int, player_path: str):
    player_module = SourceFileLoader("player-%d" % idx, player_path).load_module()
    return player_module


def import_player_modules():
    player_modules = []
    for idx, file_path in enumerate(pathlib.Path('players').glob('**/*.py')):
        path = str(file_path.absolute())
        pm = import_player_module(idx, player_path=path)
        player_modules.append(pm)
    return player_modules


def import_players() -> List[PlayerProcessManager]:
    players = []
    for idx, file_path in enumerate(pathlib.Path('players').glob('**/*.py')):
        if idx > 3: break
        path = str(file_path.absolute())
        pm = PlayerProcessManager(idx, path)
        players.append(pm)

    return players


if __name__ == '__main__':

    point = Point(False, "PointMcPointFace")

    players = import_players()
    for p in players:
        p.put(point)

    sleep(0.3)
    print([p.get() for p in players])
    print([p.get() for p in players])
    print([p.get() for p in players])
