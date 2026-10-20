# Provided, do not modify.

import math

from rally_interfaces.msg import Instruction
from rally_miru.motion import MAX_TURN_RATE, MIN_TURN_RATE, turn_rate, turn_target, TURN_TOLERANCE


def close(a, b, tolerance=1e-9):
    return abs(a - b) < tolerance


def test_turn_target():
    assert close(turn_target(0.0, Instruction.TURN_LEFT), math.pi / 2)
    assert close(turn_target(0.0, Instruction.TURN_RIGHT), -math.pi / 2)
    assert close(turn_target(math.pi / 2, Instruction.TURN_LEFT), math.pi)
    assert close(abs(turn_target(math.pi, Instruction.TURN_LEFT)), math.pi / 2)
    assert close(abs(turn_target(-math.pi / 2, Instruction.TURN_RIGHT)), math.pi)


def test_turn_target_stays_in_range():
    assert close(turn_target(math.pi, Instruction.TURN_LEFT), -math.pi / 2)
    assert -math.pi <= turn_target(-math.pi / 2, Instruction.TURN_RIGHT) <= math.pi


def test_turn_rate_stops_inside_tolerance():
    assert turn_rate(0.0) == 0.0
    assert turn_rate(TURN_TOLERANCE / 2) == 0.0
    assert turn_rate(-TURN_TOLERANCE / 2) == 0.0


def test_turn_rate_direction_and_limits():
    assert turn_rate(1.0) == MAX_TURN_RATE
    assert turn_rate(-1.0) == -MAX_TURN_RATE
    assert turn_rate(0.05) == MIN_TURN_RATE
    assert turn_rate(-0.05) == -MIN_TURN_RATE
    assert 0.0 < turn_rate(0.2) < MAX_TURN_RATE
