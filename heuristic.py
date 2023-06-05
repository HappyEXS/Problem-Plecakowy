from typing import List, Tuple


class HeuristicMethodKnapsackProblem:
    """
    Heuristic method for knapsack problem

    Attributes:
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
        self.dataset = dataset
        self._sort_elements()

    def _get_price_to_weight_ratio(self, item: Tuple[float, float]) -> float:
        return round(item[0] / item[1], 2)

    def _sort_elements(self) -> None:
        self.dataset = sorted(self.dataset, key=self._get_price_to_weight_ratio)
        self.dataset = list(reversed(self.dataset))

    def solve(self) -> None:
        value_of_packed_items = 0
        weight_of_packed_items = 0
        self.packed = []

        for element in self.dataset:
            if (element[1] + weight_of_packed_items) <= self.knapsack_capacity:
                self.packed.append(element)
                value_of_packed_items += element[0]
                weight_of_packed_items += element[1]

        self.value_of_packed_items = value_of_packed_items
        return self.get_value_of_knapsack()

    def get_knapsack(self) -> List[Tuple[float, float]]:
        return self.packed

    def get_value_of_knapsack(self) -> float:
        return self.value_of_packed_items

    def get_items(self) -> List[Tuple[float, float]]:
        return self.dataset
