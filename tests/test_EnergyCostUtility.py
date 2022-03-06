from cmath import sqrt
import pytest

from EnergyCostUtility import calculate_required_wheel_rotations

def test_calculate_required_wheel_rotations():
    assert calculate_required_wheel_rotations(2.0, 4.0) == 2.0