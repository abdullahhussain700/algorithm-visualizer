"""Generator-based Insertion Sort implementation."""

from collections.abc import Iterator

from .protocol import AlgorithmState


def insertion_sort(data: list[int]) -> Iterator[AlgorithmState]:
    """Yield visualization frames while sorting a copy of ``data``."""
    values = data.copy()
    comparisons = swaps = step = 0
    sorted_indices: set[int] = set()

    if not values:
        yield AlgorithmState(array=[])
        return

    sorted_indices.add(0)
    yield AlgorithmState(array=values.copy(), sorted_indices=[0])

    for index in range(1, len(values)):
        current = values[index]
        position = index
        while position > 0:
            comparisons += 1
            step += 1
            yield AlgorithmState(
                array=values.copy(),
                comparing_indices=[position - 1, position],
                sorted_indices=sorted(sorted_indices),
                comparisons=comparisons,
                swaps=swaps,
                step=step,
            )
            if values[position - 1] <= current:
                break
            values[position] = values[position - 1]
            position -= 1
            swaps += 1
            step += 1
            yield AlgorithmState(
                array=values.copy(),
                swapping_indices=[position, position + 1],
                sorted_indices=sorted(sorted_indices),
                comparisons=comparisons,
                swaps=swaps,
                step=step,
            )

        values[position] = current
        sorted_indices = set(range(index + 1))
        step += 1
        yield AlgorithmState(
            array=values.copy(),
            sorted_indices=sorted(sorted_indices),
            comparisons=comparisons,
            swaps=swaps,
            step=step,
        )

    yield AlgorithmState(
        array=values.copy(),
        sorted_indices=list(range(len(values))),
        comparisons=comparisons,
        swaps=swaps,
        step=step + 1,
    )
