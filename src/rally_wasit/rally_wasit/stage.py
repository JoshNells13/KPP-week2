import random
from typing import NamedTuple

# Provided, do not modify. Builds the random stage from a seed.

WIDTH = 10
HEIGHT = 10
ROCK_RATE = 0.25
MIN_ROUTE_STEPS = 12
MAX_ATTEMPTS = 1000

# East, north, west, south: the same order as the navigator uses.
DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))


class Stage(NamedTuple):
    width: int
    height: int
    rocks: tuple  # width * height values, 1 = rock, row by row from row 0
    start: tuple  # (col, row)
    finish: tuple  # (col, row)


def is_rock(stage, col, row):
    return stage.rocks[row * stage.width + col] == 1


def route_length(stage):
    # Number of moves of the shortest route from start to finish, None if there is none.
    distance = {stage.start: 0}
    queue = [stage.start]
    for col, row in queue:
        if (col, row) == stage.finish:
            return distance[(col, row)]
        for dcol, drow in DIRECTIONS:
            nxt = (col + dcol, row + drow)
            inside = 0 <= nxt[0] < stage.width and 0 <= nxt[1] < stage.height
            if inside and nxt not in distance and not is_rock(stage, nxt[0], nxt[1]):
                distance[nxt] = distance[(col, row)] + 1
                queue.append(nxt)
    return None


def generate_stage(seed):
    # random.Random(seed).random() gives the same numbers on every machine.
    rng = random.Random(seed)
    for _ in range(MAX_ATTEMPTS):
        rocks = [1 if rng.random() < ROCK_RATE else 0 for _ in range(WIDTH * HEIGHT)]
        start = (0, int(rng.random() * HEIGHT))
        finish = (WIDTH - 1, int(rng.random() * HEIGHT))
        rocks[start[1] * WIDTH + start[0]] = 0
        rocks[finish[1] * WIDTH + finish[0]] = 0

        stage = Stage(WIDTH, HEIGHT, tuple(rocks), start, finish)
        steps = route_length(stage)
        if steps is not None and steps >= MIN_ROUTE_STEPS:
            return stage
    raise RuntimeError(f'no valid stage found for seed {seed}')
