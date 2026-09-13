"""Generator-based Bubble Sort implementation for the visualizer."""

from collections.abc import Iterator

from .protocol import AlgorithmState


def bubble_sort(data: list[int]) -> Iterator[AlgorithmState]:
    """Yield visualization frames while sorting a copy of ``data``."""
    values = data.copy()
    comparisons = 0
    swaps = 0
    step = 0
    sorted_indices: set[int] = set()

    if not values:
        yield AlgorithmState(array=values)
        return

    yield AlgorithmState(array=values.copy(), step=step)

    for end in range(len(values) - 1, 0, -1):
        swapped = False
        for index in range(end):
            comparisons += 1
            step += 1
            yield AlgorithmState(
                array=values.copy(),
                comparing_indices=[index, index + 1],
                sorted_indices=sorted(sorted_indices),
                comparisons=comparisons,
                swaps=swaps,
                step=step,
            )

            if values[index] > values[index + 1]:
                values[index], values[index + 1] = values[index + 1], values[index]
                swaps += 1
                step += 1
                swapped = True
                yield AlgorithmState(
                    array=values.copy(),
                    swapping_indices=[index, index + 1],
                    sorted_indices=sorted(sorted_indices),
                    comparisons=comparisons,
                    swaps=swaps,
                    step=step,
                )

        sorted_indices.add(end)
        step += 1
        yield AlgorithmState(
            array=values.copy(),
            sorted_indices=sorted(sorted_indices),
            comparisons=comparisons,
            swaps=swaps,
            step=step,
        )
        if not swapped:
            sorted_indices.update(range(end))
            break

    sorted_indices.update(range(len(values)))
    step += 1
    yield AlgorithmState(
        array=values.copy(),
        sorted_indices=sorted(sorted_indices),
        comparisons=comparisons,
        swaps=swaps,
        step=step,
    )
