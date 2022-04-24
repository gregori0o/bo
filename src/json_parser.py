import json


class Parser:
    def __init__(self, path):
        with open(path, "r") as file:
            self.data = json.load(file)
            self.vertices = self.data["vertices"]

    def get_edges(self):
        edges = []
        for v in self.vertices:
            v = int(v["index"])
            for n in self.vertices[v]["neighbours"]:
                neighbour = int(n["index"])
                val = int(n["weight"])
                if neighbour > v:
                    edges.append((v, neighbour, val))
        return edges

    def get_interchange_points(self):
        return [data["index"] for data in self.vertices if data["interchange_point"]]

    def get_size(self):
        return len(self.vertices)


