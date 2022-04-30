import random

from base_structure import Graph
from graph_generator import GraphGenerator
from initial_solution import CreateSolution
from json_parser import Parser

from pprint import pprint


class Cockroach:
    def __init__(self, lines):
        self.visible_cockroaches: list[Cockroach] = []

        self.min_common = 8

        self.lines = lines
        self.edges = self.__update_edges()
        self.metric_value = self.__evaluate_metric_value()

    def __update_edges(self):
        self.edges: set[tuple[int, int]] = set()

        for line in self.lines:
            for v, u in zip(line[:-1], line[1:]):
                e = v[0], u[0]
                self.edges.add(e)
        return self.edges

    def update_visible_cockroaches(self, all_cockroaches):
        """

        :type all_cockroaches: list[Cockroach]
        """

        def check_if_visible(cockroach: Cockroach):
            return len(self.edges & cockroach.edges) >= self.min_common

        self.visible_cockroaches = [c for c in all_cockroaches if c is not self and check_if_visible(c)]

    def get_best_visible_cockroach(self):
        def get_metric_value(cockroach):
            """

            :type cockroach: Cockroach
            """
            return cockroach.metric_value

        return max(self.visible_cockroaches, key=get_metric_value)

    def __evaluate_metric_value(self):
        # todo evaluating value
        self.metric_value = random.randint(0, 10)
        return self.metric_value

    def get_random_common_edge(self, best_visible):
        return random.choice(tuple(self.edges & best_visible.edges))


def cockroach_solution(graph):
    pprint([(v.index, [(u.index, w) for u, w in v.neighbours]) for v in graph.vertices])
    print()
    init = CreateSolution(graph)
    num_cockroaches = 5

    cockroaches = []

    for i in range(num_cockroaches):
        lines, buses = init.create_init_solution(3, 20)

        for l in lines:
            print(l)
        print("\n")

        cockroaches.append(Cockroach(lines))

    for cockroach in cockroaches:
        cockroach.update_visible_cockroaches(cockroaches)

        if len(cockroach.visible_cockroaches) == 0:
            print("EMPTY")
            continue

        best_visible = cockroach.get_best_visible_cockroach()

        random_edge = cockroach.get_random_common_edge(best_visible)

        print(random_edge)

        # todo



def main():
    # g = GraphGenerator(20, 22)
    # g.generate_graph_with_all_weights_equal("../utils/graphs/example.json")
    _parser = Parser("../utils/graphs/g1.json")
    interchange_points = _parser.get_interchange_points()
    size = _parser.get_size()
    edges = _parser.get_edges()
    graph = Graph(size)
    for i, j, w in edges:
        graph.add_edge(i, j, w)
    graph.set_interchange_points(interchange_points)

    cockroach_solution(graph)


if __name__ == '__main__':
    main()
