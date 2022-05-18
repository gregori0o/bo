from base_structure import Graph
from typing import List
from bees_algorithm import BeesAlgorithm
from visualization import GraphVisualizer, LinesVisualizer
from cockroach import CockroachSolution


class Solver:
    def __init__(self, graph: Graph, passengers: List[List[int]], num_lines: int, num_buses: int, **kwargs):
        self.graph = graph
        self.passengers = passengers
        self.num_lines = num_lines
        self.num_buses = num_buses

        self.cockroach_steps = []
        self.bees_steps = []
        # print("Start cockroach algorithm")
        print(kwargs.get('cockroach', {}))
        self.best_lines = self.apply_cockroach_algorithm(**kwargs.get('cockroach', {}))
        # print("Start bees algorithm")
        self.cost, self.best_buses = self.apply_bees_algorithm(**kwargs.get('bees', {}))
        # print("End solving")

    def apply_cockroach_algorithm(self, **kwargs) -> List[List[tuple]]:
        algorithm = CockroachSolution(self.graph, self.num_lines, self.num_buses, self.passengers, **kwargs)
        self.cockroach_steps = algorithm.get_step_by_step_results()
        return algorithm.solve()

    def apply_bees_algorithm(self, **kwargs):
        data = {
            'interchange_points': self.graph.get_interchange_points(),
            'lines': self.best_lines,
            'travels': self.passengers
        }
        algorithm = BeesAlgorithm(self.num_lines, self.num_buses, data, **kwargs)
        self.bees_steps = algorithm.get_results_step_by_step()
        return algorithm.solve()

    def visualize_solution(self, graph_name: str = 'solution_graph'):
        GraphVisualizer(self.graph.size, self.graph.get_edges()).save(graph_name)
        LinesVisualizer(self.graph.size, self.graph.get_edges(), self.best_lines, self.graph.get_interchange_points()).save(f"{graph_name}_lines")
        for i, line in enumerate(self.best_lines):
            LinesVisualizer(self.graph.size, self.graph.get_edges(), [line], self.graph.get_interchange_points()).save(f"{graph_name}_line_{i}")

        #print("Best lines: {}".format(self.best_lines))
        #print(f"The best distribution of buses -> {self.best_buses}")
        #print(f"Minimum cost is -> {self.cost}")

    def get_result(self):
        return self.cost

    def get_steps(self):
        return self.cockroach_steps, self.bees_steps
