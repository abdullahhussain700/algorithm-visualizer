"""Generator-based Heap Sort implementation."""

from collections.abc import Iterator

from .protocol import AlgorithmState


def heap_sort(data: list[int]) -> Iterator[AlgorithmState]:
    """Yield visualization frames while sorting a copy of ``data``."""
    values = data.copy()
    comparisons = swaps = step = 0
    sorted_indices: set[int] = set()

    if not values:
        yield AlgorithmState(array=[])
        return

    def sift_down(root: int, heap_size: int) -> Iterator[AlgorithmState]:
        nonlocal comparisons, swaps, step
        while True:
            child = 2 * root + 1
            if child >= heap_size:
                return
            candidate = root
            for index in (child, child + 1):
                if index >= heap_size:
                    continue
                comparisons += 1
                step += 1
                yield AlgorithmState(
                    array=values.copy(),
                    comparing_indices=[candidate, index],
                    sorted_indices=sorted(sorted_indices),
                    comparisons=comparisons,
                    swaps=swaps,
                    step=step,
                )
                if values[index] > values[candidate]:
                    candidate = index
            if candidate == root:
                return
            values[root], values[candidate] = values[candidate], values[root]
            swaps += 1
            step += 1
            yield AlgorithmState(
                array=values.copy(),
                swapping_indices=[root, candidate],
                sorted_indices=sorted(sorted_indices),
                comparisons=comparisons,
                swaps=swaps,
                step=step,
            )
            root = candidate

    for root in range(len(values) // 2 - 1, -1, -1):
        yield from sift_down(root, len(values))

    for end in range(len(values) - 1, 0, -1):
        values[0], values[end] = values[end], values[0]
        swaps += 1
        sorted_indices.add(end)
        step += 1
        yield AlgorithmState(
            array=values.copy(),
            swapping_indices=[0, end],
            sorted_indices=sorted(sorted_indices),
            comparisons=comparisons,
            swaps=swaps,
            step=step,
        )
        yield from sift_down(0, end)

    sorted_indices.update(range(len(values)))
    yield AlgorithmState(
        array=values.copy(),
        sorted_indices=sorted(sorted_indices),
        comparisons=comparisons,
        swaps=swaps,
        step=step + 1,
    )
