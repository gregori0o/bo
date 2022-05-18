from base_structure import Graph
from json_parser import Parser
from graph_generator import GraphGenerator
from passengers_generator import Passengers
from tester import Tester
from config import *


def main():
    g = GraphGenerator(30, 120, 30)
    g.generate_graph_with_all_weights_equal()
    g.save("test")
    _parser = Parser("../utils/graphs/example.json")
    interchange_points = _parser.get_interchange_points()
    size = _parser.get_size()
    edges = _parser.get_edges()
    passengers = _parser.get_passengers()
    if not passengers:
        passengers = Passengers(size, 100).travels
    graph = Graph(size)
    for i, j, w in edges:
        graph.add_edge(i, j, w)
    graph.set_interchange_points(interchange_points)

    num_lines = 3
    num_buses = 20
    kwargs = config

    num_tests = 2
    criterion = criterion2
    tester = Tester(graph, passengers, num_lines, num_buses, **kwargs)
    tester.test(num_tests, criterion)


if __name__ == '__main__':
    main()
