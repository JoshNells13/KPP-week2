# Provided, do not modify.

import random

from helpers import drive, make_instruction, random_map
from rally_interfaces.msg import Instruction
from rally_navigator.route import directions_to_instructions, find_route, route_to_instructions

EAST, NORTH, WEST, SOUTH = 0, 1, 2, 3


def test_straight_then_turns():
    expected = [
        make_instruction(1, 2, Instruction.TURN_LEFT),
        make_instruction(2, 2, Instruction.TURN_LEFT),
        make_instruction(3, 2, Instruction.TURN_NONE)]
    assert directions_to_instructions([EAST, EAST, NORTH, NORTH, WEST, WEST]) == expected


def test_right_turn():
    expected = [
        make_instruction(1, 1, Instruction.TURN_RIGHT),
        make_instruction(2, 1, Instruction.TURN_NONE)]
    assert directions_to_instructions([EAST, SOUTH]) == expected


def test_first_move_is_north():
    expected = [
        make_instruction(1, 0, Instruction.TURN_LEFT),
        make_instruction(2, 2, Instruction.TURN_NONE)]
    assert directions_to_instructions([NORTH, NORTH]) == expected


def test_first_move_is_south():
    expected = [
        make_instruction(1, 0, Instruction.TURN_RIGHT),
        make_instruction(2, 1, Instruction.TURN_NONE)]
    assert directions_to_instructions([SOUTH]) == expected


def test_u_turn_is_two_left_turns():
    # Miru mulai menghadap timur, sedangkan rutenya ke barat.
    expected = [
        make_instruction(1, 0, Instruction.TURN_LEFT),
        make_instruction(2, 0, Instruction.TURN_LEFT),
        make_instruction(3, 2, Instruction.TURN_NONE)]
    assert directions_to_instructions([WEST, WEST]) == expected


def test_no_steps():
    assert directions_to_instructions([]) == [make_instruction(1, 0, Instruction.TURN_NONE)]


def test_driving_them_reaches_the_finish():
    rng = random.Random(777)
    checked = 0
    for attempt in range(200):
        grid = random_map(rng)
        route = find_route(grid)
        if not route:
            continue

        instructions = route_to_instructions(route)
        assert [i.id for i in instructions] == list(range(1, len(instructions) + 1))
        assert instructions[-1].turn == Instruction.TURN_NONE, f'attempt {attempt}'
        assert drive(grid, instructions) == grid.finish, f'attempt {attempt}'
        checked += 1
    assert checked > 100
