from collections import defaultdict
from typing import List, Optional, Iterator, Tuple
from dataclasses import dataclass


@dataclass
class AdjacencyDirectedList:
    list: List['AdjacencyDirectedNode']

    @staticmethod
    def new(data: List['AdjacencyDirectedNode']) -> 'AdjacencyDirectedList':
        return AdjacencyDirectedList(data)

    @staticmethod
    def default() -> 'AdjacencyDirectedList':
        return AdjacencyDirectedList([
            AdjacencyDirectedNode(1, [2, 5]),
            AdjacencyDirectedNode(4, [5]),
            AdjacencyDirectedNode(2, [3, 5]),
            AdjacencyDirectedNode(5, []),
            AdjacencyDirectedNode(6, []),
            AdjacencyDirectedNode(3, [9]),
            AdjacencyDirectedNode(7, [3, 8]),
            AdjacencyDirectedNode(8, [9]),
            AdjacencyDirectedNode(9, [])
        ])

    def __getitem__(self, item) -> Optional['AdjacencyDirectedNode']:
        for node in self.list:
            if node.value == item:
                return node
        return None

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

def topological_sort(data: Iterator[Tuple[str, int]]) -> List[int]:
    time_values = {}
    i = 1
    for value_type, value in data:
        if value not in time_values:
            time_values[value] = [i, None]
        elif value_type == "out":
            time_values[value][1] = i
        i += 1
    res = [(key, value[1]) for key, value in time_values.items()]
    return [key for key, value in reversed(sorted(res, key=lambda k: k[1]))]



if __name__ == '__main__':
    graph = AdjacencyDirectedList.default()
    graph2 = AdjacencyDirectedList.new(
        [AdjacencyDirectedNode(1, [2, 4, 12]),
         AdjacencyDirectedNode(2, [1, 4]),
         AdjacencyDirectedNode(4, [1, 12, 2, 7, 6]),
         AdjacencyDirectedNode(12, [1, 4, 10, 11]),
         AdjacencyDirectedNode(10, [12, 11]),
         AdjacencyDirectedNode(11, [12, 10]),
         AdjacencyDirectedNode(7, [3, 4, 6]),
         AdjacencyDirectedNode(3, [7]),
         AdjacencyDirectedNode(6, [7, 4, 13, 5, 9]),
         AdjacencyDirectedNode(13, [6]),
         AdjacencyDirectedNode(5, [6, 9, 8]),
         AdjacencyDirectedNode(9, [6, 5, 8]),
         AdjacencyDirectedNode(8, [5, 9]),
         AdjacencyDirectedNode(14, [15]),
         AdjacencyDirectedNode(15, [14])],
    )
    print(f"{list((val for type, val in graph.depth_first_search() if type == 'in'))=}")
    print(f"{graph.breadth_first_search()=}")
    print(f"{graph2.depth_first_search()=}")
    print(f"{graph2.breadth_first_search()=}")
    print(f"{topological_sort(graph.depth_first_search())=}")
