from base_structure import Graph
from json_parser import Parser
from src.solver import Solver
from graph_generator import GraphGenerator


def main():
    g = GraphGenerator(20, 22, 100)
    g.generate_graph_with_all_weights_equal()
    g.save("test")
    _parser = Parser("../utils/graphs/example.json")
    interchange_points = _parser.get_interchange_points()
    size = _parser.get_size()
    edges = _parser.get_edges()
    passengers = _parser.get_passengers()
    graph = Graph(size)
    for i, j, w in edges:
        graph.add_edge(i, j, w)
    graph.set_interchange_points(interchange_points)
    num_lines = 3
    num_buses = 20

    solver = Solver(graph, passengers, num_lines, num_buses)
    solver.visualize_solution("solution")


if __name__ == '__main__':
    main()
