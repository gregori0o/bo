from itertools import combinations
import numpy as np
from math import ceil

class LineResult:
    stopping_time = 1
    turning_back_time = 3

    def __init__(self, interchange_points: list,
                       lines: list[list[tuple[int, int]]],
                       buses: list[int],
                       travels: list[[int, int, int]]):
        self.interchange_points = interchange_points
        self.lines = lines
        self.line_sets = self.bus_stops_sets_for_lines()
        self.buses = buses

        (self.in_dir_time,
         self.in_opp_dir_time,
         self.bus_travel_time,
         self.time_between_buses) = self.schedule()

        self.total_time = 0
        for travel in travels:
            travel_time = self.calculate_travel_time(travel[0], travel[1], travel[2])
            self.total_time += travel_time
        self.average_time = self.total_time / len(travels)

    def bus_stops_sets_for_lines(self):
        line_sets = []
        for line in range(len(self.lines)):
            line_set = set()
            for bus_stop in self.lines[line]:
                line_set |= {bus_stop[0]}
            line_sets.append(line_set)
        return line_sets

    def schedule(self):
        in_dir_time = [[None for _ in range(len(line))] for line in self.lines]
        in_opp_dir_time = [[None for _ in range(len(line))] for line in self.lines]
        bus_travel_time = [None for _ in range(len(self.lines))]
        time_between_buses = [None for _ in range(len(self.lines))]
        for line_idx, line in enumerate(self.lines):
            time = 0
            for station_idx, station in enumerate(line):
                in_dir_time[line_idx][station_idx] = time
                time += station[1] + self.stopping_time
            time += self.turning_back_time
            for station_idx, station in reversed(list(enumerate(line))):
                in_opp_dir_time[line_idx][station_idx] = time
                time += station[1] + self.stopping_time
            time += self.turning_back_time
            bus_travel_time[line_idx] = time
            time_between_buses[line_idx] = ceil(time / self.buses[line_idx])
        return in_dir_time, in_opp_dir_time, bus_travel_time, time_between_buses


    def calculate_travel_time(self, start_point, end_point, start_time):
        def check_connection(a, b, line):
            if a in line and b in line:
                return True
            return False

        def direct_time(from_, to_, start_time):
            if from_ == to_:
                return start_time
            best_end_time = np.inf
            for line_idx, line in enumerate(self.line_sets):
                if check_connection(from_, to_, line):
                    bus_stops = np.array(self.lines[line_idx])[:, 0]
                    start_idx = np.where(bus_stops == from_)[0][0]
                    end_idx = np.where(bus_stops == to_)[0][0]
                    if start_idx < end_idx:
                        arrival_time = self.in_dir_time[line_idx][start_idx]
                    else:
                        arrival_time = self.in_opp_dir_time[line_idx][start_idx]

                    c = ceil((start_time - arrival_time) / self.time_between_buses[line_idx])
                    arrival_time += c * self.time_between_buses[line_idx]

                    end_time = arrival_time + abs(self.in_dir_time[line_idx][start_idx] - self.in_dir_time[line_idx][end_idx])
                    if end_time < best_end_time:
                        best_end_time = end_time
            return best_end_time

        def time_with_transfers(bus_stops):
            end_time = start_time
            for i in range(len(bus_stops)-1):
                end_time = direct_time(bus_stops[i], bus_stops[i+1], end_time)
                if end_time == np.inf:
                    return np.inf
            return end_time - start_time

        best_time = np.inf
        for change_count in range(5):
            for transfers in combinations(self.interchange_points, change_count):
                bus_stops = [start_point] + list(transfers) + [end_point]
                time = time_with_transfers(bus_stops)
                if time < best_time:
                    best_time = time
                # print(f"{best_time=}, {start_point=}, {end_point=}")
        return best_time

def main():
    from json_parser import Parser
    from base_structure import Graph
    from initial_solution import CreateSolution
    from passengers_generator import Passengers

    _parser = Parser("utils/graphs/g1.json")
    interchange_points = _parser.get_interchange_points()
    size = _parser.get_size()
    edges = _parser.get_edges()
    graph = Graph(size)
    for i, j, w in edges:
        graph.add_edge(i, j, w)
    graph.set_interchange_points(interchange_points)
    init = CreateSolution(graph)
    lines, buses = init.create_init_solution(3, 20)
    p = Passengers(size, 100)
    travels = p.travels
    line = LineResult(interchange_points, lines, buses, travels)

    # print(f"size={size}")
    # print(f"edges={edges}")
    # print(f"{interchange_points=}")
    # print(f"lines={lines}")
    # print(f"buses={buses}")
    # print(f"{travels=}")
    # print(f"{line.in_dir_time=}")
    # print(f"{line.in_opp_dir_time=}")
    # print(f"{line.bus_travel_time=}")
    # print(f"{line.time_between_buses=}")

    print(f"{line.total_time=}")
    print(f"{line.average_time=}")

if __name__ == "__main__":
    main()
