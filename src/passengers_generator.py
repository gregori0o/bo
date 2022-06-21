from random import sample, choices
import numpy as np

class Passengers:
    def __init__(self, num_of_stations: int, num_of_passengers: int, **kwargs):
        self.num_of_stations = num_of_stations
        self.num_of_passengers = num_of_passengers
        self.time = 24 * 60 # generating for one day accurate to the minute

        if "interchange_points" in kwargs.keys():
            interchange_points = kwargs.get("interchange_points")
            if "alfa" in kwargs.keys():
                alfa = kwargs.get("alfa")
                if alfa > 1:
                    self.travels = self.generate_with_factor_for_interchange_points(interchange_points, alfa)
            else:
                self.travels = self.generate_with_factor_for_interchange_points(interchange_points)
        else:
            self.travels = self.random_generate()

    def random_generate(self):
        travels = []
        for passenger in range(self.num_of_passengers):
            from_, to_ = sample(range(self.num_of_stations), 2)
            time = sample(range(self.time), 1)[0]
            travels.append([from_, to_, time])
        return travels

    def generate_with_factor_for_interchange_points(self, interchange_points, alfa: float = 3):
        travels = []
        weights = np.ones(self.num_of_stations)
        for station in interchange_points:
            weights[station] = alfa
        for passenger in range(self.num_of_passengers):
            from_ = choices(range(self.num_of_stations), weights=weights)[0]
            curr_weight = weights[from_]
            weights[from_] = 0
            to_ = choices(range(self.num_of_stations), weights=weights)[0]
            weights[from_] = curr_weight
            time = sample(range(self.time), 1)[0]
            travels.append([from_, to_, time])
        return travels

    def get_travels(self) -> list[[int, int, int]]:
        return self.travels
