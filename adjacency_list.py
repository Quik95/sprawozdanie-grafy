from dataclasses import dataclass
from typing import List, Iterator, Tuple, Dict


class AdjacencyDirectedList:
    list: List['AdjacencyDirectedNode']

    def depth_first_search(self) -> Iterator[Tuple[str, int]]:
        values: List[int] = [self.list[0].value]
        stack: List[int] = [self.list[0].value]
        yield "in", stack[0]
        while len(values) != len(self.list):
            # restartuj od izolowanych
            if len(stack) == 0:
                for item in self.list:
                    if item.value not in values:
                        values.append(item.value)
                        stack.append(item.value)
                        yield "in", item.value
                        break
                # wszystkie znalezione
                if len(stack) == 0:
                    break
            node: AdjacencyDirectedNode = self[stack[-1]]
            all_next_unvisited = node.get_all_next(values)
            if len(all_next_unvisited) == 0:
                yield "out", stack.pop()
                continue
            values.append(all_next_unvisited[0])
            stack.append(all_next_unvisited[0])
            yield "in", all_next_unvisited[0]
        while len(stack) > 0:
            yield "out", stack.pop()
        return None

    def breadth_first_search(self) -> List[int]:
        values: List[int] = []
        queue: List[int] = [self.list[0].value]

        while len(values) != len(self.list):
            if len(queue) == 0:
                for item in self.list:
                    if item.value not in values:
                        queue.append(item.value)
                        break
                if len(queue) == 0:
                    break
            node: AdjacencyDirectedNode = self[queue[0]]
            for adjacent in node.adjacent_nodes:
                if adjacent not in values and adjacent not in queue:
                    queue.append(adjacent)
            values.append(node.value)
            queue.pop(0)
        return values

    def number_of_return_nodes(self, data: Dict[int, List[int]]) -> int:
        keys = list(data.keys())
        n = 0
        for i in range(0, len(keys)):
            for j in range(i + 1, len(keys)):
                v = keys[i]
                u = keys[j]
                if u in self[v].adjacent_nodes and data[v][0] < data[u][0] < data[u][1] < data[v][1]:
                    n += 1
        return n

    def __getitem__(self, item: int) -> 'AdjacencyDirectedNode':
        return self.list[item - 1]


@dataclass
class AdjacencyDirectedNode:
    value: int
    adjacent_nodes: List[int]

    def get_all_next(self, already_visited: List[int]) -> List[int]:
        if len(self.adjacent_nodes) == 0:
            return []
        res = []
        for item in self.adjacent_nodes:
            if item not in already_visited:
                res.append(item)
        return res
