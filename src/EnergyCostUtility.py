from EnvironmentData import EnvironmentNode
from RobotData import RobotData
import math


def calculate_energy_cost(node1: EnvironmentNode, node2: EnvironmentNode, robot_data_obj: RobotData):
    cost = 5.0
    cost: float
    
    return cost

def calculate_velocity_on_slope(angle, robot_weight) -> float:
    
    
    pass

def calculate_driving_force() -> float:
    pass

def calculate_total_inertia() -> float:
    pass

def calculate_grav_force_of_incline(robot_mass_kg: float, slope_angle_deg: float) -> float:
    gravity_accel = 9.81
    distributed_mass = robot_mass_kg/2

    slope_force = distributed_mass * gravity_accel * math.sin(math.radians(slope_angle_deg))
    return slope_force

def calculate_combined_motor_torque() -> float:
    pass

def calculate_motor_angular_velocity() -> float:
    pass