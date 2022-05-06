import numpy as np
from base_structure import Graph
from typing import List


class CreateSolution:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.interchange_points = graph.get_interchange_points()
        self.size = graph.size

    def create_dis_matrix(self, vertices: list[int]) -> list[list[tuple[int, list[int]]]]:
        length = len(vertices)
        matrix = [[None] * length for _ in range(length)]
        for i in range(length):
            for j in range(i, length):
                matrix[i][j] = self.graph.shortest_path(vertices[i], vertices[j])
                matrix[j][i] = self.graph.shortest_path(vertices[j], vertices[i])
        return matrix

    def search_next(self, used: list[int], matrix: list[list[tuple[int, list[int]]]], last: int, t: int) -> int:
        if len(matrix) - len(used) == 1:
            return t
        nearest_to_last = []
        farthest_to_t = []
        for i in range(len(matrix)):
            if i in used or i == t:
                continue
            dis = matrix[last][i][0]
            nearest_to_last.append((dis, i))
            dis = matrix[i][t][0]
            farthest_to_t.append((dis, i))
        nearest_to_last.sort(reverse=False)

        farthest_to_t.sort(reverse=True)
        possible_stop = set()
        for nearest, farthest in zip(nearest_to_last, farthest_to_t):
            i, j = nearest[1], farthest[1]
            if i in possible_stop:
                return i
            possible_stop.add(i)
            if j in possible_stop:
                return j
            possible_stop.add(j)

    def make_lines(self, bus_stops: list[int]) -> list[tuple]:
        length = len(bus_stops)
        matrix = self.create_dis_matrix(bus_stops)
        diam = 0
        s, t = 0, 0
        for i in range(length):
            for j in range(i+1, length):
                value, _ = matrix[i][j]
                if value > diam:
                    s, t = i, j
                    diam = value
        used = [s]
        line = [bus_stops[s]]
        while len(used) < length:
            last = used[-1]
            v = self.search_next(used, matrix, last, t)
            for bs in matrix[last][v][1][1:]:
                if bs in line:
                    continue
                line.append(bs)
                if bs in bus_stops:
                    x = bus_stops.index(bs)
                    used.append(x)

            # line.append(bus_stops[v])
            # used.append(v)

        res_line = []
        for i in range(len(line) - 1):
            x, y = line[i], line[i+1]
            res_line.append((x, self.graph.shortest_path(x, y)[0]))
        res_line.append((line[-1], 0))

        return res_line

    def create_init_solution(self, number_lines: int, number_bus: int) -> tuple[list[list[tuple]], list[int]]:
        bus_stops = np.random.permutation(self.size)
        lists_of_stops = [list(arr) for arr in np.array_split(bus_stops, number_lines-1)]
        for list_stops in lists_of_stops:
            point = np.random.choice(self.interchange_points)
            if point not in list_stops:
                list_stops.append(point)
        lists_of_stops.append(self.interchange_points)
        lines = [self.make_lines(list_stops) for list_stops in lists_of_stops]
        divider = DivideBuses(number_lines, number_bus)
        buses = divider.get_one_solution()
        return lines, list(buses)


class DivideBuses:
    def __init__(self, num_lines: int, num_buses: int):
        self.num_buses = num_buses
        self.num_lines = num_lines

    def get_one_solution(self, scale: float = 3.0) -> np.ndarray:
        result = np.ones(self.num_lines)
        mean = (self.num_buses - self.num_lines) // self.num_lines
        samples = np.random.normal(loc=mean, scale=scale, size=self.num_lines).astype(int)
        samples[samples < 0] = 0
        diff = self.num_buses - self.num_lines - sum(samples)
        change = 1 if diff > 0 else -1
        for i in range(abs(diff)):
            while True:
                idx = np.random.randint(self.num_lines)
                if samples[idx] + change >= 0:
                    samples[idx] += change
                    break
        return result + samples

    def get_solutions(self, k: int) -> List[np.ndarray]:
        result = []
        for _ in range(k):
            scale = (np.random.random_sample() + 0.5) * (self.num_buses / self.num_lines)
            result.append(self.get_one_solution(scale))
        return result
