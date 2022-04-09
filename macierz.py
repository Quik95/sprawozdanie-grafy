from typing import List, Dict

from adjacency_list import AdjacencyDirectedList, AdjacencyDirectedNode
from list_of_edges import ListOfEdges


class AdjacencyMatrix:
    list: List[List[int]]

    def __getitem__(self, index: int) -> List[int]:
        return self.list[index]

    def get(self, i: int, j: int) -> int:
        return self.list[i - 1][j - 1]

    def calculate_density(self) -> float:
        e = sum([sum(row) for row in self.list])
        v = len(self.list)
        return e / (v * (v - 1))

    def to_adjacency_list(self) -> AdjacencyDirectedList:
        l = AdjacencyDirectedList()
        l.list = [0 for _ in range(len(self.list))]

        for i, row in enumerate(self.list):
            t = AdjacencyDirectedNode(i + 1, [])
            for j, item in enumerate(row):
                if item == 1:
                    t.adjacent_nodes.append(j + 1)
            l.list[i] = t

        return l

    def to_list_of_edges(self) -> ListOfEdges:
        l = ListOfEdges()
        l.list = []

        for i, row in enumerate(self.list):
            for j, item in enumerate(row):
                if item == 1:
                    l.list.append((i + 1, j + 1))
        return l

    def number_of_return_nodes(self, data: Dict[int, List[int]]) -> int:
        keys = list(data.keys())
        n = 0
        for i in range(0, len(keys)):
            for j in range(i + 1, len(keys)):
                v = keys[i]
                u = keys[j]
                if self.list[v - 1][u - 1] == 1 and data[v][0] < data[u][0] < data[u][1] < data[v][1]:
                    n += 1
        return n
