from math import inf
from solver import Solver


class Tester:
    def __init__(self, graph, passengers, num_lines, num_buses, **kwargs):
        self.graph = graph
        self.passengers = passengers
        self.num_lines = num_lines
        self.num_buses = num_buses
        self.cockroach_params = kwargs['cockroach']
        self.bees_params = kwargs['bees']

        self.best_global = inf

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
                best_local, worst_local = self._run_tests(num_tests)
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
                best_local, worst_local = self._run_tests(num_tests)
                print("BEST: {} WORST: {}".format(best_local, worst_local))
                if best_local < self.best_global:
                    self.best_global = best_local
            print("OVERALL BEST: {}".format(self.best_global))

    def _run_tests(self, num_tests):
        best_local = inf
        worst_local = -inf
        for i in range(num_tests):
            # print(self.graph.get_edges())
            solver = Solver(self.graph, self.passengers, self.num_lines, self.num_buses, kwargs={
                'cockroach': self.cockroach_params,
                'bees': self.bees_params
            })
            result = solver.get_result()
            if result > worst_local:
                worst_local = result
            if result < best_local:
                best_local = result
        return best_local, worst_local
