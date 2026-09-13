from collections.abc import Iterator

from .protocol import AlgorithmState


def selection_sort(data: list[int]) -> Iterator[AlgorithmState]:
    values = data.copy()
    comparisons = swaps = step = 0
    sorted_indices = set()

    if not values:
        yield AlgorithmState(array=[])
        return

    for i in range(len(values) - 1):
        min_index = i

        for j in range(i + 1, len(values)):
            comparisons += 1
            step += 1

            yield AlgorithmState(
                array=values.copy(),
                comparing_indices=[min_index, j],
                sorted_indices=sorted(sorted_indices),
                comparisons=comparisons,
                swaps=swaps,
                step=step,
            )

            if values[j] < values[min_index]:
                min_index = j

        if min_index != i:
            values[i], values[min_index] = values[min_index], values[i]
            swaps += 1
            step += 1

            yield AlgorithmState(
                array=values.copy(),
                swapping_indices=[i, min_index],
                sorted_indices=sorted(sorted_indices),
                comparisons=comparisons,
                swaps=swaps,
                step=step,
            )

        sorted_indices.add(i)

    sorted_indices.update(range(len(values)))
    step += 1

    yield AlgorithmState(
        array=values.copy(),
        sorted_indices=sorted(sorted_indices),
        comparisons=comparisons,
        swaps=swaps,
        step=step,
    )