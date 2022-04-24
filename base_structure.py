from queue import PriorityQueue
import numpy as np


class Vertex:
    def __init__(self, index: int, name: str):
        self.index = index
        self.name = name
        self.neighbours = []
        self.interchange_point = False

    def add_edge(self, vertex: Vertex, weight: int):
        self.neighbours.append((vertex, weight))

    def get_neighbourhood(self) -> list[tuple[Vertex, int]]:
        return self.neighbours

    def set_interchange_point(self, value: bool = True):
        self.interchange_point = value


class Graph:
    def __init__(self, size: int, names: list[str] = None):
        self.names = ['#{}'.format(i) for i in range(size)] if names is None else names
        self.size = size
        self.vertices = [Vertex(i, name) for i, name in zip(range(size), self.names)]

    def add_edge(self, i: int, j: int, weight: int):
        self.vertices[i].add_edge(self.vertices[j], weight)
        self.vertices[j].add_edge(self.vertices[i], weight)

    def get_interchange_points(self) -> list[int]:
        return [vertex.index for vertex in self.vertices if vertex.interchange_point]

    def shortest_path(self, s: int, t: int):
        queue = PriorityQueue()
        parent = [None] * self.size
        dis = [np.inf] * self.size
        visited = [False] * self.size
        parent[s] = s
        dis[s] = 0
        queue.put((0, s))
        while queue.not_empty():
            weight, v = queue.get()
            if v == t:
                break
            if visited[v]:
                continue
            visited[v] = True
            for u, w in self.vertices[v].get_neighbourhood():
                if dis[u.index] > dis[v] + w:
                    dis[u.index] = dis[v] + w
                    parent[u.index] = v
        path = []
        v = t
        while v != s:
            path.append(v)
            v = parent[v]
        path.append(s)
        path = reversed(path)
        return path, dis[t]
