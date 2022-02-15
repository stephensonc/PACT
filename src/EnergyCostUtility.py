from cmath import sqrt
import math
from src.EnvironmentData import EnvironmentNode


def calculate_energy_cost(horizondal_dist, vertical_dist, robot_data_obj):
    pass


def distance_between_nodes(node_1: EnvironmentNode, node_2: EnvironmentNode):
    """ Get the horizontal(level) distance between two nodes """
    distance = 0.0

    return math.dist((node_1.x_coord, node_1.y_coord), (node_2.x_coord, node_1.y_coord))
    if node_1.x_coord == node_2.x_coord:
        distance = node_2.y_coord - node_1.y_coord
    elif node_1.y_coord == node_2.y_coord:
        distance = node_2.x_coord - node_1.x_coord
    else:
        x_dist = node_2.x_coord - node_1.x_coord
        y_dist = node_2.y_coord - node_1.y_coord
        distance = sqrt(pow(x_dist, 2) + pow(y_dist, 2))
    return abs(distance)