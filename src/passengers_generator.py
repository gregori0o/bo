from random import sample

class Passengers:
    def __init__(self, num_of_stations: int, num_of_passengers: int):
        self.num_of_stations = num_of_stations
        self.num_of_passengers = num_of_passengers
        self.time = 24 * 60 # generating for one day accurate to the minute
        self.travels = self.random_generate()

    def random_generate(self):
        travels = []
        for passenger in range(self.num_of_passengers):
            from_, to_ = sample(range(self.num_of_stations), 2)
            time = sample(range(self.time), 1)[0]
            travels.append([from_, to_, time])
        return travels

    def get_travels(self) -> list[[int, int, int]]:
        return self.travels

# example
# p = Passengers(5, 10)
# travels = p.get_travels()
# print(travels)