import numpy as np
from initial_solution import DivideBuses
from line_result import LineResult
from typing import List, Optional, Dict, Tuple


class BeesAlgorithm:
    def __init__(self, num_lines: int, num_buses: int, data: Dict, num_bees: int = 10, num_transition: int = 2, percent_bees: float = 1/3):
        self.data = data
        self.num_lines = num_lines
        self.num_buses = num_buses
        self.num_bees = num_bees
        self.population = DivideBuses(num_lines, num_buses).create_solutions(num_bees)
        self.k = num_transition
        self.p = min(max(int(percent_bees * num_bees), 1), num_bees)

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

    def solve(self) -> Tuple[float, np.ndarray]:
        the_best = np.inf
        costs = self.cost_for_population()
        while (the_best - costs[0][0]) > 0:
            the_best = min(the_best, costs[0][0])
            print(f"Actual minimum -> {the_best}")
            self.step(costs)
            costs = self.cost_for_population()
        print(f"Minimum is -> {the_best}")
        return costs[0]


# sample execution
def main():
    from json_parser import Parser
    from base_structure import Graph
    from initial_solution import CreateSolution
    from passengers_generator import Passengers

    _parser = Parser("../utils/graphs/g1.json")
    interchange_points = _parser.get_interchange_points()
    size = _parser.get_size()
    edges = _parser.get_edges()
    graph = Graph(size)
    for i, j, w in edges:
        graph.add_edge(i, j, w)
    graph.set_interchange_points(interchange_points)
    init = CreateSolution(graph)
    num_lines = 3
    num_buses = 20
    lines, buses = init.create_init_solution(num_lines, num_buses)
    p = Passengers(size, 100)
    travels = p.travels

    data = {
        'interchange_points': interchange_points,
        'lines': lines,
        'travels': travels
    }
    solver = BeesAlgorithm(num_lines, num_buses, data, 10, 1, 0.3)
    result = solver.solve()

    print(f"size={size}")
    print(f"edges={edges}")
    print(f"{interchange_points=}")
    print(f"lines={lines}")
    print(f"buses={buses}")
    print(f"{travels=}")
    print(f"the best result={result[0]}")
    print(f"the best distribution={result[1]}")

if __name__ == "__main__":
    main()
