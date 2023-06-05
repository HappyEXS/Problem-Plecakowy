import numpy as np
from typing import List, Tuple


def get_uniform(from_a: int, to_b: int) -> float:
    return np.random.uniform(from_a, to_b)


def generate_uncorrelated(
    num_of_items: int, max_weight: int
) -> List[Tuple[float, float]]:
    data = []
    for _ in range(num_of_items):
        weight = get_uniform(1, max_weight)
        value = get_uniform(1, max_weight)
        data.append((round(value, 2), round(weight, 2)))
    return data


def generate_semicorrelated(
    num_of_items: int, max_weight: int
) -> List[Tuple[float, float]]:
    data = []
    for _ in range(num_of_items):
        weight = get_uniform(1, max_weight)
        value = weight + get_uniform(-(max_weight / 2), max_weight / 2)
        value = max(value, 1)
        data.append((round(value, 2), round(weight, 2)))
    return data


def generate_correlated(
    num_of_items: int, max_weight: int
) -> List[Tuple[float, float]]:
    data = []
    for _ in range(num_of_items):
        weight = get_uniform(1, max_weight)
        value = weight + (max_weight / 2)
        data.append((round(value, 2), round(weight, 2)))
    return data
