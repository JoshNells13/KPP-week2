# Provided, do not modify.

import math

from rally_miru.motion import remaining_distance, target_point


def close(a, b, tolerance=1e-9):
    return abs(a - b) < tolerance


def test_target_point():
    for heading, expected in ((0.0, (6.0, 2.0)), (math.pi / 2, (3.0, 5.0)),
                              (math.pi, (0.0, 2.0)), (-math.pi / 2, (3.0, -1.0))):
        x, y = target_point(3.0, 2.0, heading, 3)
        assert close(x, expected[0]) and close(y, expected[1]), f'heading {heading}'


def test_remaining_distance():
    assert close(remaining_distance(1.0, 1.0, 0.0, 4.0, 1.0), 3.0)
    assert close(remaining_distance(1.0, 1.0, math.pi / 2, 1.0, 3.0), 2.0)
    assert close(remaining_distance(1.0, 5.0, -math.pi / 2, 1.0, 2.0), 3.0)


def test_remaining_distance_is_negative_past_the_target():
    assert close(remaining_distance(4.3, 1.0, 0.0, 4.0, 1.0), -0.3)


def test_remaining_distance_ignores_sideways_error():
    assert close(remaining_distance(1.0, 1.2, 0.0, 4.0, 1.0), 3.0)
