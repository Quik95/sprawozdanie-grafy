from typing import List, Tuple, Dict


class ListOfEdges:
    list: List[Tuple[int, int]]

    def has(self, i: int, j: int) -> bool:
        for p in self.list:
            if p[0] == i and p[1] == j:
                return True
        return False

    def number_of_return_nodes(self, data: Dict[int, List[int]]) -> int:
        keys = list(data.keys())
        n = 0
        for i in range(0, len(keys)):
            for j in range(i + 1, len(keys)):
                v = keys[i]
                u = keys[j]
                if self.has(v, u) and data[v][0] < data[u][0] < data[u][1] < data[v][1]:
                    n += 1
        return n
