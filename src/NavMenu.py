import os
import json
from EnvironmentData import EnvironmentGraph, EnvironmentNode
class NavMenu:

    def __init__(self, supported_algorithm_names:"list[str]") -> None:

        self.env_created: bool = False
        self.env_dimensions: tuple = (0,0)
        self.env_elevations = []
        self.env_fric_coeffs = []

        self.supported_alg_names = supported_algorithm_names

        self.menu_options = {
            "Create Environment" : self.create_env_selected,
            "Import Environment from File" : self.import_env,
            "Export Environment to File" : self.prompt_for_output_filename,
            "Add Algorithm to Run" : self.add_algorithm_selected,
            "Run Selected Algorithms" : self.run_algorithms, # Currently handled by AlgorithmComparisonTool
            "Exit" : exit
        }

        self._menu_relationship_map = {}
        item_idx = 1
        for menu_item in self.menu_options.keys():
            self._menu_relationship_map.update({item_idx: menu_item})
            item_idx += 1

        self.algorithms_to_run = ["A*", "Energy Cost A*"]

    def clear_menu(self):
        # nt represents windows
        os.system('cls' if os.name == 'nt' else 'clear')

    def reset_menu(self):
        self.clear_menu()
        self.print_menu()
    
    def print_menu(self):

        print("Algorithm Comparison Tool")

        env_status_text = "not set" if not self.env_created else f"Set to environment with dimensions {self.env_dimensions}"
    
        print(f"Environment Selected: {env_status_text}")

        print(f"Algorithms Selected: " + ", ".join([x for x in self.algorithms_to_run]))

        item_idx = 1
        for menu_item in self.menu_options.keys():
            print(f"{item_idx}. {menu_item}")
            item_idx += 1

    def select_option(self, choice: str):
        # if choice.lower() == "exit" or (int(choice) in self._menu_relationship_map.keys() and self._menu_relationship_map[int(choice)] == "Exit"):
        #     exit()
        choice, is_int = try_parse_int(choice)
        if self.selection_is_valid_option(choice):
            if is_int:
                return self.menu_options[self._menu_relationship_map[int(choice)]]()
            else:
                return self.menu_options[choice]()
        else:
            self.reset_menu()
            return self.select_option(input(f"{choice} is not a valid option, please enter another: "))

    
    def selection_is_valid_option(self, choice: str):
        choice, is_int = try_parse_int(choice)
        if is_int:
            return choice in self._menu_relationship_map.keys()
        else:
            return choice in self.menu_options.keys()

    # Add algorithm to the comparison

    def add_algorithm_selected(self):
        algorithm_name = input("Please enter algorithm name: ")
        if algorithm_name in self.supported_alg_names:
            self.algorithms_to_run.append(algorithm_name)
        else:
            self.reset_menu()
            print(f"Failed to find algorithm: {algorithm_name}")


    def prompt_for_coords(self):
        start_coord_string = input("Please enter the start coordinates, separated by a comma: ")
        end_coord_string = input("Please enter the end coordinates, separated by a comma: ")

        # print(start_coord_string)
        # print(end_coord_string)

        start_coord_tuple = tuple([int(x) for x in start_coord_string.split(",")])
        end_coord_tuple = tuple([int(x) for x in end_coord_string.split(",")])
        # print(start_coord_tuple)
        # print(end_coord_tuple)

        return start_coord_tuple, end_coord_tuple

    # End Add algorithm handling


    # Create Env selected

    def create_env_selected(self):
        self.env_created = True
        env_width = int(input("Please enter the environment width (int)(x axis): "))
        env_height = int(input("Please enter the environment height (int)(y axis): "))
        self.env_dimensions = (env_width, env_height)
        return env_width, env_height


    # End Create Env handling

    def import_env(self):
        env_data_path = "stored_environments"
        path_divider = "\\" if os.name == "nt" else "/"

        print("Environment files found: ", end="")
        for file in os.listdir(env_data_path):
            print(file)
        print("\n")
        filename = input("Please enter the filename for the environment: ")

        file_path = env_data_path + path_divider + filename
        
        env_data_dict = None

        with open(file_path) as file:
            env_data_dict = json.load(file)
        
        self.env_dimensions = (env_data_dict["width"], env_data_dict["height"])
        self.env_elevations = env_data_dict["elevations"]
        self.env_fric_coeffs = env_data_dict["friction_coefficients"]

        self.env_created = True

    
    

    def prompt_for_output_filename(self):
        return input("Please enter a filename for the environment file: ")
    
    def run_algorithms(self):
        return

def try_parse_int(value):
    try:
        return int(value), True
    except ValueError:
        return value, False