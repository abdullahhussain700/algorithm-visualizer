"""Array generation and validation helpers."""

import random

MIN_ARRAY_SIZE = 8
MAX_ARRAY_SIZE = 80
DATA_TYPES = [
    {"label": "Random", "value": "random"},
    {"label": "Nearly sorted", "value": "nearly-sorted"},
    {"label": "Reversed", "value": "reversed"},
]


def normalize_size(size: int | float | None) -> int:
    """Clamp invalid UI values to the supported array-size range."""
    try:
        normalized = int(size or MIN_ARRAY_SIZE)
    except (TypeError, ValueError):
        normalized = MIN_ARRAY_SIZE
    return max(MIN_ARRAY_SIZE, min(MAX_ARRAY_SIZE, normalized))


def generate_array(size: int | float | None, data_type: str | None) -> list[int]:
    """Create a fresh input array for the visualizer."""
    size = normalize_size(size)
    if data_type == "nearly-sorted":
        values = list(range(10, 10 + size))
        for _ in range(max(1, size // 5)):
            first, second = random.sample(range(size), 2)
            values[first], values[second] = values[second], values[first]
        return values
    if data_type == "reversed":
        return list(range(100, 100 - size, -1))
    return [random.randint(10, 100) for _ in range(size)]
