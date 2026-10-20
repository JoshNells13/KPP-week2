# Provided, do not modify.

import math

from rally_miru.motion import snap_heading, snap_to_cell_center, wrap_angle


def close(a, b, tolerance=1e-9):
    return abs(a - b) < tolerance


def test_wrap_angle():
    assert close(wrap_angle(3 * math.pi / 2), -math.pi / 2)
    assert close(wrap_angle(-3 * math.pi / 2), math.pi / 2)
    assert close(wrap_angle(0.5), 0.5)


def test_snap_to_cell_center():
    assert close(snap_to_cell_center(3.3), 3.0)
    assert close(snap_to_cell_center(3.7), 4.0)
    assert close(snap_to_cell_center(0.9), 1.0)


def test_snap_heading():
    assert close(snap_heading(0.03), 0.0)
    assert close(snap_heading(1.6), math.pi / 2)
    assert close(snap_heading(-1.5), -math.pi / 2)
