import numpy as np
from typing import List, Tuple
from copy import deepcopy


class Node:
    """
    Representation of a node in the tree-alike representation of a knapsack problem

    Atributes:
    backpack: binary array - n-th element of an array represents the n-th item in the backpack
        1-item selected, 0- item not selected
    level: int - tier of the node in the tree (for root level=0)
        Inforamtion on how many bits in backpack are in the final state.
        Bits from level's place are not permanent, just fielld as zeros.
    h: float - heuristic function
    g: float - value of the knapsack
    weight: float - weight of the knapsac
    """

    def __init__(self, backpack: np.ndarray, level: int):
        self.backpack = backpack
        self.level = level
        self.h = None
        self.g = None
        self.weight = None

    def set_h(self, value: float):
        self.h = value

    def set_g(self, value: float):
        self.g = value

    def set_weight(self, value: float):
        self.weight = value

    def get_f(self):
        return self.g + self.h


class Astar:
    """
    Astar algorithm for knapsac problem

    Atributes:
        dataset: list of items - available items to choose
            item: tuple - consist of two float numbers (value, weight)
        knapsack_capasity: float - maximum weight of items in knapsack

    Methods:
        solve - solves the knapsack problem, writes results to the class variables
        get_knapsack - returns list of chosen items to the knapsack
        get_value_of_knapsack - returns value of items in the knapsack
    """

    def __init__(self, dataset: List[Tuple[float, float]], knapsack_capacity: float) -> None:
        self.knapsack_capacity = knapsack_capacity
        self.dataset = self._sort_dataset(dataset)
        self.num_of_elements = len(dataset)

    def _sort_dataset(self, dataset: List[Tuple[float, float]]):
        sorted_dataset = sorted(dataset, key=self._get_price_to_weight_ratio)
        return list(reversed(sorted_dataset))

    def _get_price_to_weight_ratio(self, item: Tuple[float, float]) -> float:
        return round(item[0] / item[1], 2)

    def _generate_children(self, node: Node) -> Tuple[Node, Node]:
        backpack0, backpack1 = node.backpack, deepcopy(node.backpack)
        backpack1[node.level] = 1
        return (
            Node(backpack0, node.level + 1),
            Node(backpack1, node.level + 1),
        )

    def _set_g(self, node: Node) -> int:
        value_sum, weight_sum = 0, 0
        for i in range(len(node.backpack)):
            value_sum += node.backpack[i] * self.dataset[i][0]
            weight_sum += node.backpack[i] * self.dataset[i][1]

        if weight_sum > self.knapsack_capacity:
            node.set_g(0)
            node.set_h(0)
            return -1
        node.set_g(value_sum)
        node.set_weight(weight_sum)
        return 0

    def _set_h(self, node: Node) -> None:
        max_value, weight_of_packed_items = 0, node.weight
        for item in self.dataset[node.level :]:
            if item[1] + weight_of_packed_items <= self.knapsack_capacity:
                max_value += item[0]
                weight_of_packed_items += item[1]
            else:
                max_value += round(item[0] / item[1], 2) * (self.knapsack_capacity - weight_of_packed_items)
                break
        node.set_h(max_value)

    def _set_f(self, node: Node) -> None:
        if self._set_g(node) == -1:
            return 0
        self._set_h(node)

    def solve(self) -> None:
        queue = []
        empty_backpack = np.zeros(self.num_of_elements, dtype=np.int)
        tmp_node = Node(empty_backpack, 0)
        self._set_f(tmp_node)
        queue.append(tmp_node)

        while True:
            tmp_node = queue[0]
            for node in queue[1:]:
                if node.get_f() > tmp_node.get_f():
                    tmp_node = node

            if tmp_node.level == self.num_of_elements:
                break

            queue.remove(tmp_node)
            node0, node1 = self._generate_children(tmp_node)
            self._set_f(node0)
            self._set_f(node1)
            queue.append(node0)
            queue.append(node1)

        self.final_backpack = tmp_node
        return self.get_value_of_knapsack()

    def get_knapsack(self) -> List[Tuple[float, float]]:
        packed = []
        for i in range(self.num_of_elements):
            if self.final_backpack.backpack[i] == 1:
                packed.append(self.dataset[i])
        return packed

    def get_value_of_knapsack(self) -> float:
        return self.final_backpack.g
