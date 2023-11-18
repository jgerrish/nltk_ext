import json

class Graph:
    def __init__(self, directed=False):
        self.graph = {}
        self.directed = directed

    def vertices(self):
        if self.directed == False:
            return self.graph.keys()
        else:
            vertices = set()
            for v1 in self.graph.keys():
                vertices.add(v1)
                for v2 in self.graph[v1]:
                    vertices.add(v2)
            return list(vertices)

    def get_vertex(self, v):
        if v in self.graph:
            return self.graph[v]

    def get_edge(self, v1, v2):
        if v1 in self.graph:
            if v2 in self.graph[v1]:
                return self.graph[v1][v2]
        return None

    def neighbors(self, v):
        if v in self.graph:
            return self.graph[v].keys()
        else:
            return []

    def add_edge(self, src, dest, val=True):
        if src not in self.graph:
            self.graph[src] = {}

        self.graph[src][dest] = val

        if self.directed == False:
            if dest not in self.graph:
                self.graph[dest] = {}
            self.graph[dest][src] = val

    # Add an edge to the graph with value 1
    # If the edge already exists, increment its value
    def inc_edge(self, src, dest):
        if src not in self.graph:
            self.graph[src] = {}

        if dest not in self.graph[src]:
            self.graph[src][dest] = 1
        else:
            self.graph[src][dest] += 1

        if self.directed == False:
            if dest not in self.graph:
                self.graph[dest] = {}
            if src not in self.graph[dest]:
                self.graph[dest][src] = 1
            else:
                self.graph[dest][src] += 1

    def remove_vertex(self, v):
        if v in self.graph:
            for dest in self.graph[v]:
                if v in self.graph[dest]:
                    del self.graph[dest][v]
            del self.graph[v]

    def __str__(self):
        return self.as_json()

    def as_json(self):
        return json.dumps(self.graph, sort_keys=True, indent=4, separators=(',', ': '))

    def as_edgelist(self):
        s = ""
        for v1 in self.vertices():
            for v2 in self.graph[v1].keys():
                s += v1 + " " + v2 + " " + str(self.graph[v1][v2]) + "\n"

        if self.directed == True:
            for v2 in self.vertices():
                for v1 in self.graph[v2].keys():
                    s += v2 + " " + v1 + " " + str(self.graph[v2][v1]) + "\n"

        return s
