
import pytest
from src.EnvironmentData import EnvironmentGraph, EnvironmentNode

from src.AlgorithmComparisonTool import AlgorithmComparisonTool


def test_run_algorithm():
    comparison_tool = AlgorithmComparisonTool()

    graph = EnvironmentGraph(3, 3)

        
    nodes = [
        EnvironmentNode(0, 0, 10.1),
        EnvironmentNode(0, 1, 15.3),
        EnvironmentNode(0, 2, 18.4),
        EnvironmentNode(1, 0, 10.3),
        EnvironmentNode(1, 1, 14.2, passable=False),
        EnvironmentNode(1, 2, 5.5, passable=False),
        EnvironmentNode(2, 0, 4.0),
        EnvironmentNode(2, 1, 6.7),
        EnvironmentNode(2, 2, 8.9)
    ]

    start_cell = (0,1)
    end_cell = (2, 1)

    for node in nodes:
        graph.add_node(node)

    path, run_successful, return_msg = comparison_tool.run_algorithm("YEET", graph, start_cell, end_cell)

    assert len(path) == 0
    assert not run_successful
    assert "Failed to find algorithm with name" in return_msg


    path, run_successful, return_msg = comparison_tool.run_algorithm("A*", graph, start_cell, end_cell)

    assert len(path) == 3
    assert run_successful
    assert "ran successfully" in return_msg