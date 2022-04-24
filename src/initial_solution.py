import numpy as np
from base_structure import Graph


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

    def make_lines(self, bus_stops: list[int]) -> list[int]:
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
        print(len(bus_stops))
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

        return line

    def create_init_solution(self, number_lines: int, number_bus: int) -> tuple[list[list[int]], list[int]]:
        bus_stops = np.random.permutation(self.size)
        lists_of_stops = [list(arr) for arr in np.array_split(bus_stops, number_lines)]
        for list_stops in lists_of_stops:
            point = np.random.choice(self.interchange_points)
            if point not in list_stops:
                list_stops.append(point)
        lines = [self.make_lines(list_stops) for list_stops in lists_of_stops]
        k = number_bus % number_lines
        num = number_bus // number_lines
        buses = [num + 1] * k + [num] * (number_lines - k)
        return lines, buses
