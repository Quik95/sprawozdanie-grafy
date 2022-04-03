from typing import List, Optional
from dataclasses import dataclass


@dataclass
class AdjacencyDirectedList:
    list: List['AdjacencyDirectedNode']

    @staticmethod
    def default() -> 'AdjacencyDirectedList':
        return AdjacencyDirectedList([
            AdjacencyDirectedNode(1, AdjacencyDirectedNode(2, AdjacencyDirectedNode(5, None))),
            AdjacencyDirectedNode(4, AdjacencyDirectedNode(5, None)),
            AdjacencyDirectedNode(2, AdjacencyDirectedNode(3, AdjacencyDirectedNode(5, None))),
            AdjacencyDirectedNode(5, None),
            AdjacencyDirectedNode(6, None),
            AdjacencyDirectedNode(3, AdjacencyDirectedNode(9, None)),
            AdjacencyDirectedNode(7, AdjacencyDirectedNode(3, AdjacencyDirectedNode(8, None))),
            AdjacencyDirectedNode(8, AdjacencyDirectedNode(9, None)),
            AdjacencyDirectedNode(9, None)
        ])

    def __getitem__(self, item) -> Optional['AdjacencyDirectedNode']:
        for node in self.list:
            if node.value == item:
                return node
        return None

    def depth_first_search(self):
        values: List[int] = [self.list[0].value]
        stack: List[int] = [self.list[0].value]
        while len(values) != len(self.list):
            # restartuj od izolowanych
            if len(stack) == 0:
                for item in self.list:
                    if item.value not in values:
                        values.append(item.value)
                        stack.append(item.value)
                        continue
                # wszystkie znalezione
                if len(stack) == 0:
                    break
            node: AdjacencyDirectedNode = self.find_by_value(stack[-1])
            all_next_unvisited = node.get_all_next(values)
            if len(all_next_unvisited) == 0:
                stack.pop()
                continue
            values.append(all_next_unvisited[0])
            stack.append(all_next_unvisited[0])

        return values

    def find_by_value(self, value: int) -> Optional['AdjacencyDirectedNode']:
        for item in self.list:
            if item.value == value:
                return item
        return None


@dataclass
class AdjacencyDirectedNode:
    value: int
    next_node: Optional['AdjacencyDirectedNode']

    def get_all_next(self, already_visited: List[int]) -> List[int]:
        res = []
        curr = self.next_node
        while curr:
            if curr.value not in already_visited:
                res.append(curr.value)
            curr = curr.next_node
        return res


if __name__ == '__main__':
    graph = AdjacencyDirectedList.default()
    print(f"{graph.depth_first_search()=}")


