from RobotData import RobotData


def test_RobotData():
    robot_data_obj = RobotData("robot_data/robot_example.yml")

    attributes = [
        robot_data_obj.kg_weight,
        robot_data_obj.roll_friction_coefficient,
        robot_data_obj.avg_movespeed,
        robot_data_obj.max_movespeed,
        robot_data_obj.max_passable_slope
        ]

    for attr in attributes:
        assert attr is not None

    assert robot_data_obj.kg_weight == 30.5
    assert robot_data_obj.roll_friction_coefficient == 0.1
    assert robot_data_obj.avg_movespeed == 7.3
    assert robot_data_obj.max_movespeed == 10.0
    assert robot_data_obj.max_passable_slope == 70.0