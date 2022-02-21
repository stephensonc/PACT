from EnvironmentData import EnvironmentNode, calculate_incline_angle_degrees
from RobotData import RobotData
import math


GRAVITY_ACCEL = 9.81

def calculate_energy_cost(node1: EnvironmentNode, node2: EnvironmentNode, robot_data_obj: RobotData):
    cost = 5.0
    cost: float

    robot_mass = robot_data_obj.kg_weight
    incline_angle_deg = calculate_incline_angle_degrees(node1, node2)

    normal_force = calculate_normal_force(robot_mass, incline_angle_deg)
    force_of_gravity = calculate_grav_force_of_path(robot_mass, incline_angle_deg)
    velocity = calculate_velocity_on_slope(robot_mass, incline_angle_deg)
    kinetic_friction = calculate_friction_force_of_path(robot_data_obj.friction_coefficient, normal_force, velocity)
    return cost

def calculate_velocity_on_slope(angle, robot_weight) -> float:
    
    
    pass

def calculate_driving_force() -> float:
    pass

def calculate_total_inertia() -> float:
    pass

def calculate_grav_force_of_path(robot_mass_kg: float, slope_angle_deg: float) -> float:
    distributed_mass = robot_mass_kg/2

    slope_force = distributed_mass * GRAVITY_ACCEL * math.sin(math.radians(slope_angle_deg))
    return slope_force

def calculate_friction_force_of_path(friction_coefficient: float, normal_force: float, velocity: float) -> float:
    velocity_sign_mult = get_pos_negative_multiplier(velocity)
    return friction_coefficient * normal_force * velocity_sign_mult

def calculate_combined_motor_torque() -> float:
    pass

def calculate_normal_force(robot_mass_kg: float, incline_angle_deg: float) -> float:
    incline_angle_rad = math.radians(incline_angle_deg)
    return robot_mass_kg * GRAVITY_ACCEL * math.cos(incline_angle_rad)


def calculate_motor_angular_velocity(combined_motor_torque: float, wheel_radius: float, robot_mass: float, incline_angle_deg: float) -> float:
    incline_angle_rad = math.radians(incline_angle_deg)
    
    pass

def get_pos_negative_multiplier(x: float) -> int:
    if x == 0:
        return x
    else:
        return -1 if x < 0 else 1