from src.RobotData import RobotData
from src.Algorithms import Algorithm, DefaultAStar, EnergyCostAStar
from src.EnvironmentData import EnvironmentGraph, EnvironmentNode



class AlgorithmComparisonTool:
    def __init__(self) -> None:

        self.robot_data = None
        self.supported_algorithms = {
            "A*": DefaultAStar,
            "Energy Cost A*": EnergyCostAStar
        }

    def set_robot_data(self, robot_data_filepath: str):
        try:
            self.robot_data = RobotData(robot_data_filepath)
        except Exception as exc:
            self.robot_data = None
            print(exc)

    # Universal function to run any supported algorithm
    def run_algorithm(self, algorithm_name: str, env_graph: EnvironmentGraph, start_cell_coords:tuple, end_cell_coords:tuple) -> "tuple(list, bool, str)":
        successfully_ran: bool = False
        return_message = ""
        output_path = []
        try:
            alg_obj: Algorithm = self.supported_algorithms[algorithm_name]()
            output_path = alg_obj.run(env_graph, start_cell_coords, end_cell_coords)
            
            return_message = f"{algorithm_name} Algorithm ran successfully"
            successfully_ran = True
        except KeyError:
            return_message = f"Failed to find algorithm with name: {algorithm_name}.\nSupported algorithm names:\n"
            for alg_name in self.supported_algorithms.keys():
                return_message += f"{alg_name}\n"

        return output_path, successfully_ran, return_message

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


        path, run_success, return_msg = self.run_algorithm("A*", start_cell, end_cell)
        if not run_success:
            print(f"Algorithm run failed for reason: {return_msg}")
        for node in path:
            print(f"({node.x_coord}, {node.y_coord})")



if __name__ == "__main__":
    tool_obj = AlgorithmComparisonTool()
    tool_obj.main()