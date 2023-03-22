from audioop import reverse
from collections import deque
from random import randint
import sys
from time import time

class Graph:
    peaks = 0
    min_ribs = 0
    max_ribs = 0
    min_ribs_for_peaks = 0
    directed = False
    inc_ribs = 0
    out_ribs = 0
    graph = None
    adjacency_matrix = None
    ribs_list = None

    def __init__(self, peaks, min_ribs_for_peaks, inc_ribs, out_ribs, directed = False) -> None:
        self.peaks = peaks
        self.min_ribs_for_peaks = min_ribs_for_peaks
        self.inc_ribs = inc_ribs
        self.out_ribs = out_ribs
        self.directed = directed
        self.generate_graph()
        self.get_adjacency_matrix()

    def generate_graph(self):
        M = self.peaks
        ribs_list = set()
        graph = ({i:set() for i in range(M)})
        i = 0
        while i != M:
            v1, v2 = [i, randint(0, len(graph) - 1)]
            weight = randint(1, 20)
            if self.directed:
                graph[v1].add(v2)
                graph[v2].add(v1)
                ribs_list.add((v1, v2))
                if len(graph[v1]) < self.min_ribs_for_peaks and len(graph[v1]) < self.out_ribs and len(graph[v2]) < self.inc_ribs:
                    i += 1
            else:
                if len(graph[i]) >= self.min_ribs_for_peaks:
                    i += 1
                else:
                    graph[v1].add(v2)
                    graph[v2].add(v1)
                    ribs_list.add((v1, v2, weight))
        self.graph = graph
        self.ribs_list = ribs_list
        # return graph, tuple(ribs_list), self.directed

    def get_adjacency_matrix(self):
        graph = [[0] * len(self.graph) for i in range(len(self.graph))]
        
        for i in self.ribs_list:
            graph[i[0]][i[1]] = i[2]
            graph[i[1]][i[0]] = i[2]

        self.adjacency_matrix = graph

        for i in self.adjacency_matrix:
            print(i)

        return graph



def dijkstra(graph, start):
    # init
    visited = []
    distance = {start: 0}
    node = list(range(len(graph[0])))
    if start in node:
        node.remove(start)
        visited.append(start)
    else:
        return None
    for i in node:
        distance[i] = graph[start][i]
    prefer = start
    while node:
        _distance = float('inf')
        for i in visited:
            for j in node:
                if graph[i][j] > 0:
                    if _distance > distance[i] + graph[i][j]:
                        _distance = distance[j] = distance[i] + graph[i][j]
                        prefer = j
        visited.append(prefer)
        node.remove(prefer)
    print(distance)
    return distance

def get_path(graph, distansec, start):
    path = dict()
    for i in distansec:
        path[i] = []
    for i in path:
        k = i
        while k != start:
                for j in enumerate(graph[k]):
                    if j[1] != 0:
                        if distansec[j[0]] == (distansec[k] - graph[k][j[0]]):
                            path[i].append(k)
                            k = j[0]
                            break
    for el in path.values():
        el.reverse()
    print(path)
    return path


def analys():
    times = []
    peaks = [100, 200, 500, 1000]
    min_ribs = [30, 40, 100, 200]
    for i in range(len(peaks)):
        start_time = time()
        graph = Graph(peaks[i], min_ribs[i], 10, 10, False)
        weight_peaks = dijkstra(graph.adjacency_matrix, 0)
        path = get_path(graph.adjacency_matrix, weight_peaks, 0)
        times.append(time() - start_time)
    print(f"Times: {times}")

# analys()
peaks = 10
min_ribs = 3
graph = Graph(peaks, min_ribs, 10, 10, False)
weight_peaks = dijkstra(graph.adjacency_matrix, 0)
path = get_path(graph.adjacency_matrix, weight_peaks, 0)