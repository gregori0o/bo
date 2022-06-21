import numpy as np
from initial_solution import DivideBuses
from line_result import LineResult
from typing import List, Optional, Dict, Tuple


class BeesAlgorithm:
    def __init__(self, num_lines: int, num_buses: int, data: Dict, num_bees: int = 10, num_transition: int = 2, update_ratio: float = .3, n_iterations: int = 10):
        self.data = data
        self.num_lines = num_lines
        self.num_buses = num_buses
        self.num_bees = num_bees
        self.population = DivideBuses(num_lines, num_buses).create_solutions(num_bees)
        self.k = num_transition
        self.p = min(max(int(update_ratio * num_bees), 1), num_bees)
        self.iterations = n_iterations
        self.partial_results = []

    def get_cost(self, solution: np.ndarray) -> float:
        solver = LineResult(buses=list(solution), **self.data)
        return float(solver.average_time)

    def generate_similar(self, solution: np.ndarray, m: int) -> List[np.ndarray]:
        result = []
        for _ in range(m):
            sol = solution.copy()
            for _ in range(self.k):
                while True:
                    idx = np.random.randint(self.num_lines)
                    if sol[idx] > 1:
                        break
                sol[idx] -= 1
                idx = np.random.randint(self.num_lines)
                sol[idx] += 1
            result.append(sol)
        return result

    def cost_for_population(self, population: Optional[List[np.ndarray]] = None) -> List[Tuple[float, np.ndarray]]:
        if population is None:
            population = self.population
        result = []
        for solution in population:
            result.append((self.get_cost(solution), solution))
        return sorted(result, key=lambda x: x[0])

    def step(self, cost_of_population: List[Tuple[float, np.ndarray]]):
        free_bees = self.num_bees - self.p
        best_cost = cost_of_population[:self.p]
        sum_weights = sum([1/x for x, _ in best_cost])
        self.population = []
        for x, solution in best_cost:
            m = round((free_bees/x) / sum_weights)
            m = max(m, 1)
            similar = self.generate_similar(solution, m)
            costs = self.cost_for_population(similar)
            if costs[0][0] < x:
                self.population.append(costs[0][1])
            else:
                self.population.append(solution)
        self.population += DivideBuses(self.num_lines, self.num_buses).create_solutions(free_bees)

    def solve(self, with_log=False) -> Tuple[float, np.ndarray]:
        the_best = np.inf
        costs = self.cost_for_population()
        for _ in range(self.iterations):
            the_best = min(the_best, costs[0][0])
            if with_log:
                print(f"Actual minimum -> {the_best}")
            self.step(costs)
            costs = self.cost_for_population()
            self.partial_results.append(the_best)
        return costs[0]

    def get_results_step_by_step(self):
        return self.partial_results
