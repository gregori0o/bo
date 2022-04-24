from base_structure import Graph
from initial_solution import CreateSolution
from json_parser import Parser


def main():
    _parser = Parser("../utils/graphs/g1.json")
    interchange_points = _parser.get_interchange_points()
    size = _parser.get_size()
    edges = _parser.get_edges()
    graph = Graph(size)
    for i, j, w in edges:
        graph.add_edge(i, j, w)
    graph.set_interchange_points(interchange_points)
    init = CreateSolution(graph)
    lines, buses = init.create_init_solution(3, 20)
    print(size, edges, interchange_points, lines, buses)


if __name__ == '__main__':
    main()
