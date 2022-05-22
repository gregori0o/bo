from math import inf
from solver import Solver
import matplotlib.pyplot as plt
import numpy as np

from visualization import GraphVisualizer, LinesVisualizer


class Tester:
    def __init__(self, graph, passengers, num_lines, num_buses, **kwargs):
        self.graph = graph
        self.passengers = passengers
        self.num_lines = num_lines
        self.num_buses = num_buses
        self.cockroach_params = kwargs['cockroach']
        self.bees_params = kwargs['bees']

        self.cockroach_tests_history = {}
        self.bees_test_history = {}

        self.best_global = inf

        self.best_solution = None

    def test(self, num_tests, criteria):
        cockroach_criteria = criteria.get('cockroach', {})
        bees_criteria = criteria.get('bees', {})
        if len(cockroach_criteria) + len(bees_criteria) > 1:
            raise ValueError("There might be max one criterion!")

        if cockroach_criteria:
            cockroach_param_key = next(iter(cockroach_criteria.keys()))
            cockroach_param_values = cockroach_criteria[cockroach_param_key]
            for cockroach_param in cockroach_param_values:
                print("Param: {}={}".format(cockroach_param_key, cockroach_param))
                self.cockroach_params[cockroach_param_key] = cockroach_param
                best_local, worst_local = self._run_tests(num_tests, cockroach_param_key, cockroach_param)
                print("BEST: {} WORST: {}".format(best_local, worst_local))
                if best_local < self.best_global:
                    self.best_global = best_local
            print("OVERALL BEST: {}".format(self.best_global))

        if bees_criteria:
            bees_param_key = next(iter(bees_criteria.keys()))
            bees_param_values = bees_criteria[bees_param_key]
            for bees_param in bees_param_values:
                print("Param: {}={}".format(bees_param_key, bees_param))
                self.bees_params[bees_param_key] = bees_param
                best_local, worst_local = self._run_tests(num_tests, bees_param_key, bees_param)
                print("BEST: {} WORST: {}".format(best_local, worst_local))
                if best_local < self.best_global:
                    self.best_global = best_local
            print("OVERALL BEST: {}".format(self.best_global))

        self.plot_and_save("utils/test_results/cockroach_test.png", "cockroach")
        self.plot_and_save("utils/test_results/bees_test.png", "bees")
        self.visualize_solution()

    def _run_tests(self, num_tests, param, value):
        best_local = inf
        worst_local = -inf
        for i in range(num_tests):
            # print(self.graph.get_edges())
            kwargs = {
                'cockroach': self.cockroach_params,
                'bees': self.bees_params
            }
            solver = Solver(self.graph, self.passengers, self.num_lines, self.num_buses, **kwargs)
            cockroach_results, bees_result = solver.get_steps()
            self.cockroach_tests_history[(i+1, param, value)] = cockroach_results
            self.bees_test_history[(i+1, param, value)] = bees_result
            result = solver.get_result()
            if result > worst_local:
                worst_local = result
            if result < best_local:
                best_local = result
            actual_solution = solver.get_solution()
            if self.best_solution is None or self.best_solution[0] > actual_solution[0]:
                self.best_solution = actual_solution
        return best_local, worst_local

    def plot_and_save(self, path, algorithm):
        plt.clf()
        if algorithm == 'cockroach':
            plt.title("Cockroach algorithm")
            for key, times in self.cockroach_tests_history.items():
                test_num, param_name, param_value = key
                iters = len(times)
                plt.plot(np.arange(1, iters+1), times, label="Test: {} for {}={}".format(test_num, param_name, param_value))
            plt.xlabel('iterations')
            plt.ylabel('results')
            plt.legend()
            plt.savefig(path)

        elif algorithm == 'bees':
            plt.title("Bees algorithm")
            for key, times in self.bees_test_history.items():
                test_num, param_name, param_value = key
                iters = len(times)
                plt.plot(np.arange(1, iters + 1), times,
                         label="Test: {} for {}={}".format(test_num, param_name, param_value))
            plt.xlabel('iterations')
            plt.ylabel('results')
            plt.legend()
            plt.savefig(path)

    def visualize_solution(self, graph_name: str = 'the_best_result'):
        GraphVisualizer(self.graph.size, self.graph.get_edges()).save(graph_name)
        if self.best_solution is None:
            return
        LinesVisualizer(self.graph.size, self.graph.get_edges(), self.best_solution[1], self.graph.get_interchange_points()).save(f"{graph_name}_lines")
        for i, line in enumerate(self.best_solution[1]):
            LinesVisualizer(self.graph.size, self.graph.get_edges(), [line], self.graph.get_interchange_points()).save(f"{graph_name}_line_{i}")

        print("Best lines: {}".format(self.best_solution[1]))
        print(f"The best distribution of buses -> {self.best_solution[2]}")
        print(f"Minimum cost is -> {self.best_solution[0]}")
