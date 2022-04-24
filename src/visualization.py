import graphviz
import random

# colors:
# https://graphviz.org/doc/info/colors.html

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
        self.graph.view(filename=filename, directory='../utils/visualizations/graphs')


class SolutionVisualizer:
    def __init__(self, size, edges, lines):
        self.graph = graphviz.Graph('Buses lines', engine='sfdp')


g = graphviz.Graph('Buses lines', filename='../utils/visualizations/buses_lines/buses_lines.gv', engine='sfdp')

# creates random colors for edges
NUM_OF_LINES = 4
r = lambda: random.randint(150, 255)
colors = ['#%02X%02X%02X' % (r(),r(),r()) for line in range(NUM_OF_LINES)]
# print(colors)

# adds transfer stations
g.attr('node', shape='doubleoctagon', style='filled', fillcolor='lightcoral', fixedsize='true')
g.node('#2')
g.node('#6')
g.node('#7')
g.node('#8')


# adds unattended line segments
g.attr('node', shape='circle', style='filled', fillcolor='lightskyblue1')
g.attr('edge', penwidth='1')
g.edge('#2', '#3', label='3')
g.edge('#6', '#8', label='3')

# adds attended line segments
g.attr('edge', penwidth='5')
g.edge('#1', '#2', label='3', color=colors[0])
g.edge('#2', '#4', label='2', color=colors[0])
g.edge('#4', '#5', label='1', color=colors[1])
g.edge('#5', '#8', label='1', color=colors[1])
g.edge('#3', '#6', label='5', color=colors[2])
g.edge('#6', '#7', label='6', color=colors[2])
g.edge('#7', '#10', label='2', color=colors[2])
g.edge('#7', '#8', label='3', color=colors[3])
g.edge('#8', '#9', label='5', color=colors[3])
g.edge('#9', '#10', label='4', color=colors[3])

g

# creates pdf file
# g.view()