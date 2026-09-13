"""Algorithm contracts and the registry of algorithms available to the UI."""

from .registry import ALGORITHMS, get_algorithm, get_algorithm_description, get_algorithm_spec
from .protocol import AlgorithmState, SortingAlgorithm
from .runner import materialize_frames

__all__ = [
    "ALGORITHMS",
    "AlgorithmState",
    "SortingAlgorithm",
    "get_algorithm",
    "get_algorithm_description",
    "get_algorithm_spec",
    "materialize_frames",
]
