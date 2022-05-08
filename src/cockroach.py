import copy
import random

from base_structure import Graph
from initial_solution import CreateSolution
from json_parser import Parser
from pprint import pprint

from src.line_result import LineResult
from src.passengers_generator import Passengers

MIN_COMMON = 8
STEP_SIZE = 2
MAX_UPDATE_RATIO = .5 # should be <= 0.5 !!!


class Cockroach:
    __id = 0

    def __init__(self, lines: list, buses, passengers, interchange_points):
        self.visible_cockroaches: list[Cockroach] = []

        self.lines = lines
        self.edges = self.__update_edges()  # edge: no_line

        self.buses = buses
        self.passengers = passengers
        self.travels = passengers.travels
        self.interchange_points = interchange_points

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
            return len(self.edges & cockroach.edges.keys()) >= MIN_COMMON

        self.visible_cockroaches = [c for c in all_cockroaches if c.id != self.id and check_if_visible(c)]

    def get_best_visible_cockroach(self):
        return max(self.visible_cockroaches)

    def __evaluate_metric_value(self):
        summary = LineResult(self.interchange_points, self.lines, self.buses, self.travels)
        self.metric_value = summary.average_time

        return self.metric_value

    def get_random_common_edge(self, best_visible):
        return random.choice(tuple(self.edges.keys() & best_visible.edges.keys()))

    def __eq__(self, other):
        return self.lines == other.lines

    def __gt__(self, other):
        return self.metric_value < other.metric_value


def cockroach_from_new_line(cockroach, line_no, new_line):
    new_lines = copy.deepcopy(cockroach.lines)
    new_lines[line_no] = new_line
    new_cockroach = Cockroach(new_lines, cockroach.buses, cockroach.passengers, cockroach.interchange_points)
    return new_cockroach


def get_final_stops(line, new_line_from_best_stops, new_line_start_stops):
    # final_stops = new_line_start_stops + new_line_from_best_stops
    final_stops = new_line_start_stops + [stop for stop in new_line_from_best_stops if
                                          stop not in new_line_start_stops]  # to drugie dlatego zeby sie nie dublowaly - wtedy sie zacina generowanie
    final_stops += [line[-1][0]] if line[-1][0] not in final_stops else []
    return final_stops


def get_edge_and_line_info(cockroach, random_edge):
    line_no, edge_no = cockroach.edges[random_edge]
    line = cockroach.lines[line_no]
    return edge_no, line_no, line


def get_stops_from_current_cockroach(edge_no, line):
    new_line_start_stops = [l[0] for l in line[:edge_no + 1]]
    return new_line_start_stops


def get_stops_from_best_cockroach(best_edge_no, best_line):
    new_line_from_best_stops = [l[0] for l in
                                random.sample(best_line[best_edge_no + 1:],
                                              STEP_SIZE if STEP_SIZE <= len(
                                                  best_line[best_edge_no + 1:])
                                              else len(best_line[
                                                       best_edge_no + 1:]))]  # todo save order... or no?
    return new_line_from_best_stops


class CockroachSolution:
    def __init__(self, graph, num_cockroaches=10, num_lines=5, num_busses=20, num_passengers=100, min_common=8,
                 step_size=2, dispersing_update_ratio=.5):
        global MIN_COMMON, STEP_SIZE, MAX_UPDATE_RATIO
        MIN_COMMON = min_common
        STEP_SIZE = step_size
        MAX_UPDATE_RATIO = dispersing_update_ratio

        self.stops = set(list(range(len(graph.vertices))))

        self.solution_creator = CreateSolution(graph)

        self.cockroaches = []

        passengers = Passengers(graph.size, num_passengers)

        for i in range(num_cockroaches):
            lines, buses = self.solution_creator.create_init_solution(num_lines, num_busses)

            self.cockroaches.append(Cockroach(lines, buses, passengers, graph.get_interchange_points()))

    def solve(self, n_iterations=10):
        for _ in range(n_iterations):
            print("BEST: {}".format(self.get_best_global_cockroach().metric_value))
            self.chase_swarming()
            self.dispersing()

        return self.get_best_global_cockroach().lines

    def chase_swarming(self):
        for i in range(len(self.cockroaches)):
            cockroach = self.cockroaches[i]

            cockroach.update_visible_cockroaches(self.cockroaches)

            if len(cockroach.visible_cockroaches) == 0:
                # print("EMPTY")
                continue

            best_visible = cockroach.get_best_visible_cockroach()

            if best_visible.metric_value <= cockroach.metric_value:
                best_visible = self.get_best_global_cockroach()

            if best_visible == cockroach:
                # print("SAME")
                continue

            random_edge = cockroach.get_random_common_edge(best_visible)
            edge_no, line_no, line = get_edge_and_line_info(cockroach, random_edge)
            best_edge_no, best_line_no, best_line = get_edge_and_line_info(best_visible, random_edge)

            # print(f"{cockroach.id}: edge {random_edge} line_no {line_no} \t best {best_visible.id} line_no {best_line_no}")

            new_line_start_stops = get_stops_from_current_cockroach(edge_no, line)
            new_line_from_best_stops = get_stops_from_best_cockroach(best_edge_no, best_line)

            # print(f"starting {new_line_start_stops} added {new_line_from_best_stops}")

            final_stops = get_final_stops(line, new_line_from_best_stops, new_line_start_stops)
            if random.random() >= .5:
                final_stops.reverse()
            # print(f"final stops {final_stops}")

            new_line = self.solution_creator.make_lines(final_stops)

            # print(f"{line}\n{best_line}")
            # print(f"\t{new_line}\n")

            new_cockroach = cockroach_from_new_line(cockroach, line_no, new_line)

            if cockroach < new_cockroach:
                self.cockroaches[i] = new_cockroach

    def dispersing(self):
        for i in range(len(self.cockroaches)):
            cockroach = self.cockroaches[i]

            random_line = random.randint(0, len(cockroach.lines)-1) # choose line to change
            line = cockroach.lines[random_line]
            edges_num = len(line)
            max_update_segments_num = int(MAX_UPDATE_RATIO * edges_num)

            stops = [segment[0] for segment in line]
            if random.random() > 0.5:   # remove some stops from one of ends
                stops.reverse()

            if len(stops) > 2: # omit remove step if we destroy line in that way
                stops_to_remove = random.randint(0, max_update_segments_num)
                stops = stops[:edges_num - stops_to_remove]

            stops_not_used = list(self.stops - set(stops))  # add some stops
            sample_size = random.randint(0, min(max_update_segments_num, len(stops_not_used)))
            stops_to_add = random.sample(stops_not_used, sample_size)
            stops += stops_to_add

            new_line = self.solution_creator.make_lines(stops) # make new line
            new_cockroach = cockroach_from_new_line(cockroach, random_line, new_line)

            if cockroach < new_cockroach:   # override cockroach if its better
                self.cockroaches[i] = new_cockroach

    def get_best_global_cockroach(self):
        return max(self.cockroaches)


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

    solution.solve()


if __name__ == '__main__':
    main()
