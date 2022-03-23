from platform import node
from this import d
from EnvironmentData import EnvironmentNode, calculate_incline_angle_degrees, distance_between_nodes
from RobotData import RobotData
import math


GRAVITY_ACCEL = 9.81 # m/s^2


def calculate_energy_cost(node1: EnvironmentNode, node2: EnvironmentNode, robot_data_obj: RobotData) -> float:
    incline_angle_deg = calculate_incline_angle_degrees(node1, node2)
    incline_angle_rad = math.radians(incline_angle_deg)
    travel_distance = distance_between_nodes(node1, node2)
    robot_mass = robot_data_obj.kg_weight
    robot_weight = robot_mass * GRAVITY_ACCEL

    # Wheel/motor data
    wheel_radius = robot_data_obj.wheel_radius
    wheel_roll_friction_coefficient = robot_data_obj.roll_friction_coefficient
    motor_efficiency = robot_data_obj.wheel_power_efficiency
    num_wheels = robot_data_obj.number_of_wheels

    # Drivetrain data
    expected_drivetrain_efficiency = 0.8
    drivetrain_gear_ratio = robot_data_obj.drivetrain_gear_ratio
    
    velocity = robot_data_obj.avg_movespeed # m/s
    desired_acceleration = velocity/0.5 # m/s^2 (Assumed half a second to reach full speed)
    
    motor_angular_velocity = calculate_wheel_angular_velocity(velocity, wheel_radius) # rad/s

    normal_force = calculate_normal_force(robot_mass, incline_angle_rad) # mass * cos(angle)

    # Friction types
    roll_friction = calculate_roll_friction(normal_force, wheel_roll_friction_coefficient)
    incline_friction = calculate_incline_friction(robot_weight, incline_angle_rad)
    acceleration_friction = calculate_acceleration_friction(robot_mass, desired_acceleration)

    # Torque
    combined_wheel_torque = calculate_wheel_torque(roll_friction, incline_friction, acceleration_friction, wheel_radius)
    combined_motor_torque = caclulate_combined_motor_torque(combined_wheel_torque, expected_drivetrain_efficiency, drivetrain_gear_ratio)

    continuous_power_cost = calculate_combined_power_cost(combined_motor_torque, motor_angular_velocity, motor_efficiency, expected_drivetrain_efficiency) # Watts (Joules/second)

    return continuous_power_cost * calculate_time_to_traverse(travel_distance, velocity) # Joules


def calculate_wheel_angular_velocity(velocity: float, wheel_radius: float):
    return velocity/wheel_radius

def calculate_time_to_traverse(path_distance, robot_velocity):
    return path_distance/robot_velocity


# Force calculations

def calculate_normal_force(robot_mass_kg: float, incline_angle_rad: float) -> float:
    return robot_mass_kg * GRAVITY_ACCEL * math.cos(incline_angle_rad)

def get_pos_negative_multiplier(x: float) -> int:
    if x == 0:
        return x
    else:
        return -1 if x < 0 else 1

# Friction calculations

def calculate_roll_friction(normal_force: float, wheel_roll_friction_coefficient: float):
    return normal_force * wheel_roll_friction_coefficient

def calculate_incline_friction(robot_weight: float, incline_angle_rad: float):
    return robot_weight * math.sin(incline_angle_rad)

def calculate_acceleration_friction(robot_mass: float, desired_acceleration: float) -> float:
    return robot_mass * desired_acceleration

# Torque calculations

def calculate_roll_torque(roll_friction: float, wheel_radius: float) -> float:
    return roll_friction * wheel_radius

def calculate_incline_torque(incline_friction: float, wheel_radius: float) -> float:
    return incline_friction * wheel_radius

def calculate_acceleration_torque(acceleration_friction: float, wheel_radius: float) -> float:
    return acceleration_friction * wheel_radius

def calc_torque(friction_force: float, wheel_radius: float) -> float:
    return friction_force * wheel_radius

def calculate_wheel_torque(roll_friction, incline_friction, acceleration_friction, wheel_radius):
    # Combined wheel torque
    roll_torque = calc_torque(roll_friction, wheel_radius)
    incline_torque = calc_torque(incline_friction, wheel_radius)
    acceleration_torque = calc_torque(acceleration_friction, wheel_radius)
    constant_torque = roll_torque + incline_torque
    return constant_torque + acceleration_torque

def caclulate_combined_motor_torque(wheel_torque: float, drivetrain_efficiency: float, drivetrain_gear_ratio: float) -> float:
    return (1.0/drivetrain_efficiency) * (wheel_torque/drivetrain_gear_ratio)


# Power calculations

def calculate_combined_power_cost(combined_torque, angular_velocity: float, motor_efficiency: float, drivetrain_efficiency: float):
    return combined_torque * (angular_velocity * (1.0/drivetrain_efficiency) * (1.0/motor_efficiency))