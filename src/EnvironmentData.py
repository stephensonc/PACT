class EnvironmentNode:

    def __init__(self, x_coordinate, y_coordinate, elevation):
        self.x_coord = x_coordinate
        self.y_coord = y_coordinate
        self.elevation = elevation
        self.adjacent_nodes = [] # list of tuples

    
    def add_adjacent_node(self, distance: float, node):
        self.adjacent_nodes.append((distance, node))

    def print(self):
        print(
        f"""---------------
        x: {self.x_coord}
        y: {self.y_coord}
        elevation: {self.elevation}
        ---------------""",
        end='')

class EnvironmentGraph:

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

    def print(self):
        for row in self.nodes:
            for node in row:
                node.print()
            print()
