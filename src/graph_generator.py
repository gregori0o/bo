import json
from random import sample


class GraphGenerator:
    def __init__(self, vertices, min_edges):
        self.vertices = vertices
        self.edges = min_edges
        self.graph = {"vertices": []}
        self.interchange_points = sample(range(vertices), 4)
        self.edges_list = sample([(x, y) for x in range(self.vertices) for y in range(self.vertices) if x < y], self.edges)
        self.make_reachable()

    def generate_graph_with_all_weights_equal(self):
        for v in range(self.vertices):
            self.graph["vertices"].append({"index": v, "interchange_point": v in self.interchange_points, "neighbours": []})
        for e in self.edges_list:
            u, v = e
            self.graph["vertices"][u]["neighbours"].append({"index": v, "weight": 1})
            self.graph["vertices"][v]["neighbours"].append({"index": u, "weight": 1})

    def find_components(self, components, rep):
        for e in self.edges_list:
            if len(components) == 1:
                break
            u, v = e
            if rep[u] == rep[v]: # connected
                continue
            components[rep[u]].update(components[rep[v]])
            merged = components.pop(rep[v], None)
            if merged:
                for item in merged:
                    rep[item] = rep[u]

    def make_reachable(self):
        components = {}
        rep = {}
        for v in range(self.vertices):
            components[v] = set()
            components[v].add(v)
            rep[v] = v

        self.find_components(components, rep)

        counter = 0 # check, to delete later
        for comp in components.values():
            counter += len(comp)
        if counter != self.vertices:
            print("ERROR WITH SPLITTING COMPONENTS!")

        for component in components.copy().values():
            u = sample(list(components[rep[0]]), 1)[0]
            v = sample(list(component), 1)[0]
            if rep[u] != rep[v]:
                components[rep[u]].update(components[rep[v]])
                merged = components.pop(rep[v], None)
                if merged:
                    for item in merged:
                        rep[item] = rep[u]
                self.edges_list.append((u, v))

    def save(self, filename: str):
        with open("../utils/graphs/" + filename + ".json", "w") as file:
            json.dump(self.graph, file, indent=4)

# sample execution
# g = GraphGenerator(10, 20)
# g.generate_graph_with_all_weights_equal()
# g.save("filename")
# print(g.graph)
# print(f"{g.edges_list=}")
# print(f"{g.vertices=}")
# print(f"{g.edges=}")
# print(f"{g.interchange_points=}")
