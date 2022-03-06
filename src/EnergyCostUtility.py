from platform import node
from EnvironmentData import EnvironmentNode, calculate_incline_angle_degrees, distance_between_nodes
from RobotData import RobotData
import math


GRAVITY_ACCEL = 9.81


def calculate_energy_cost(node1: EnvironmentNode, node2: EnvironmentNode, robot_data_obj: RobotData) -> float:
    cost = 0.0

    robot_mass = robot_data_obj.kg_weight
    wheel_radius = robot_data_obj.wheel_radius
    wheel_circumference = robot_data_obj.wheel_circumference

    

    incline_angle_deg = calculate_incline_angle_degrees(node1, node2)
    velocity = robot_data_obj.avg_movespeed
    
    # Correct the sign on the velocity to reflect upward/downward movement
    if incline_angle_deg < 0:
        velocity = 0 - velocity

    travel_distance = distance_between_nodes(node1, node2)
    
    num_wheel_rotations = calculate_required_wheel_rotations(wheel_circumference, travel_distance)
    time_taken_for_path = calculate_time_traveled(velocity, travel_distance)
    
    wheel_angular_velocity = calculate_motor_angular_velocity(num_wheel_rotations, time_taken_for_path)

    normal_force = calculate_normal_force(robot_mass, incline_angle_deg)
    force_of_gravity = calculate_grav_force_of_path(robot_mass, incline_angle_deg)
    kinetic_friction = calculate_friction_force_of_path(robot_data_obj.friction_coefficient, normal_force, velocity)

    

    combined_motor_torque = calculate_combined_motor_torque(robot_mass, wheel_angular_velocity, wheel_radius, force_of_gravity, kinetic_friction)
    power_consumed_by_one_motor = combined_motor_torque * wheel_angular_velocity


    # if power_consumed_by_one_motor < 0:
    #     print("Normal force:", normal_force)
    #     print("Angular Velocity:", wheel_angular_velocity)
    #     print("Incline angle deg:", incline_angle_deg)
    #     print("Gravity force:", force_of_gravity)
    #     print("Power consumed:", power_consumed_by_one_motor)

    cost = power_consumed_by_one_motor * robot_data_obj.number_of_wheels

    return cost

def calculate_required_wheel_rotations(wheel_circumference: float, travel_distance: float):
    return travel_distance/wheel_circumference

# Time taken to traverse the distance
def calculate_time_traveled(robot_velocity: float, distance_traveled: float) -> float:
    return distance_traveled/robot_velocity

def calculate_motor_angular_velocity(num_wheel_rotations: float, time_traveled: float) -> float:
    rotation_angle = num_wheel_rotations * 2 * math.pi
    return rotation_angle / time_traveled



# Force calculations

def calculate_grav_force_of_path(robot_mass_kg: float, slope_angle_deg: float) -> float:
    distributed_mass = robot_mass_kg/2

    slope_force = distributed_mass * GRAVITY_ACCEL * math.sin(math.radians(slope_angle_deg))
    return slope_force

def calculate_friction_force_of_path(friction_coefficient: float, normal_force: float, velocity: float) -> float:
    velocity_sign_mult = get_pos_negative_multiplier(velocity)
    return friction_coefficient * normal_force * velocity_sign_mult

def calculate_normal_force(robot_mass_kg: float, incline_angle_deg: float) -> float:
    incline_angle_rad = math.radians(incline_angle_deg)
    return robot_mass_kg * GRAVITY_ACCEL * math.cos(incline_angle_rad)

def calculate_combined_motor_torque(robot_mass: float, angular_velocity: float, wheel_radius: float, gravitation_force: float, friction_force: float) -> float:
    return ((robot_mass/2) * angular_velocity * pow(wheel_radius, 2)) + gravitation_force + friction_force


def get_pos_negative_multiplier(x: float) -> int:
    if x == 0:
        return x
    else:
        return -1 if x < 0 else 1