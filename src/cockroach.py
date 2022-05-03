import random

from base_structure import Graph
from initial_solution import CreateSolution
from json_parser import Parser


class Cockroach:
    __id = 0
    min_common = 9
    step_size = 2

    def __init__(self, lines: list):
        self.visible_cockroaches: list[Cockroach] = []

        self.lines = lines
        self.edges = self.__update_edges()  # edge: no_line
        self.metric_value = self.__evaluate_metric_value()

        self.id = Cockroach.__id
        Cockroach.__id += 1

    def __update_edges(self):
        self.edges: dict[tuple[int, int], (int, int)] = {}

        for i, line in enumerate(self.lines):
            for edge_no, tmp in enumerate(zip(line[:-1], line[1:])):
                v, u = tmp
                e = v[0], u[0]
                self.edges[e] = i, edge_no
        return self.edges

    def update_visible_cockroaches(self, all_cockroaches):
        """

        :type all_cockroaches: list[Cockroach]
        """

        def check_if_visible(cockroach: Cockroach):
            return len(self.edges & cockroach.edges.keys()) >= self.min_common

        self.visible_cockroaches = [c for c in all_cockroaches if c.id != self.id and check_if_visible(c)]

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
        return random.choice(tuple(self.edges.keys() & best_visible.edges.keys()))


def is_line_better(old, new):
    # todo
    desired_len = 5

    return abs(len(new) - desired_len) <= abs(len(old) - desired_len)


class CockroachSolution:
    def __init__(self, graph, num_cockroaches=10, num_lines=5):
        self.solution_creator = CreateSolution(graph)

        self.cockroaches = []

        for i in range(num_cockroaches):
            lines, buses = self.solution_creator.create_init_solution(num_lines, 20)
            self.cockroaches.append(Cockroach(lines))

    def chase_swarming(self):
        for cockroach in self.cockroaches:
            cockroach.update_visible_cockroaches(self.cockroaches)

            if len(cockroach.visible_cockroaches) == 0:
                print("EMPTY")
                continue

            best_visible = cockroach.get_best_visible_cockroach()

            random_edge = cockroach.get_random_common_edge(best_visible)
            line_no, edge_no = cockroach.edges[random_edge]
            best_line_no, best_edge_no = best_visible.edges[random_edge]
            # print(f"{cockroach.id}: edge {random_edge} line_no {line_no} \t best {best_visible.id} line_no {best_line_no}")

            line = cockroach.lines[line_no]
            best_line = best_visible.lines[best_line_no]

            new_line_start_stops = [l[0] for l in line[:edge_no + 1]]
            new_line_from_best_stops = [l[0] for l in
                                        random.sample(best_line[best_edge_no + 1:],
                                                      Cockroach.step_size if Cockroach.step_size <= len(
                                                          best_line[best_edge_no + 1:])
                                                      else len(best_line[
                                                               best_edge_no + 1:]))]  # todo save order... or no?
            # print(f"starting {new_line_start_stops} added {new_line_from_best_stops}")

            final_stops = new_line_start_stops + new_line_from_best_stops
            final_stops += [line[-1][0]] if line[-1][0] not in new_line_from_best_stops else []
            # print(f"final stops { final_stops }")

            new_line = self.solution_creator.make_lines(final_stops)

            # print(f"{line}\n{best_line}")
            # print(f"\t{new_line}\n")

            if is_line_better(line, new_line):
                cockroach.lines[line_no] = new_line


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

    solution = CockroachSolution(graph)

    solution.chase_swarming()


if __name__ == '__main__':
    main()
