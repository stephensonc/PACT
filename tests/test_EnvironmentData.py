

from src.EnvironmentData import EnvironmentGraph, EnvironmentNode


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