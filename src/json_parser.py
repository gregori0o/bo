import json


class Parser:
    def __init__(self, path):
        with open(path, "r") as file:
            self.data = json.load(file)

    def get_data(self):
        return self.data
