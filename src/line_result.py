from json_parser import Parser
from base_structure import Graph
from initial_solution import CreateSolution

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
print(size, edges, interchange_points, lines, buses, sep="\n")

from itertools import combinations
from passengers_generator import Passengers

# TODO not yet done
class LineResult:
    stopping_time = 1
    turning_back_time = 3

    def __int__(self, size, edges: list[tuple[int, int, int]], interchange_points: list, lines: list[list[tuple[int, int]]], buses: list[int], travels: list[[int, int, int]]):
        self.size = size
        self.edges = edges
        self.interchange_points = interchange_points
        self.lines = lines
        self.buses = buses
        self.travels = travels

        self.in_dir_time, self.in_opp_dir_time, self.time_between_buses = self.schedule()

    def schedule(self):
        in_dir_time = [[None for _ in range(len(line))] for line in lines]
        in_opp_dir_time = [[None for _ in range(len(line))] for line in lines]
        time_between_buses = [None for _ in range(lines)]
        for line_idx in range(lines):
            time = 0
            for station, station_idx in enumerate(line):
                in_dir_time[line_idx][station_idx] = time
                time += station[1] + stopping_time
            time += turning_back_time
            for station, station_idx in enumerate(list(reversed(line))):
                in_dir_time[line_idx][station_idx] = time
                time += station[1] + stopping_time
            time += turning_back_time
            time_between_buses[line_idx] = time // self.buses[line_idx]
        return in_dir_time, in_opp_dir_time, time_between_buses


    def calculate_travel_time(self, from_, to_, start_time):
        pass

p = Passengers(size, 100)
travels = p.travels
r = LineResult(size, edges, interchange_points, lines, buses, travels)