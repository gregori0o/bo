import graphviz
import random


# colors:
# https://graphviz.org/doc/info/colors.html
def create_colors_for_lines(num_of_lines: int):
    # creates random colors for edges (from 150 because want to make colors less vivid)
    r = lambda: random.randint(150, 255)
    colors = ['#%02X%02X%02X' % (r(), r(), r()) for line in range(num_of_lines)]
    return colors


class GraphVisualizer:
    def __init__(self, size: int, edges: tuple[any, any, int]):
        self.graph = graphviz.Graph('Graph', engine='sfdp')
        self.add_nodes(size)
        self.add_edges(edges)

    def add_nodes(self, size):
        self.graph.attr('node', shape='circle', style='filled', fillcolor='lightskyblue1')
        for i in range(size):
            self.graph.node('#' + str(i))

    def add_edges(self, edges):
        for x, y, val in edges:
            self.graph.attr('edge', penwidth='1')
            self.graph.edge('#' + str(x), '#' + str(y), label=str(val))

    def show(self):
        return self.graph

    def save(self, filename: str):
        self.graph.view(filename=filename, directory='utils/visualizations/graphs')


class LinesVisualizer:
    def __init__(self, size: int, edges: tuple[any, any, int], lines: list[list[tuple]], stations: tuple):
        self.colors = create_colors_for_lines(len(lines))
        self.graph = graphviz.Graph('Buses lines', engine='sfdp')
        self.graph.attr(label='\n'.join(['{} -> {}'.format(i, [bs for bs, _ in line]) for i, line in enumerate(lines)]))
        self.add_interchange_stations(stations)
        self.add_edges(edges)
        self.add_lines(lines, edges)

    def add_interchange_stations(self, stations):
        self.graph.attr('node', shape='doubleoctagon', style='filled', fillcolor='lightcoral', fixedsize='true')
        for no_station in stations:
            self.graph.node('#' + str(no_station))
        self.graph.attr('node', shape='circle', style='filled', fillcolor='lightskyblue1', fixedsize='true')

    def add_lines(self, lines, edges):
        self.graph.attr('edge', penwidth='5')
        for idx, line in enumerate(lines):
            i, j = 0, 1
            while j < len(line):
                self.graph.edge('#' + str(line[i][0]), '#' + str(line[j][0]), color=self.colors[idx], label=str(line[i][1]))
                i += 1
                j += 1

    def add_edges(self, edges):
        for x, y, val in edges:
            self.graph.attr('edge', penwidth='1')
            self.graph.edge('#' + str(x), '#' + str(y), label=str(val))

    def show(self):
        return self.graph

    def save(self, filename: str):
        self.graph.view(filename=filename, directory='utils/visualizations/lines')


class SolutionVisualizer:
    def __init__(self, size: int, edges: tuple[any, any, int], lines: tuple, stations: tuple):
        self.colors = create_colors_for_lines(len(lines))
        self.graph = graphviz.Graph('Buses lines', engine='sfdp')
        self.add_interchange_stations(stations)
        self.add_lines_segments(lines, edges)
        # self.add_unattended_line_segments(edges)

    def add_interchange_stations(self, stations):
        self.graph.attr('node', shape='doubleoctagon', style='filled', fillcolor='lightcoral', fixedsize='true')
        for no_station in stations:
            self.graph.node('#' + str(no_station))

    def add_lines_segments(self, lines, edges):
        self.graph.attr('edge', penwidth='5')
        for idx, line in enumerate(lines):
            i, j = 0, 1
            while j < len(line):
                for x, y, val in edges:
                    if (line[i] == x and line[j] == y) or (line[i] == x and line[j] == y):
                        self.graph.edge('#' + str(line[i]), '#' + str(line[j]), label=str(val), color=self.colors[idx])
                        break
                i += 1
                j += 1

    def add_unattended_line_segments(self, edges):
        self.graph.attr('node', shape='circle', style='filled', fillcolor='lightskyblue1')

    def show(self):
        return self.graph

    def save(self, filename: str):
        self.graph.view(filename=filename, directory='utils/visualizations/buses_lines')

