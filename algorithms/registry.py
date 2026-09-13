"""Algorithm metadata and registration hooks."""

from dataclasses import dataclass
from typing import Optional

from .bubble import bubble_sort
from .heap_sort import heap_sort
from .insertion_sort import insertion_sort
from .merge_sort import merge_sort
from .protocol import SortingAlgorithm
from .quick_sort import quick_sort
from .selection_sort import selection_sort


@dataclass(frozen=True)
class AlgorithmSpec:
    value: str
    label: str
    description: str
    how_it_works: str
    best_time: str
    average_time: str
    worst_time: str
    space: str
    stable: bool
    in_place: bool
    implementation: Optional[SortingAlgorithm] = None


ALGORITHM_SPECS = (
    AlgorithmSpec("bubble", "Bubble Sort", "Compare neighboring values and exchange them when needed.", "Repeatedly compare adjacent values, bubbling the largest remaining value to the end.", "O(n)", "O(n^2)", "O(n^2)", "O(1)", True, True, bubble_sort),
    AlgorithmSpec("selection", "Selection Sort", "Select the next smallest value and place it in order.", "Find the smallest value in the unsorted region and swap it into the next open position.", "O(n^2)", "O(n^2)", "O(n^2)", "O(1)", False, True, selection_sort),
    AlgorithmSpec("insertion", "Insertion Sort", "Build the sorted prefix one value at a time.", "Take the next value and shift larger sorted values right until it fits.", "O(n)", "O(n^2)", "O(n^2)", "O(1)", True, True, insertion_sort),
    AlgorithmSpec("merge", "Merge Sort", "Divide the data, then combine sorted sections.", "Split the array into halves, sort each half, and merge the ordered halves together.", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)", True, False, merge_sort),
    AlgorithmSpec("quick", "Quick Sort", "Partition around a pivot and sort each section.", "Choose a pivot, move smaller values before it, and recursively sort both partitions.", "O(n log n)", "O(n log n)", "O(n^2)", "O(log n) avg / O(n) worst", False, True, quick_sort),
    AlgorithmSpec("heap", "Heap Sort", "Use a heap structure to repeatedly select the next value.", "Build a max heap, move its largest value to the end, and restore the heap repeatedly.", "O(n log n)", "O(n log n)", "O(n log n)", "O(1)", False, True, heap_sort),
)

ALGORITHMS = [{"label": spec.label, "value": spec.value} for spec in ALGORITHM_SPECS]


def get_algorithm(value: str | None) -> Optional[SortingAlgorithm]:
    """Return a registered implementation, or ``None`` when it is missing."""
    spec = next((item for item in ALGORITHM_SPECS if item.value == value), None)
    return spec.implementation if spec else None


def get_algorithm_description(value: str | None) -> str:
    """Return readable metadata for a selected algorithm."""
    spec = next((item for item in ALGORITHM_SPECS if item.value == value), None)
    return spec.description if spec else "Choose an algorithm to begin."


def get_algorithm_spec(value: str | None) -> AlgorithmSpec | None:
    """Return the complete metadata record for a selected algorithm."""
    return next((item for item in ALGORITHM_SPECS if item.value == value), None)
