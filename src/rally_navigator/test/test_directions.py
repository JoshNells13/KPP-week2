# Provided, do not modify.

from rally_navigator.grid import Cell
from rally_navigator.route import route_to_directions

EAST, NORTH, WEST, SOUTH = 0, 1, 2, 3


def test_straight_line():
    route = [Cell(0, 0), Cell(1, 0), Cell(2, 0)]
    assert route_to_directions(route) == [EAST, EAST]


def test_all_four_directions():
    route = [Cell(1, 1), Cell(2, 1), Cell(2, 2), Cell(1, 2), Cell(1, 1)]
    assert route_to_directions(route) == [EAST, NORTH, WEST, SOUTH]


def test_a_route_of_one_cell_has_no_steps():
    assert route_to_directions([Cell(3, 3)]) == []


def test_empty_route():
    assert route_to_directions([]) == []


def test_longer_route():
    route = [Cell(0, 0), Cell(0, 1), Cell(0, 2), Cell(1, 2), Cell(1, 1), Cell(1, 0)]
    assert route_to_directions(route) == [NORTH, NORTH, EAST, SOUTH, SOUTH]
