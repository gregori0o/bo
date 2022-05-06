from base_structure import Graph
from initial_solution import CreateSolution
from json_parser import Parser
from src.passengers_generator import Passengers
from visualization import GraphVisualizer, LinesVisualizer
from graph_generator import GraphGenerator
from bees_algorithm import BeesAlgorithm


def main():
    g = GraphGenerator(20, 22)
    g.generate_graph_with_all_weights_equal()
    g.save("test")
    _parser = Parser("utils/graphs/test.json")
    interchange_points = _parser.get_interchange_points()
    size = _parser.get_size()
    edges = _parser.get_edges()
    graph = Graph(size)
    for i, j, w in edges:
        graph.add_edge(i, j, w)
    graph.set_interchange_points(interchange_points)
    init = CreateSolution(graph)
    num_lines = 3
    num_buses = 20
    lines, buses = init.create_init_solution(num_lines, num_buses)

    # graph_vis = GraphVisualizer(size, edges)
    # graph_vis.save('graph')
    #
    # for i, line in enumerate(lines):
    #    lines_vis = LinesVisualizer(size, edges, [line], interchange_points)
    #    lines_vis.save('line{}'.format(i))

    p = Passengers(size, 100)
    travels = p.travels
    data = {
        'interchange_points': interchange_points,
        'lines': lines,
        'travels': travels
    }
    solver = BeesAlgorithm(num_lines, num_buses, 10, 1, 0.3, data)
    result = solver.solve()
    print(result)


if __name__ == '__main__':
    main()
