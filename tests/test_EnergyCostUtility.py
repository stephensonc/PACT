from cmath import sqrt
import pytest
from src.EnergyCostUtility import distance_between_nodes
from src.EnvironmentData import EnvironmentNode

# def test_distance_between_nodes():
#     node1 = EnvironmentNode(0.0, 19.2, 0.0)
#     node2 = EnvironmentNode(14.1, 25.0, 0.0)
#     dist = distance_between_nodes(node1, node2)
#     198.81 + 33.64 
#     assert dist == sqrt(pow(14.1, 2) + pow(25.0 - 19.2, 2))