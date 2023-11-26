from typing import Any, Dict, List, Set

import json

VertexType = Any
EdgeType = List[Any]
GraphType = Dict[Any, Any]


class Graph:
    def __init__(self, directed: bool = False) -> None:
        self.graph: GraphType = {}
        self.directed = directed

    def vertices(self) -> Set[VertexType]:
        if not self.directed:
            return set(self.graph.keys())
        else:
            vertices = set()
            for v1 in self.graph.keys():
                vertices.add(v1)
                for v2 in self.graph[v1]:
                    vertices.add(v2)
            return vertices

    def get_vertex(self, v: Any) -> VertexType:
        if v in self.graph:
            return self.graph[v]

    def get_edge(self, v1: Any, v2: Any) -> EdgeType:
        if v1 in self.graph:
            if v2 in self.graph[v1]:
                return self.graph[v1][v2]
        return None

    def neighbors(self, v: Any) -> List[VertexType]:
        if v in self.graph:
            return self.graph[v].keys()
        else:
            return []

    def add_edge(self, src: VertexType, dest: VertexType, val: bool = True) -> None:
        if src not in self.graph:
            self.graph[src] = {}

        self.graph[src][dest] = val

        if not self.directed:
            if dest not in self.graph:
                self.graph[dest] = {}
            self.graph[dest][src] = val

    # Add an edge to the graph with value 1
    # If the edge already exists, increment its value
    def inc_edge(self, src: VertexType, dest: VertexType) -> None:
        if src not in self.graph:
            self.graph[src] = {}

        if dest not in self.graph[src]:
            self.graph[src][dest] = 1
        else:
            self.graph[src][dest] += 1

        if not self.directed:
            if dest not in self.graph:
                self.graph[dest] = {}
            if src not in self.graph[dest]:
                self.graph[dest][src] = 1
            else:
                self.graph[dest][src] += 1

    def remove_vertex(self, v: VertexType) -> None:
        if v in self.graph:
            for dest in self.graph[v]:
                if v in self.graph[dest]:
                    del self.graph[dest][v]
            del self.graph[v]

    def __str__(self) -> str:
        return self.as_json()

    def as_json(self) -> str:
        return json.dumps(self.graph, sort_keys=True, indent=4, separators=(",", ": "))

    def as_edgelist(self) -> str:
        s = ""
        for v1 in self.vertices():
            for v2 in self.graph[v1].keys():
                s += v1 + " " + v2 + " " + str(self.graph[v1][v2]) + "\n"

        if self.directed:
            for v2 in self.vertices():
                for v1 in self.graph[v2].keys():
                    s += v2 + " " + v1 + " " + str(self.graph[v2][v1]) + "\n"

        return s
