from src.Algorithms import DefaultAStar
from src.EnvironmentData import EnvironmentGraph, EnvironmentNode


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

    open_list = DefaultAStar.pop_node_from_list(open_list, node_to_remove)
    assert len(open_list) == 1
    assert open_list[0].elevation == 18.0



def test_start_pathing():
    graph = EnvironmentGraph(3, 3)

    
    nodes = [
        EnvironmentNode(0, 0, 10.1),
        EnvironmentNode(0, 1, 15.3),
        EnvironmentNode(0, 2, 18.4),
        EnvironmentNode(1, 0, 10.3, False),
        EnvironmentNode(1, 1, 14.2, False),
        EnvironmentNode(1, 2, 5.5, False),
        EnvironmentNode(2, 0, 4.0),
        EnvironmentNode(2, 1, 6.7),
        EnvironmentNode(2, 2, 8.9)
    ]
    for node in nodes:
        graph.add_node(node)

    graph.update_adjacent_nodes()

    start_cell = (0,1)
    end_cell = (2, 1)

    path = DefaultAStar.run(graph, start_cell, end_cell)
    assert path is not None
    assert len(path) > 0


    
