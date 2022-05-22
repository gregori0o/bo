from base_structure import Graph
from json_parser import Parser
from graph_generator import GraphGenerator
from passengers_generator import Passengers
from solver import Solver
from tester import Tester
from config import *
import sys


def solve(filepath):
    _parser = Parser(filepath)
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

    solver = Solver(graph, passengers, with_log=True, **config)
    solver.visualize_solution()


def generate(filepath):
    g = GraphGenerator(**config['generate'])
    g.generate_graph_with_all_weights_equal()
    g.save(filepath)


def test(filepath, criteria):
    _parser = Parser(filepath)
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
    num_tests = config['num_tests']

    tester = Tester(graph, passengers, **config)
    tester.test(num_tests, criterias[criteria])


def main():
    g = GraphGenerator(30, 120, 30)
    g.generate_graph_with_all_weights_equal()
    g.save("test")
    _parser = Parser("utils/graphs/example.json")
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

    num_tests = 4
    tester = Tester(graph, passengers, num_lines, num_buses, **kwargs)
    tester.test(num_tests, criterias['1'])


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[2] == '-s':
        solve(sys.argv[1])
    elif len(sys.argv) == 4 and sys.argv[2] == '-t':
        test(sys.argv[1], sys.argv[3])
    elif len(sys.argv) == 3 and sys.argv[2] == '-g':
        generate(sys.argv[1])
    else:
        print("""
            It isn't valid execution.
            Valid form is: ./src/main.py <filepath> <-s | -g | -t criteria>
            -s -> solve graph from filepath
            -g -> generate graph to filepath
            -t -> test graph from filepath for criteria from config file
            criteria -> name of criteria
        """)
