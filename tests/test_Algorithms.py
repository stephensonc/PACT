from Algorithms import DefaultAStar, EnergyCostAStar
from EnergyCostUtility import calculate_energy_cost
from EnvironmentData import EnvironmentGraph, EnvironmentNode
from RobotData import RobotData


def test_pop_node():

    node_to_remove = DefaultAStar.AStarEnvironmentNode(
        EnvironmentNode(
            0,
            1,
            13.42,
            True
        )
    )

    control_node = DefaultAStar.AStarEnvironmentNode(
        EnvironmentNode(
            1,
            0,
            18.0,
            True
        )
    )

    open_list = [
        control_node,
        node_to_remove
        ]

    alg = DefaultAStar()

    open_list = alg.pop_node_from_list(open_list, node_to_remove)
    assert len(open_list) == 1
    assert open_list[0].elevation == 18.0


def test_AStarEnvironmentNode():
    node = EnvironmentNode(0,0,30.12)
    astar_node = DefaultAStar.AStarEnvironmentNode(node)

    assert astar_node.x_coord == node.x_coord
    assert astar_node.y_coord == node.y_coord
    
    assert len(astar_node.adjacent_edges) == len(node.adjacent_edges)

def test_start_pathing():
    graph = EnvironmentGraph(3, 3)

    
    nodes = [
        EnvironmentNode(0, 0, 10.1),
        EnvironmentNode(0, 1, 15.3),
        EnvironmentNode(0, 2, 18.4),
        EnvironmentNode(1, 0, 10.3, passable=False),
        EnvironmentNode(1, 1, 14.2, passable=False),
        EnvironmentNode(1, 2, 5.5, passable=False),
        EnvironmentNode(2, 0, 4.0),
        EnvironmentNode(2, 1, 6.7),
        EnvironmentNode(2, 2, 8.9)
    ]

    nodes = [DefaultAStar.AStarEnvironmentNode(node) for node in nodes]
    for node in nodes:
        graph.add_node(node)

    graph.update_adjacent_nodes()

    start_cell = (0,1)
    end_cell = (2, 1)

    alg = DefaultAStar()

    open_list, closed_list, current_node, path = alg.start_pathing(nodes, [], nodes[0], nodes[1])
    
    assert open_list is not None
    assert closed_list is not None
    assert current_node is not None
    assert len(closed_list) == 1


def test_get_num_nodes_to_find():
    node1 = EnergyCostAStar.EnergyCostAStarEnvironmentNode(EnvironmentNode(0,0,1.0))
    node2 = EnergyCostAStar.EnergyCostAStarEnvironmentNode(EnvironmentNode(50,50,1.0))
    alg = EnergyCostAStar(RobotData("robot_data/robot_example.yml"))
    assert alg.get_num_nodes_to_find(node1, node2) == 8

def test_energy_get_h_value():
    env = EnvironmentGraph(2, 2)
    nodes = [
        [
            EnvironmentNode(0,0, 1.0, 1),
            EnvironmentNode(1,0, 1.0, 1)
        ],
        [
            EnvironmentNode(0,1, 1.0, 1),
            EnvironmentNode(1,1, 1.0, 1)
        ]
    ]
    alg = EnergyCostAStar(RobotData("robot_data/robot_example.yml"))
    env.nodes = nodes

    alg.env_grid = env

    expected_h_value = calculate_energy_cost(env.nodes[0][0], env.nodes[1][1], alg.robot_data_obj)
    assert alg.get_h_value(env.nodes[0][0], env.nodes[1][1]) == expected_h_value
    
