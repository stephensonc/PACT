import yaml

class RobotData:

    def __init__(self, robot_yml_filepath: str = "robot_data/robot_example.yml"):

        self.has_all_data = False

        self.kg_weight = None
        self.friction_coefficient = None
        self.avg_movespeed = None
        self.max_movespeed = None
        self.max_passable_slope = None

        self.set_data(robot_yml_filepath)

        if self.max_passable_slope is None:
            self.max_passable_slope = 70.0
        else:
            self.has_all_data = True

    def set_data(self, robot_yml_filepath: str):
        try:
            with open(robot_yml_filepath) as file:
                data_dict = {}
                try:
                    data_dict = yaml.safe_load(file)
                except yaml.YAMLError as exc:
                    print(exc)

                try:
                    self.kg_weight = data_dict["weight_in_kg"]
                    self.friction_coefficient = data_dict["wheel_friction_coefficient"]
                    self.avg_movespeed = data_dict["average_movespeed_m/s"]
                    self.max_movespeed = data_dict["max_movespeed_m/s"]
                    self.max_passable_slope = data_dict["max_passable_slope"]
                    self.has_all_data = True
                except KeyError as exc:
                    print(exc)
        except FileNotFoundError as exc:
            print(exc)

            