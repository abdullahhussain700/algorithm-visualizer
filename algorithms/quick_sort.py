"""Generator-based Quick Sort implementation."""

from collections.abc import Iterator

from .protocol import AlgorithmState


def quick_sort(data: list[int]) -> Iterator[AlgorithmState]:
    """Yield visualization frames while sorting a copy of ``data``."""
    values = data.copy()
    comparisons = swaps = step = 0
    sorted_indices: set[int] = set()

    if not values:
        yield AlgorithmState(array=[])
        return

    def partition(low: int, high: int) -> Iterator[AlgorithmState]:
        nonlocal comparisons, swaps, step
        pivot = values[high]
        boundary = low
        for index in range(low, high):
            comparisons += 1
            step += 1
            yield AlgorithmState(
                array=values.copy(),
                comparing_indices=[index, high],
                sorted_indices=sorted(sorted_indices),
                comparisons=comparisons,
                swaps=swaps,
                step=step,
            )
            if values[index] <= pivot:
                if boundary != index:
                    values[boundary], values[index] = values[index], values[boundary]
                    swaps += 1
                    step += 1
                    yield AlgorithmState(
                        array=values.copy(),
                        swapping_indices=[boundary, index],
                        sorted_indices=sorted(sorted_indices),
                        comparisons=comparisons,
                        swaps=swaps,
                        step=step,
                    )
                boundary += 1

        if boundary != high:
            values[boundary], values[high] = values[high], values[boundary]
            swaps += 1
            step += 1
            yield AlgorithmState(
                array=values.copy(),
                swapping_indices=[boundary, high],
                sorted_indices=sorted(sorted_indices),
                comparisons=comparisons,
                swaps=swaps,
                step=step,
            )
        sorted_indices.add(boundary)
        return boundary

    def sort(low: int, high: int) -> Iterator[AlgorithmState]:
        if low > high:
            return
        if low == high:
            sorted_indices.add(low)
            return
        pivot_index = yield from partition(low, high)
        yield from sort(low, pivot_index - 1)
        yield from sort(pivot_index + 1, high)

    yield AlgorithmState(array=values.copy())
    yield from sort(0, len(values) - 1)
    yield AlgorithmState(
        array=values.copy(),
        sorted_indices=list(range(len(values))),
        comparisons=comparisons,
        swaps=swaps,
        step=step + 1,
    )
