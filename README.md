# Mission briefing

Fred has a reaaaaally dirty room.

His solution is to deploy a bunch of vacuum robots to clean the mess up.
Unfortunately he is very suspicious of what the commercial robots think and spy.

Now that's where you come in.
Your job is to write the best driver for the Roomba.

Your solution, if passing the initial screening,
will be assessed in a competition format live on screen.

Best solutions might be included in this challenge, forever honoring the champions.

# Technical

The solution type is to write a `reflex agent` based AI.

  A simple reflex agent is the most basic of the intelligent agents out there. It performs actions based on a current situation. When something happens in the environment of a simple reflex agent, the agent quickly scans its knowledge base for how to respond to the situation at-hand based on pre-determined rules.

You are given the current position point as input.
It has location `uuid` id (no coordinates) and whether it has `dirt`.  
You should return an action based on this input.  
Valid actions are `UP`, `DOWN`, `LEFT`, `RIGHT`, `SUCK` for dirt cleaning and `NOOP` for no-operation.  
Each successful `SUCK` (one that removed dirt) awards the player a `score point`.  
The module is expected to load and work well using around 50ms. Delayed answers are discarded.

The agent should have a name and an author.  
The name should be less than 16 characters long, so think of something unique & cool :D.

The class that is imported from your solution in the challenge is `Robot`.

## The agent format is as follows

```python
from typing import NamedTuple

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


class Agent:
    AUTHOR = "fred@thorgate.eu"
    NAME = "Agent"
    ACTION = Action

    def __str__(self) -> str:
        return str(self.NAME)

    def step(self, perception: Point) -> str:
        if perception.dirty:
            return Action.SUCK
        return Action.NOOP
```

Simplest test:

```python
from solution import Robot

dusty_room_map = {}
dim = 3
for x in range(1, 1 + dim):
    for y in range(1, 1 + dim):
        dusty_room_map[(x, y)] = Point(True, str(uuid4()))

# random wall
del dusty_room_map[(2, 3)]

agent = Robot()
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

    for y_pos in range(1, dim + 1):
        print("")
        for x_pos in range(1, dim + 1):
            pos = (x_pos, y_pos)
            point = dusty_room_map.get(pos)

            if pos == agent_pos:
                print("R", end=" ")
            elif not point:
                print("#", end=" ")
            elif point.dirty:
                print("o", end=" ")
            else:
                print(".", end=" ")

    print("agent is in:{} total dirt:{} last action:{}".format(
        agent_pos,
        sum(room.dirty for room in dusty_room_map.values()),
        agent_action,
    ))
print("Done")
```

The output should be similar to this:  
`R` - robot, `.` - empty, `#` - obstacle / wall, `o` - dirt / score point
```
. . . 
o o R 
o # o agent is in:(3, 2) total dirt:5 last action:down
```

## Hints

- Your agent should always remove dust when it can
- Initial solution can be random choice of movement actions
- This can be improved by remembering last moving direction and continuing it for a random distance.
- Finally, mapping the environment will reduce the visiting of already cleaned tiles
- In the tournament app, the dirt has a generation pattern which can taken advantage of.

### # # # # # # # # # # # # # # #

The tournament gui app that the software will run:

<img src="https://pyspace.egg.thorgate.eu/media/70f/287415638455fabbc69b5f935eb52/small_example2.gif.gif" />

[Provided as is. Not recommended until you have passed with an initial implementation.](https://github.com/vegetablejuiceftw/vacuum)