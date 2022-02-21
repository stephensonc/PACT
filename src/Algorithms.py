from math import dist
from tracemalloc import start
from RobotData import RobotData
from EnvironmentData import EnvironmentGraph, EnvironmentNode
from EnergyCostUtility import calculate_energy_cost

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
        print("Running default AStar")
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
            # Probably could return here

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
        return dist(start_node.coord_tuple, dest_node.coord_tuple) 


class EnergyCostAStar(DefaultAStar):

    def __init__(self, robot_data_obj: RobotData = None) -> None:
        super().__init__(robot_data_obj)

    class EnergyCostAStarEnvironmentNode(DefaultAStar.AStarEnvironmentNode):

        def __init__(self, node: EnvironmentNode) -> None:
            super().__init__(node)
        
        def calculate_edge_cost(self, target_node: EnvironmentNode) -> float:
            return calculate_energy_cost(self, target_node, self.robot_data_obj)


    def run(self, env_grid: EnvironmentGraph, start_cell_coords: tuple, dest_cell_coords: tuple) -> "list[DefaultAStar.AStarEnvironmentNode]":
        for row in env_grid.nodes:
            for node in row:
                node.set_robot_data(self.robot_data_obj)
        return super().run(env_grid, start_cell_coords, dest_cell_coords)

    def get_h_value(start_node: EnvironmentNode, dest_node: EnvironmentNode) -> int:
        return calculate_energy_cost(start_node, dest_node)