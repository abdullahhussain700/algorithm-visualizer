"""Generator-based Merge Sort implementation."""

from collections.abc import Iterator

from .protocol import AlgorithmState


def merge_sort(data: list[int]) -> Iterator[AlgorithmState]:
    """Yield visualization frames while sorting a copy of ``data``."""
    values = data.copy()
    comparisons = swaps = step = 0

    if not values:
        yield AlgorithmState(array=[])
        return

    def frames(left: int, right: int) -> Iterator[AlgorithmState]:
        nonlocal comparisons, swaps, step
        if right - left <= 1:
            return

        middle = (left + right) // 2
        yield from frames(left, middle)
        yield from frames(middle, right)

        merged = []
        first, second = left, middle
        while first < middle and second < right:
            comparisons += 1
            step += 1
            yield AlgorithmState(
                array=values.copy(),
                comparing_indices=[first, second],
                comparisons=comparisons,
                swaps=swaps,
                step=step,
            )
            if values[first] <= values[second]:
                merged.append(values[first])
                first += 1
            else:
                merged.append(values[second])
                second += 1

        merged.extend(values[first:middle])
        merged.extend(values[second:right])
        for offset, value in enumerate(merged):
            target = left + offset
            if values[target] != value:
                values[target] = value
                swaps += 1
                step += 1
                yield AlgorithmState(
                    array=values.copy(),
                    swapping_indices=[target],
                    comparisons=comparisons,
                    swaps=swaps,
                    step=step,
                )

    yield AlgorithmState(array=values.copy())
    yield from frames(0, len(values))
    yield AlgorithmState(
        array=values.copy(),
        sorted_indices=list(range(len(values))),
        comparisons=comparisons,
        swaps=swaps,
        step=step + 1,
    )
