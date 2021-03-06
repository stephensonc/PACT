import os
import yaml
import math

class RobotData:

    def __init__(self, robot_yml_filepath: str = ""):

        self.has_all_data = False

        self.kg_weight = None
        self.roll_friction_coefficient = None
        self.wheel_radius = None
        self.wheel_power_efficiency = None
        self.drivetrain_gear_ratio = None
        self.avg_movespeed = None
        self.max_movespeed = None
        self.max_passable_slope = None
        self.wheel_circumference = None

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
                    self.number_of_wheels = data_dict["number_of_wheels"]
                    self.roll_friction_coefficient = data_dict["wheel_roll_friction_coefficient"]
                    self.wheel_radius = data_dict["wheel_radius_meters"]
                    self.wheel_voltage = data_dict["individual_wheel_voltage"]
                    self.wheel_power_efficiency = data_dict["individual_wheel_power_efficiency"] if "individual_wheel_power_efficiency" in data_dict.keys() else 1
                    self.drivetrain_gear_ratio = data_dict["drivetrain_gear_ratio"]
                    self.avg_movespeed = data_dict["average_movespeed_m/s"]
                    self.max_movespeed = data_dict["max_movespeed_m/s"]
                    self.max_passable_slope = data_dict["max_passable_slope"]

                    self.wheel_circumference = self.calculate_wheel_circumference(self.wheel_radius)

                    self.has_all_data = True
                except KeyError as exc:
                    print(exc)
                    input("An error has occured during robot data collection, please hit enter to return to the menu")
        except FileNotFoundError as exc:
            print(exc)
            print("File not found, here is a list of the available files in the robot_data folder:")
            for filename in os.listdir("robot_data"):
                print(filename)

    def calculate_wheel_circumference(self, radius: float) -> float:
        return 2 * math.pi * radius
            