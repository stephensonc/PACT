import os

from EnvironmentData import EnvironmentGraph
class NavMenu:

    def __init__(self, supported_algorithm_names:"list[str]") -> None:

        self.env_created: bool = False
        self.env_dimensions: tuple = (0,0)
        self.supported_alg_names = supported_algorithm_names

        self.menu_options = {
            "Create Environment" : self.create_env_selected,
            # "Modify Environment" : self.modify_env,
            "Add Algorithm to Run" : self.add_algorithm_selected,
            "Run Selected Algorithms" : self.run_algorithms,
            "Exit" : exit
        }
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
        if choice.lower() == "exit":
            exit()
        if self.selection_is_valid_option(choice):
            return self.menu_options[choice]()
        else:
            self.reset_menu()
            return self.select_option(input(f"{choice} is not a valid option, please enter another: "))

    
    def selection_is_valid_option(self, choice: str):
        return choice in self.menu_options.keys()
    
    # Add algorithm to the comparison

    def add_algorithm_selected(self):
        algorithm_name = input("Please enter ")
        if algorithm_name in self.supported_alg_names:
            self.algorithms_to_run.append(algorithm_name)
        else:
            self.reset_menu()
            print(f"Failed to find algorithm: {algorithm_name}")


    def prompt_for_coords(self):
        start_coord_string = input("Please enter the start coordinates, separated by a comma: ")
        end_coord_string = input("Please enter the end coordinates, separated by a comma: ")

        print(start_coord_string)
        print(end_coord_string)

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

    def modify_env():
        return

    def run_algorithms(self):
        return

    