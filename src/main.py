from base_structure import Graph
from json_parser import Parser
from src.solver import Solver
from graph_generator import GraphGenerator
from passengers_generator import Passengers


def main():
    g = GraphGenerator(20, 22, 100)
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
    kwargs = {
        'cockroach': {
            'num_cockroaches': 10,
            'min_common': 8,
            'step_size': 2,
            'dispersing_update_ratio': .5,
            'n_iterations': 5,
            'num_to_test': 5
        },

        'bees': {
            'num_bees': 10,
            'num_transition': 2,
            'update_ratio': .3,
            'n_iterations': 5
        }
    }

    solver = Solver(graph, passengers, num_lines, num_buses, **kwargs)
    solver.visualize_solution("solution")


if __name__ == '__main__':
    main()
