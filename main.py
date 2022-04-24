from base_structure import Graph
from initial_solution import CreateSolution


size = 10
edges = [
    (0, 1, 3),
    (1, 2, 3),
    (2, 5, 5),
    (1, 3, 2),
    (3, 4, 1),
    (4, 7, 1),
    (5, 7, 3),
    (5, 6, 6),
    (7, 6, 3),
    (6, 9, 2),
    (8, 9, 4),
    (7, 8, 5)
]
interchange_points = [1, 5, 6, 7]


def main():
    graph = Graph(size)
    for i, j, w in edges:
        graph.add_edge(i, j, w)
    graph.set_interchange_points(interchange_points)
    init = CreateSolution(graph)
    lines, buses = init.create_init_solution(3, 20)
    print(lines, buses)


if __name__ == '__main__':
    main()
