from RobotData import RobotData
from EnvironmentData import EnvironmentGraph, EnvironmentNode, distance_between_nodes, distance_between_nodes_no_elevation
from EnergyCostUtility import calculate_energy_cost


# Abstract class dictating required inputs/output
class Algorithm:

    def __init__(self, robot_data_obj: RobotData = None) -> None:
        self.robot_data_obj = RobotData() if robot_data_obj is None else robot_data_obj

    # Must return an array of tuples containing path coords
    def run(self, env_grid: EnvironmentGraph, start_cell_coords: tuple, dest_cell_coords: tuple) -> "list[tuple(int, int)]":
        pass


class DefaultAStar(Algorithm):

    def __init__(self, robot_data_obj = None) -> None:
        super().__init__(robot_data_obj)

    class AStarEnvironmentNode(EnvironmentNode):
        def __init__(self, node: EnvironmentNode) -> None:

            # Copy over original node data
            super().__init__(node.x_coord, node.y_coord, node.elevation, node.passable)
            # print(len(node.adjacent_edges))
            self.adjacent_edges = node.adjacent_edges
            self.robot_data_obj = node.robot_data_obj


            # New, AStar-specific node data
            self.previous_node = None
            self.cost_to_end = 0 # F value
            self.cost_from_start = 0 # G value
            self.heuristic_value = 0 # H value

            # update adjacent_edges type annotation
            self.adjacent_edges: list[EnvironmentGraph.Edge]



    def run(self, env_grid:EnvironmentGraph, start_cell_coords: tuple, dest_cell_coords: tuple) -> "list[AStarEnvironmentNode]":
        open_list = []
        closed_list = []
        current_node = None
        output_path = []

        # Ensure that grid nodes have adjacency info
        env_grid.update_adjacent_nodes()

        # Add the start and end nodes of the path as AStarEnvironmentNodes to give them f, g, and h values
        open_list.append(DefaultAStar.AStarEnvironmentNode(env_grid.nodes[start_cell_coords[0]][start_cell_coords[1]]))
        end_node = DefaultAStar.AStarEnvironmentNode(env_grid.nodes[dest_cell_coords[0]][dest_cell_coords[1]])


        while len(open_list) > 0:
            open_list, closed_list, current_node, output_path = self.start_pathing(open_list, closed_list, current_node, end_node)
            if len(output_path) > 0:
                break
        output_path.reverse()
        return output_path

    def start_pathing(self, open_list: "list[AStarEnvironmentNode]", closed_list: "list[AStarEnvironmentNode]", current_node: AStarEnvironmentNode, end_node: AStarEnvironmentNode):
            
        best_node_index = 0
        for i in range(len(open_list)):
            if open_list[i].cost_to_end < open_list[best_node_index].cost_to_end:
                best_node_index = i

        current_node = open_list[best_node_index]
        
        # print(f"Starting pathing for node at coords: ({current_node.x_coord}, {current_node.y_coord})")
        
        output_path = []


        # End condition
        if current_node.coord_tuple == end_node.coord_tuple:
            temp = current_node
            output_path.append(temp)
            # Retrace the steps of the best path
            while temp.previous_node is not None:
                output_path.append(temp.previous_node)
                temp = temp.previous_node
            # return open_list, closed_list, current_node, output_path

        open_list = self.pop_node_from_list(open_list, current_node)
        closed_list.append(current_node) # TODO: Verify that current_node is an AStarEnvironmentNode
        

        for adjacent_node_edge in current_node.adjacent_edges:
            # print("Getting adjacent node")
            edge_cost = adjacent_node_edge.cost
            edge_cost: float

            adjacent_node = adjacent_node_edge.destination_node
            adjacent_node: DefaultAStar.AStarEnvironmentNode
            
            # print(f"Adjacent node at coords: {adjacent_node.x_coord}, {adjacent_node.y_coord}")
            if adjacent_node in closed_list or not adjacent_node_edge.passable:
                # print("Adjacent node in closed list or non-passable")
                continue
            else:
                # print(f"Updating node at coordinates: {current_node.x_coord}, {current_node.y_coord}")
                already_updated_node = False
                temp_cost_to_adjacent_node = current_node.cost_from_start + edge_cost
                for j in range(len(open_list)):
                    # if the coordinates are the same
                    if adjacent_node.x_coord == open_list[j].x_coord and adjacent_node.y_coord == open_list[j].y_coord:
                        if temp_cost_to_adjacent_node < open_list[j].cost_from_start:
                            open_list[j].cost_from_start = temp_cost_to_adjacent_node
                            open_list[j].heuristic_value = self.get_h_value(open_list[j], end_node)
                            open_list[j].cost_to_end = open_list[j].cost_from_start + open_list[j].heuristic_value
                            open_list[j].previous_node = current_node
                            # print("Node coordinates: " + open_list[j].coord_tuple)
                        already_updated_node = True

                if not already_updated_node:
                    adjacent_node.cost_from_start = temp_cost_to_adjacent_node
                    adjacent_node.heuristic_value = self.get_h_value(adjacent_node, end_node)
                    adjacent_node.cost_to_end = adjacent_node.cost_from_start + adjacent_node.heuristic_value
                    adjacent_node.previous_node = current_node
                    open_list.append(adjacent_node)

        return open_list, closed_list, current_node, output_path

    def pop_node_from_list(self, open_list: "list[DefaultAStar.AStarEnvironmentNode]", current_node: AStarEnvironmentNode):
        for i in range(len(open_list)):
            if open_list[i] == current_node:
                open_list.pop(i)
                break
        return open_list

    def get_h_value(self, start_node: EnvironmentNode, dest_node: EnvironmentNode) -> int:
        return distance_between_nodes(start_node, dest_node) 


class EnergyCostAStar(DefaultAStar):

    def __init__(self, robot_data_obj: RobotData = None) -> None:
        super().__init__(robot_data_obj)

    class EnergyCostAStarEnvironmentNode(DefaultAStar.AStarEnvironmentNode):

        def __init__(self, node: EnvironmentNode) -> None:
            super().__init__(node)
            self.env_grid = None
        
        def calculate_edge_cost(self, target_node: EnvironmentNode) -> float:
            return calculate_energy_cost(self, target_node, self.robot_data_obj)


    def run(self, env_grid: EnvironmentGraph, start_cell_coords: tuple, dest_cell_coords: tuple) -> "list[DefaultAStar.AStarEnvironmentNode]":
        self.env_grid = env_grid
        for row in env_grid.nodes:
            for node in row:
                node.set_robot_data(self.robot_data_obj)
        return super().run(env_grid, start_cell_coords, dest_cell_coords)

    def get_h_value(self, start_node: EnvironmentNode, dest_node: EnvironmentNode) -> int:
        heuristic_cost = 0
        if start_node.coord_tuple == dest_node.coord_tuple:
            return 0.0
        else:


            # num_nodes_to_find = int(len(self.env_grid.nodes)/5)

            num_nodes_to_find = self.get_num_nodes_to_find(start_node, dest_node) # between the start and end node

            x_increment = int((dest_node.x_coord - start_node.x_coord) / num_nodes_to_find)
            y_increment = int((dest_node.y_coord - start_node.y_coord) / num_nodes_to_find)

            current_node = start_node
            # print(f"Current node x,y: ({current_node.x_coord},{current_node.y_coord})")

            for i in range(1, num_nodes_to_find + 1):
                # Get coordinates of a node (1/num_nodes_to_find) of the way to the final path node
                x_coord = current_node.x_coord + x_increment
                y_coord = current_node.y_coord + y_increment

                if x_coord == current_node.x_coord:
                    x_coord = dest_node.x_coord
                if y_coord == current_node.x_coord:
                    y_coord == dest_node.x_coord
                
                
                # print(f"\tHeuristic node x,y: ({x_coord},{y_coord})")

                # Update the node being used for the heuristic
                heuristic_node = self.env_grid.nodes[x_coord][y_coord]
                energy_cost = calculate_energy_cost(current_node, heuristic_node, self.robot_data_obj)
                # Add the cost between these two nodes to the list
                heuristic_cost += energy_cost
                
                # move to the next node of the (num_nodes_to_find) nodes to traverse
                current_node = heuristic_node
            # print(f"Heuristic value for node ({start_node.x_coord}, {start_node.y_coord}): {energy_cost}")

            return heuristic_cost

    def get_num_nodes_to_find(self, node1: EnvironmentNode, node2: EnvironmentNode):
        num_nodes = int(distance_between_nodes_no_elevation(node1, node2)/2)
        return num_nodes if num_nodes > 0 else 1