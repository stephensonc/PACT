import math
import random
from EnergyCostUtility import calculate_energy_cost
from RobotData import RobotData
from Algorithms import Algorithm, DefaultAStar, EnergyCostAStar
from EnvironmentData import EnvironmentGraph, EnvironmentNode



class AlgorithmComparisonTool:
    def __init__(self) -> None:
        self.robot_data = None
        self.supported_algorithms = {
            "A*": DefaultAStar,
            "Energy Cost A*": EnergyCostAStar
        }        
        self.set_robot_data()

    def set_robot_data(self, robot_data_filepath: str = "robot_data/robot_example.yml"):
        try:
            self.robot_data = RobotData(robot_data_filepath)
        except Exception as exc:
            self.robot_data = RobotData() # Auto-corrects to default path
            print(exc)

    # Universal function to run any supported algorithm
    def run_algorithm(self, algorithm_name: str, env_graph: EnvironmentGraph, start_cell_coords:tuple, end_cell_coords:tuple) -> "tuple(list, bool, str)":
        successfully_ran: bool = False
        return_message = ""
        output_path = []

        print(f"Running algorithm: {algorithm_name}")
        try:
            alg_obj: Algorithm = self.supported_algorithms[algorithm_name](self.robot_data)
            output_path = alg_obj.run(env_graph, start_cell_coords, end_cell_coords)
            
            return_message = f"{algorithm_name} Algorithm ran successfully"
            successfully_ran = True
        except KeyError:
            return_message = f"Failed to find algorithm with name: {algorithm_name}.\nSupported algorithm names:\n"
            for alg_name in self.supported_algorithms.keys():
                return_message += f"{alg_name}\n"

        return output_path, successfully_ran, return_message

    def calculate_energy_cost_of_path(self, final_path: "list[tuple(int, int)]") -> float:
        path_costs = self.calculate_individual_path_costs(final_path)
        return sum(path_costs)
    
    def calculate_individual_path_costs(self, final_path: "list[tuple(int, int)]") -> "list[float]":
        costs = []
        for i in range(len(final_path) - 1):
            node1 = final_path[i]
            node2 = final_path[i + 1]
            path_cost = calculate_energy_cost(node1, node2, self.robot_data)
            costs.append(path_cost)
        return costs

    def auto_generate_graph(self, length, width) -> EnvironmentGraph:
        elevations = []
        for i in range(length * width):
            elevations.append(float(random.randint(0, 300))/10)

        friction_coefficients = []
        for i in range(length * width):
            friction_coefficients.append(float(random.randint(1, 40))/10)

        return self.create_graph(length, width, elevations, friction_coefficients)

    def create_graph(self, length: int, width: int, elevation_values: "list[float]", friction_coefficients: "list[float]") -> EnvironmentGraph:
        graph = EnvironmentGraph(length, width)
        if len(elevation_values) != length * width or len(friction_coefficients) != length * width:
            print("Number of elevation values or friction coefficients not equal to number of nodes")
            return None
        else:
            idx = 0
            for row in graph.nodes:
                for node in row:
                    graph.nodes[node.x_coord][node.y_coord] = EnvironmentNode(node.x_coord, node.y_coord, elevation_values[idx], friction_coefficients[idx])
                    idx += 1        
        return graph



    def main(self):
        graph = EnvironmentGraph(3, 3)

        
        nodes = [
            EnvironmentNode(0, 0, 10.1),
            EnvironmentNode(0, 1, 15.3),
            EnvironmentNode(0, 2, 18.4),
            EnvironmentNode(1, 0, 10.3),
            EnvironmentNode(1, 1, 14.2, passable=False),
            EnvironmentNode(1, 2, 5.5, passable=False),
            EnvironmentNode(2, 0, 4.0),
            EnvironmentNode(2, 1, 6.7),
            EnvironmentNode(2, 2, 8.9)
        ]
        for node in nodes:
            graph.add_node(node)

        graph.update_adjacent_nodes()
        graph.print()

        start_cell = (0,1)
        end_cell = (2, 1)


        path, run_success, return_msg = self.run_algorithm("A*", graph, start_cell, end_cell)
        if not run_success:
            print(f"Algorithm run failed for reason: {return_msg}")
        for node in path:
            print(f"({node.x_coord}, {node.y_coord})")

        path_costs = self.calculate_individual_path_costs(path)
        for path_cost in path_costs:
            print(path_cost)


        path, run_success, return_msg = self.run_algorithm("Energy Cost A*", graph, start_cell, end_cell)
        if not run_success:
            print(f"Algorithm run failed for reason: {return_msg}")
        for node in path:
            print(f"({node.x_coord}, {node.y_coord})")
        path_costs = self.calculate_individual_path_costs(path)
        for path_cost in path_costs:
            print(path_cost)

if __name__ == "__main__":
    tool_obj = AlgorithmComparisonTool()
    tool_obj.main()