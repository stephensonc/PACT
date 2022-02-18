from typing import Tuple
from src.EnvironmentData import EnvironmentGraph, EnvironmentNode

class AlgorithmInterface:

    # Must return an array of tuples containing path coords
    def run(env_grid: EnvironmentGraph, start_cell_coords: Tuple, dest_cell_coords: Tuple):
        pass


class DefaultAStar(AlgorithmInterface):

    class AStarEnvironmentNode(EnvironmentNode):
        def __init__(self, node: EnvironmentNode) -> None:

            # Copy over original node data
            super().__init__(node.x_coord, node.y_coord, node.elevation, node.passable)
            
            self.adjacent_nodes = [DefaultAStar.AStarEnvironmentNode(node) for node in self.adjacent_nodes]
            # for i in range(len(self.adjacent_nodes)):
            #     self.adjacent_nodes[i] = DefaultAStar.AStarEnvironmentNode(node)

            # New, AStar-specific node data
            self.previous_node = None
            self.cost_to_end = 0 # F value
            self.cost_from_start = 0 # G value
            self.heuristic_value = 0 # H value

            # update adjacent_nodes type annotation
            self.adjacent_nodes: list[tuple(float, DefaultAStar.AStarEnvironmentNode)]



    def run(env_grid:EnvironmentGraph, start_cell_coords: Tuple, dest_cell_coords: Tuple) -> "list[AStarEnvironmentNode]":
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
            open_list, closed_list, current_node, output_path = DefaultAStar.start_pathing(open_list, closed_list, current_node, end_node)
            if len(output_path) > 0:
                break

        return output_path

    def start_pathing(open_list: "list[AStarEnvironmentNode]", closed_list: "list[AStarEnvironmentNode]", current_node: AStarEnvironmentNode, end_node: AStarEnvironmentNode):

        best_node_index = 0
        for i in range(len(open_list)):
            if open_list[i].cost_to_end < open_list[best_node_index].cost_to_end:
                best_node_index = i

        current_node = open_list[best_node_index]

        output_path = []


        # End condition
        if current_node == end_node:
            temp = current_node

            # Retrace the steps of the best path
            while temp.previous_node is not None:
                output_path.append(temp.previous_node)
                temp = temp.previous_node
            # Probably could return here

        open_list = DefaultAStar.pop_node_from_list(open_list, current_node)
        closed_list.append(current_node) # TODO: Verify that current_node is an AStarEnvironmentNode
        
        for adjacent_node_edge in current_node.adjacent_nodes:
            edge_cost = adjacent_node_edge[0]
            edge_cost: float

            adjacent_node = adjacent_node_edge[1]
            adjacent_node: DefaultAStar.AStarEnvironmentNode
            
            if adjacent_node in closed_list or not adjacent_node.passable:
                continue
            else:
                already_updated_node = False
                temp_cost_to_node = current_node.cost_from_start + edge_cost
                for j in range(len(open_list)):
                    # if the coordinates are the same
                    if adjacent_node.x_coord == open_list[j].x_coord and adjacent_node.y_coord == open_list[j].y_coord:
                        if temp_cost_to_node < open_list[j].cost_from_start:
                            open_list[j].cost_from_start = temp_cost_to_node
                            open_list[j].heuristic_value = DefaultAStar.get_h_value(open_list[j].coord_tuple, end_node.coord_tuple)
                            open_list[j].cost_to_end = open_list[j].cost_from_start + open_list[j].heuristic_value
                            open_list[j].previous_node = current_node
                        already_updated_node = True

                if not already_updated_node:
                    adjacent_node.cost_from_start = temp_cost_to_node
                    adjacent_node.heuristic_value = DefaultAStar.get_h_value(adjacent_node)
                    adjacent_node.cost_to_end = adjacent_node.cost_from_start + adjacent_node.heuristic_value
                    adjacent_node.previous_node = current_node
                    open_list.append(adjacent_node)

        return open_list, closed_list, current_node, output_path

    def pop_node_from_list(open_list: "list[DefaultAStar.AStarEnvironmentNode]", current_node: AStarEnvironmentNode):
        for i in range(len(open_list)):
            if open_list[i] == current_node:
                open_list.pop(i)
                break
        return open_list

    def get_h_value(node_coords: tuple, dest_cell_coords: tuple) -> int: 
        return abs(node_coords[0] - dest_cell_coords[0]) + abs(node_coords[1] - dest_cell_coords[1])


    def return_path() -> None:
        pass