# Provided, do not modify.

import random

from helpers import make_map, random_map, shortest_steps
from rally_navigator.grid import Cell
from rally_navigator.route import find_route


def test_straight_line():
    grid = make_map(['S...F'])
    assert find_route(grid) == [Cell(i, 0) for i in range(5)]


def test_goes_around_rocks():
    grid = make_map([
        '..F',
        '##.',
        'S..'])
    assert find_route(grid) == [Cell(0, 0), Cell(1, 0), Cell(2, 0), Cell(2, 1), Cell(2, 2)]


def test_unique_long_route():
    # Satu-satunya rute terpendek: timur, utara, barat.
    grid = make_map([
        'F..',
        '##.',
        'S..'])
    expected = [Cell(0, 0), Cell(1, 0), Cell(2, 0), Cell(2, 1), Cell(2, 2), Cell(1, 2),
                Cell(0, 2)]
    assert find_route(grid) == expected


def test_no_route():
    grid = make_map([
        '..F',
        '###',
        'S..'])
    assert find_route(grid) == []


def test_start_is_finish():
    grid = make_map(['S..'])
    grid.finish = grid.start
    assert find_route(grid) == [grid.start]


def test_is_shortest_on_random_maps():
    rng = random.Random(12345)
    found = 0
    for attempt in range(200):
        grid = random_map(rng)
        expected = shortest_steps(grid)
        route = find_route(grid)
        if expected < 0:
            assert route == [], f'attempt {attempt}'
            continue

        found += 1
        assert len(route) == expected + 1, f'attempt {attempt}'
        assert route[0] == grid.start and route[-1] == grid.finish
        for previous, cell in zip(route, route[1:]):
            assert not grid.is_rock(cell), f'attempt {attempt}'
            assert abs(cell.col - previous.col) + abs(cell.row - previous.row) == 1
    assert found > 100
