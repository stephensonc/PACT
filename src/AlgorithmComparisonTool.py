from Algorithms import DefaultAStar
from EnvironmentData import EnvironmentGraph, EnvironmentNode


supported_algorithms = {
    "A*": DefaultAStar
}


def main():
    graph = EnvironmentGraph(3, 3)

    
    nodes = [
        EnvironmentNode(0, 0, 10.1),
        EnvironmentNode(0, 1, 15.3),
        EnvironmentNode(0, 2, 18.4),
        EnvironmentNode(1, 0, 10.3, True),
        EnvironmentNode(1, 1, 14.2, False),
        EnvironmentNode(1, 2, 5.5, False),
        EnvironmentNode(2, 0, 4.0),
        EnvironmentNode(2, 1, 6.7),
        EnvironmentNode(2, 2, 8.9)
    ]
    for node in nodes:
        graph.add_node(node)

    graph.update_adjacent_nodes()
    graph.print()

    start_cell = (0,1)
    end_cell = (2, 1)

    path = DefaultAStar.run(graph, start_cell, end_cell)
    for node in path:
        print(f"({node.x_coord}, {node.y_coord})")



if __name__ == "__main__":
    main()