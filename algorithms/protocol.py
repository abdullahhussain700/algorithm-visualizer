"""Interfaces that sorting implementations must follow.

Keep algorithm code in this package (or import it here) and keep it independent
from Dash. The UI consumes these state objects without knowing the algorithm.
"""

from dataclasses import asdict, dataclass, field
from typing import Iterator, Protocol


@dataclass(frozen=True)
class AlgorithmState:
    """One frame emitted by a sorting algorithm."""

    array: list[int]
    comparing_indices: list[int] = field(default_factory=list)
    swapping_indices: list[int] = field(default_factory=list)
    sorted_indices: list[int] = field(default_factory=list)
    comparisons: int = 0
    swaps: int = 0
    step: int = 0

    def as_dict(self) -> dict:
        """Return a JSON-serializable state for ``dcc.Store``."""
        return asdict(self)


class SortingAlgorithm(Protocol):
    """Callable contract for a generator-based sorting implementation.

    Implementations should copy the input before mutating it and yield an
    ``AlgorithmState`` after each meaningful visualization step.
    """

    def __call__(self, data: list[int]) -> Iterator[AlgorithmState]:
        ...
