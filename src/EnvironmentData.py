import math
from RobotData import RobotData


class EnvironmentNode:


    # Each node is 1 meter away from the next in line, not counting elevation differences

    def __init__(self, x_coordinate: int, y_coordinate: int, elevation: float, friction_coeff: float = 1.0, passable: bool = True):
        # Type annotations:
        self.x_coord: int
        self.y_coord: int
        self.coord_tuple: tuple
        self.elevation: float
        self.adjacent_edges: list[EnvironmentGraph.Edge]
        self.passable: bool
        self.friction_coefficient: float

        # Instance variable initialization
        self.x_coord = x_coordinate
        self.y_coord = y_coordinate
        self.coord_tuple = (self.x_coord, self.y_coord)
        self.elevation = elevation
        self.adjacent_edges = []
        self.passable = passable
        self.friction_coefficient = friction_coeff

        # Robot Data
        self.robot_data_obj = None
        
        
    def add_adjacent_edge(self, distance: float, node):
        # self.adjacent_edges.append((distance, node))
        self.adjacent_edges.append(EnvironmentGraph.Edge(distance, self, node))


    def set_robot_data(self, robot_data_obj: RobotData):
        self.robot_data_obj = robot_data_obj


    # Override this to change how the edge cost is generated
    def calculate_edge_cost(self, target_node) -> float:
        return distance_between_nodes(self, target_node)

    def get_adjacent_nodes(self, graph_nodes):
        self.adjacent_edges = []
        x = self.x_coord
        y = self.y_coord

        num_cols = len(graph_nodes)
        num_rows = len(graph_nodes[0])

        top_node = None
        top_left = None
        top_right = None
        left_node = None
        right_node = None
        bot_node = None
        bot_left = None
        bot_right = None

        # Top, left, right, bottom
        if x < num_cols - 1: 
            right_node = graph_nodes[x + 1][y]
        if x > 0:
            left_node = graph_nodes[x - 1][y]
        if y < num_rows - 1:
            top_node = graph_nodes[x][y + 1]
        if y > 0:
            bot_node = graph_nodes[x][y-1]

        # Diagonal adjacency
        if x > 0 and y > 0:
            bot_left = graph_nodes[x - 1][y - 1]
        if x < num_cols - 1 and y > 0:
            bot_right = graph_nodes[x + 1][y - 1]
        if x > 0 and y < num_rows - 1:
            top_left = graph_nodes[x - 1][y + 1]
        if x < num_cols - 1 and y < num_rows - 1:
            top_right = graph_nodes[x + 1][y + 1]

        adj_nodes = [
            top_node,
            top_left,
            top_right,
            left_node,
            right_node,
            bot_node,
            bot_left,
            bot_right
            ]

        for node in adj_nodes:
            if node is not None and node.passable:
                dist = self.calculate_edge_cost(node)
                self.add_adjacent_edge(dist, node)
        for edge in self.adjacent_edges:
            if edge.passable:
                break
            elif edge == self.adjacent_edges[-1]:
                print(f"All adjacent nodes impassible for node at ({self.x_coord}, {self.y_coord})")


    def print(self):
        print(
        f"| x: {self.x_coord}, y: {self.y_coord}, elevation: {self.elevation}"
        , end=' |')

class EnvironmentGraph:


    class Edge:
        def __init__(self, traversal_cost: float, start_node: EnvironmentNode, dest_node: EnvironmentNode, passable_threshold: float = 70.0) -> None:
            self.cost = traversal_cost
            self.destination_node = dest_node
            self.passable = self.is_climbable(start_node, dest_node)

        def is_climbable(self, node1: EnvironmentNode, node2: EnvironmentNode, passable_thresh: float = 70.0):
            if not node2.passable:
                return False
            else:
                return calculate_incline_angle_degrees(node1, node2) <= passable_thresh


    # Num_columns is the width, num_rows is the height
    def __init__(self, num_columns: int, num_rows: int) -> None:
        self.nodes = []
        for i in range(num_columns):            
            self.nodes.append([])
            for j in range(num_rows):
                self.nodes[-1].append(EnvironmentNode(i, j, -1.0))
    
    def add_node_raw(self, x_coord: int, y_coord: int, elevation: float):
        self.add_node(EnvironmentNode(x_coord, y_coord, elevation))
    
    def add_node(self, node: EnvironmentNode):
        if node.x_coord < len(self.nodes):
            if node.y_coord < len(self.nodes[node.x_coord]):
                self.nodes[node.x_coord][node.y_coord] = node

    # Updates the adjacency list for every node in the graph
    def update_adjacent_nodes(self):
        for column in self.nodes:
            for node in column:
                node.get_adjacent_nodes(self.nodes)

    def print(self):
        for column in self.nodes:
            for node in column:
                node.print()
            print()


def distance_between_nodes(node_1: EnvironmentNode, node_2: EnvironmentNode):
        """ Get the distance between two nodes in meters, including elevation."""
        distance = math.dist(
            [node_1.x_coord, node_1.y_coord, node_1.elevation],
            [node_2.x_coord, node_2.y_coord, node_2.elevation])

        #elevation_diff = node_2.elevation - node_1.elevation

        #distance = math.tan(elevation_diff/distance)
        return distance

def calculate_incline_angle_degrees(node1: EnvironmentNode, node2: EnvironmentNode) -> float:
    horizontal_distance = math.dist([node1.x_coord, node1.y_coord], [node2.x_coord, node2.y_coord])
    vertical_distance = node2.elevation - node1.elevation
    if horizontal_distance == 0:
        print("Distance between nodes is zero")
        print(node1.coord_tuple)
        print(node2.coord_tuple)
        angle = 0
    else:
        angle = math.degrees(math.atan(vertical_distance/horizontal_distance))
    return angle