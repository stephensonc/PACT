

from src.EnvironmentData import EnvironmentGraph, EnvironmentNode, calculate_incline_angle


def test_calculate_incline_angle():
    node1 = EnvironmentNode(0, 0, 0.0)
    node2 = EnvironmentNode(0, 3, 4.0)

    angle = calculate_incline_angle(node1, node2)
    assert round(angle, 2) == 53.13

def test_EnvironmentGraph():
    graph = EnvironmentGraph(3, 3)
    graph.add_node_raw(0, 0, 33.45)

    node2 = EnvironmentNode(1, 2, 44.12)
    graph.add_node(node2)
    graph.print()

    assert graph.nodes[0][0].elevation == 33.45
    assert graph.nodes[1][2] == node2


def test_add_node():
    graph = EnvironmentGraph(2,2)
    node2 = EnvironmentNode(1, 0, 44.12)
    graph.add_node(node2)
    assert graph.nodes[1][0] == node2

def test_get_adjacent_edges():
    graph = EnvironmentGraph(2, 2)
    
    nodes = [
        EnvironmentNode(0, 0, 10.1),
        EnvironmentNode(0, 1, 15.3),
        EnvironmentNode(1, 0, 10.3),
        EnvironmentNode(1, 1, 14.2)
    ]
    for node in nodes:
        graph.add_node(node)

    graph.update_adjacent_nodes()

    assert graph.nodes[0][0] == nodes[0]
    assert len(graph.nodes[0][0].adjacent_edges) == 3

    assert len(graph.nodes[1][1].adjacent_edges) == 3
    

