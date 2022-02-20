from cmath import sqrt
import pytest
from src.EnvironmentData import calculate_incline_angle

from src.EnvironmentData import EnvironmentNode

def test_calculate_incline_angle():
    node1 = EnvironmentNode(0, 0, 0.0)
    node2 = EnvironmentNode(0, 3, 4.0)

    angle = calculate_incline_angle(node1, node2)
    assert round(angle, 2) == 53.13

# def test_distance_between_nodes():
#     node1 = EnvironmentNode(0.0, 19.2, 0.0)
#     node2 = EnvironmentNode(14.1, 25.0, 0.0)
#     dist = distance_between_nodes(node1, node2)
#     198.81 + 33.64 
#     assert dist == sqrt(pow(14.1, 2) + pow(25.0 - 19.2, 2))