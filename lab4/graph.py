from collections import deque
from random import randint
from time import time

class Graph:
    adjacency_matrix = None
    incidence_matrix = None
    adjacency_list = None
    ribs_list = None
    directed = None

    def get_adjacency_matrix(self):
        N = len(self.adjacency_list)
        self.adjacency_matrix = [[0] * N for i in range(N)]
        for i in range(N):
            for j in self.adjacency_list[i]:
                self.adjacency_matrix[i][j] = 1
        for i in self.adjacency_matrix:
            print(i)

    def get_incidence_matrix(self):
        M = len(self.ribs_list)
        N = len(self.adjacency_list)
        self.incidence_matrix = [[0] * M for i in range(N)]
        for i in range(M):
            for j in range(N):
                if self.directed:
                    if (i, j) in self.ribs_list:
                        self.incidence_matrix[i][j] = 1
                    if (j, i) in self.ribs_list:
                        self.incidence_matrix[i][j] = -1
                else:
                    if (i, j) in self.ribs_list or (j, i) in self.ribs_list:
                        self.incidence_matrix[i][j] = 1
        for i in self.incidence_matrix:
            print(i)


    def get_adjacency_list(self):
        return self.adjacency_list

    def get_ribs_list(self):
        return self.ribs_list

class Generate:
    min_peaks = 0
    max_peaks = 0
    min_ribs = 0
    max_ribs = 0
    max_ribs_for_peaks = 0
    directed = False
    inc_ribs = 0
    out_ribs = 0

    def __init__(self, min_peaks, max_peaks, min_ribs, max_ribs, max_ribs_for_peaks, inc_ribs, out_ribs, directed = False) -> None:
        self.min_peaks = min_peaks
        self.max_peaks = max_peaks
        self.min_ribs = min_ribs
        self.max_ribs = max_ribs
        self.max_ribs_for_peaks = max_ribs_for_peaks
        self.inc_ribs = inc_ribs
        self.out_ribs = out_ribs
        self.directed = directed

    def generate_graph(self):
        M = randint(self.min_peaks, self.max_peaks)
        N = randint(self.min_ribs, self.max_ribs)
        ribs_list = set()
        graph = ({i:set() for i in range(M)})
        i = 0
        while i != N:
            v1, v2 = [randint(0, len(graph) - 1) for i in range(2)]
            if self.directed:
                if len(graph[v1]) < self.max_ribs_for_peaks and len(graph[v1]) < self.out_ribs and len(graph[v2]) < self.inc_ribs:
                    graph[v1].add(v2)
                    graph[v2].add(v1)
                    ribs_list.add((v1, v2))
                    i += 1
            else:
                if len(graph[v1]) < self.max_ribs_for_peaks and len(graph[v2]) < self.max_ribs_for_peaks:
                    graph[v1].add(v2)
                    graph[v2].add(v1)
                    ribs_list.add((v1, v2))
                    i += 1
        return graph, tuple(ribs_list), self.directed

def bfs(graph:Graph, start_vertex, end_vertex):
    cur_graph = graph.get_adjacency_list()
    parents = [None] * len(cur_graph) 
    distances = [None] * len(cur_graph)
    distances[start_vertex] = 0
    queue = deque([start_vertex])

    while queue:
        cur_v = queue.popleft()
        for neigh_v in cur_graph[cur_v]:
            if distances[neigh_v] is None:
                distances[neigh_v] = distances[cur_v] + 1
                parents[neigh_v] = cur_v
                queue.append(neigh_v)
    
    path = [end_vertex]
    parent = parents[end_vertex]
    while not parent is None:
        path.append(parent)
        parent = parents[parent]
    if len(path) == 1 and path[0] not in cur_graph[path[0]]:
        return None
    else:
        return path[::-1]

def dfs(graph, start, stop, visited=None, res=None):
    if res is None:
        res = []
    if visited is None:
        visited = set()
    visited.add(start)
    res.append(start)
    for next in graph[start] - visited:
        if next == stop:
            visited.add(next)
            res.append(next)
            return res
        dfs(graph, next, stop, visited, res)
    if stop not in res:
        return None
    else:
        return res

def analys(dfs_r = False, bfs_r = False):
    graphs = [Graph() for i in range(10)]
    peaks = [100 * i for i in range(1, 11)]
    ribs = [400 * i  for i in range(1, 11)]
    for i in enumerate(graphs):
        start_time = time()
        i[1].adjacency_list, i[1].ribs_list, i[1].directed = Generate(
            peaks[i[0]],
            peaks[i[0]] * 1.5,
            ribs[i[0]],
            ribs[i[0]] * 1.5,
            ribs[i[0]] / 2,
            ribs[i[0]],
            ribs[i[0]],
            False,
        ).generate_graph()
        flag = randint(0, 1)
        coords_1 = i[1].ribs_list[randint(0, len(i[1].ribs_list))][0]
        coords_2 = i[1].ribs_list[randint(0, len(i[1].ribs_list))][0]
        if bfs_r:
            res = dfs(i[1].adjacency_list, coords_1, coords_2)
            stop_time = time() - start_time
            if res is None:
                print(None, "dfs", stop_time)
            else:
                print(len(res), "dfs", stop_time)
        elif dfs_r:
            res = bfs(i[1], coords_1, coords_2)
            stop_time = time() - start_time
            if res is None:
                print(None, "bfs", stop_time)
            else:
                print(len(res), "bfs", stop_time)

# analys(dfs_r=True)
# print("-----------------------")
# analys(bfs_r=True)

graph = Graph()
graph.adjacency_list, graph.ribs_list, graph.directed = Generate(6, 12, 10, 15, 10, 10, 10, True).generate_graph()
print("Матрица смежности:")
graph.get_adjacency_matrix()
print("\nМатрица инцедентности:")
graph.get_incidence_matrix()
print("\nСписок смежности:")
print(graph.get_adjacency_list())
print("\nСписок ребер:")
print(graph.get_ribs_list())