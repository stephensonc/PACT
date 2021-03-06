import json
import os
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from EnergyCostUtility import calculate_energy_cost, calculate_time_to_traverse
from NavMenu import NavMenu
from RobotData import RobotData
from Algorithms import Algorithm, DefaultAStar, EnergyCostAStar
from EnvironmentData import EnvironmentGraph, EnvironmentNode, distance_between_nodes



class AlgorithmComparisonTool:
    def __init__(self) -> None:
        self.robot_data = None
        self.supported_algorithms = {
            "A*": DefaultAStar,
            "Energy Cost A*": EnergyCostAStar
        }        
        self.set_robot_data()
        self.env_graph = None

    def set_robot_data(self, robot_data_filepath: str = "robot_data/robot_example_2.yml"):
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




    # Path diagnostic data

    def calculate_distance_of_path(self, final_path: "list[EnvironmentNode]") -> float:
        path_costs = self.calculate_individual_path_distances(final_path)
        total_cost = 0
        for cost in path_costs:
            total_cost += cost
        return total_cost
    
    def calculate_individual_path_distances(self, final_path: "list[EnvironmentNode]") -> "list[float]":
        costs = []
        for i in range(len(final_path) - 1):
            node1 = final_path[i]
            node2 = final_path[i + 1]
            path_cost = distance_between_nodes(node1, node2)
            costs.append(path_cost)
        return costs

    def calculate_energy_cost_of_path(self, final_path: "list[EnvironmentNode]") -> float:
        path_costs = self.calculate_individual_path_costs(final_path)
        total_cost = 0
        for cost in path_costs:
            total_cost += cost
        return total_cost
    
    def calculate_individual_path_costs(self, final_path: "list[EnvironmentNode]") -> "list[float]":
        costs = []
        for i in range(len(final_path) - 1):
            node1 = final_path[i]
            node2 = final_path[i + 1]
            path_cost = calculate_energy_cost(node1, node2, self.robot_data)
            costs.append(path_cost)
        return costs
    
    def calculate_time_to_traverse(self, final_path):
        robot_data = self.robot_data

        total_time = 0.0
        individual_path_distances = self.calculate_individual_path_distances(final_path)

        for dist in individual_path_distances:
            total_time += calculate_time_to_traverse(dist, robot_data.avg_movespeed, robot_data.avg_movespeed/1.5)
        return total_time


    def get_path_diagnostic_data(self, final_path: "list[tuple[int]]"):
        total_distance = self.calculate_distance_of_path(final_path)
        total_energy_cost = self.calculate_energy_cost_of_path(final_path)
        time_to_traverse = self.calculate_time_to_traverse(final_path)

        output_dict = {
            "total_distance": total_distance,
            "total_energy_cost": total_energy_cost,
            "time_to_traverse": time_to_traverse
        }


        return output_dict


    # End Path diagnostic data



    def auto_create_uniform_graph(self, width, height) -> EnvironmentGraph:
        elevations = []
        for i in range(width):
            row = []
            for j in range(height):
                row.append(1.0)
            elevations.append(row)

        friction_coefficients = []
        for i in range(width):
            row = []
            for j in range(height):
                coeff = 1.0
                row.append(coeff)
                # print(coeff)
            friction_coefficients.append(row)

        return self.create_graph(width, height, elevations, friction_coefficients)

    def auto_create_graph(self, width, height) -> EnvironmentGraph:
        elevations = []
        for i in range(width):
            row = []
            for j in range(height):
                row.append(float(random.randint(1, 6)))
            elevations.append(row)

        friction_coefficients = []
        for i in range(width):
            row = []
            for j in range(height):
                coeff = float(random.randint(1, 12))/10
                row.append(coeff)
                # print(coeff)
            friction_coefficients.append(row)

        return self.create_graph(width, height, elevations, friction_coefficients)


    # Fills elevations and friction by columns first
    def create_graph(self, width: int, height: int, elevation_values: "list[list[float]]", friction_coefficients: "list[list[float]]") -> EnvironmentGraph:
        graph = EnvironmentGraph(width, height)


        if len(elevation_values) * len(elevation_values[0]) != width * height or len(friction_coefficients) * len(friction_coefficients[0]) != width * height:
            print("Number of elevation values or friction coefficients not equal to number of nodes")
            return None
        else:
            for x in range(len(graph.nodes)):
                for y in range(len(graph.nodes[x])):
                    graph.nodes[x][y] = EnvironmentNode(x, y, elevation_values[x][y], friction_coefficients[x][y]) 
        graph.update_adjacent_nodes()   
        return graph


    def plot_paths(self, paths: dict):
        figure = plt.figure()
        axes = plt.axes(projection='3d')
        axes.set_title("Map: Paths taken to objective")

        

        for alg_name in paths.keys():
            x_coords = np.array([coord_tuple[0] for coord_tuple in paths[alg_name]])
            y_coords = np.array([coord_tuple[1] for coord_tuple in paths[alg_name]])
            z_coords = np.array([coord_tuple[2] for coord_tuple in paths[alg_name]])
            # plt.plot(x_coords, y_coords, z_coords, label=alg_name)
            axes.plot3D(x_coords, y_coords, z_coords, zorder=10, label=alg_name, linewidth=5)

        # x_values = np.linspace(0, len(self.env_graph.nodes), len(self.env_graph.nodes))
        # y_values = np.linspace(0, len(self.env_graph.nodes[0]), len(self.env_graph.nodes[0]))


        start_coords = paths[list(paths.keys())[0]][0]
        end_coords = paths[list(paths.keys())[0]][-1]
        x_values = np.linspace(start_coords[0], end_coords[0], abs(end_coords[0] - start_coords[0]) + 1)
        y_values = np.linspace(start_coords[1], end_coords[1], abs(end_coords[1] - start_coords[1]) + 1)
        
        node_elevations = []
        for x in range(start_coords[0], end_coords[0] + 1):
            node_coords = []
            for y in range(start_coords[1], end_coords[1] + 1):
                node = self.env_graph.nodes[x][y]
                node_coords.append(node.elevation)
            node_elevations.append(node_coords)
        
        X, Y = np.meshgrid(x_values, y_values)
        Z = np.array(node_elevations)

        surface = axes.plot_surface(X, Y, Z, zorder=0,cmap=cm.get_cmap('Greys'), linewidth=0, label="surface")
        # surface = axes.plot_wireframe(X, Y, Z, color="green", linewidth=1, label="surface")

        surface._facecolors2d=surface._facecolor3d
        surface._edgecolors2d=surface._edgecolor3d
        # figure.colorbar(surface, shrink=0.5, aspect=5)

        axes.set_xlabel("X coordinate (meters)")
        axes.set_ylabel("Y coordinate (meters)")
        axes.set_zlabel("Elevation (meters)")
        axes.legend(paths.keys())
        plt.show()

    
    def write_env_to_file(self, filename: str):
        env_path = "stored_environments"

        filename = filename if ".json" in filename else filename + ".json"
        path_divider = "\\" if os.name == "nt" else "/"
        env_dict = self.env_graph.get_dict_form()

        with open(env_path + path_divider + filename, "w") as file:
            json.dump(env_dict, file)


    def run_tool(self):


        supported_alg_names = self.supported_algorithms.keys()
        
        menu = NavMenu(supported_alg_names)

        choice = ""
        while choice.lower() != "exit":
            menu.reset_menu()
            choice = input("Please choose a menu option by typing in its label: ")
            option_output = menu.select_option(choice)
            int_choice, is_int = try_parse_int(choice)

            if is_int and int_choice in menu._menu_relationship_map.keys():
                choice = menu._menu_relationship_map[int_choice]

            if choice == "Create Environment":
                graph_width = menu.env_dimensions[0]
                graph_height = menu.env_dimensions[1]
                self.env_graph = self.auto_create_graph(graph_width, graph_height)
            if choice == "Import Environment from File":
                self.env_graph = self.create_graph(menu.env_dimensions[0], menu.env_dimensions[1], menu.env_elevations, menu.env_fric_coeffs)

            if choice == "Export Environment to File":
                self.write_env_to_file(option_output) # option_output will be the filename


            if choice == "Run Selected Algorithms":
                
                start_cell, end_cell = menu.prompt_for_coords()
                # print(start_cell)
                # print(end_cell)


                paths = {}
                for alg in menu.algorithms_to_run:
                    start_time = time.time()

                    path, run_success, return_msg = self.run_algorithm(alg, self.env_graph, start_cell, end_cell)

                    end_time = time.time()

                    if not run_success:
                        print(f"Algorithm run failed for reason: {return_msg}")

                    else:
                        path_diagnostic_data = self.get_path_diagnostic_data(path)

                        total_distance = round(path_diagnostic_data['total_distance'], 2)
                        total_energy_cost = round(path_diagnostic_data['total_energy_cost'], 2)
                        traversal_time = round(path_diagnostic_data['time_to_traverse'], 2)

                        
                        
                        print(f"Total distance traveled: {total_distance} meters")
                        print(f"Total energy cost: {total_energy_cost} Joules")
                        print(f"Total time to traverse path: {traversal_time} seconds")
                        print(f"Time taken to run algorithm: {round(end_time - start_time, 2)} seconds")
                        print()
                        
                        path_coords = [(node.x_coord, node.y_coord, node.elevation) for node in path]
                        paths.update({alg: path_coords}) # algorithm name, path
                    # for node in path:
                    #     print(f"({node.x_coord}, {node.y_coord})") 

                self.plot_paths(paths)
                    
                input("Press enter to continue: ")



    def main(self):

        width = 5
        height = 4

        test_elevations = [
            [7.0, 48.3, 47.2, 46.6],
            [8.0, 8.0, 10.3, 14.2],
            [9.3, 55.8, 13.8, 10.0],
            [8.0, 13.3, 6.2, 14.1],
            [8.0, 35.4, 13.7, 20.0]
        ]

        test_friction_coefficients = []
        for i in range(width):
            row = []
            for j in range(height):
                row.append(1.0)
            test_friction_coefficients.append(row)

        # graph = self.create_graph(width, height, test_elevations, test_friction_coefficients)
        graph = self.auto_create_graph(width, height)

        graph.update_adjacent_nodes()
        graph.print()

        start_cell = (2,0)
        end_cell = (3, 2)
        # end_cell = (int(width/2), int(height/3))

        path, run_success, return_msg = self.run_algorithm("A*", graph, start_cell, end_cell)
        if not run_success:
            print(f"Algorithm run failed for reason: {return_msg}")
        for node in path:
            print(f"({node.x_coord}, {node.y_coord})")

        path_costs = self.calculate_individual_path_costs(path)
        # for path_cost in path_costs:
        #     print(path_cost)
        print("Total energy cost:", self.calculate_energy_cost_of_path(path))

        path, run_success, return_msg = self.run_algorithm("Energy Cost A*", graph, start_cell, end_cell)
        if not run_success:
            print(f"Algorithm run failed for reason: {return_msg}")
        for node in path:
            print(f"({node.x_coord}, {node.y_coord})")
        path_costs = self.calculate_individual_path_costs(path)
        # for path_cost in path_costs:
        #     print(path_cost)

        print("Total energy cost:", self.calculate_energy_cost_of_path(path))

def try_parse_int(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

if __name__ == "__main__":
    tool_obj = AlgorithmComparisonTool()
    tool_obj.run_tool()