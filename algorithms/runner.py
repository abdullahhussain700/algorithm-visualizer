"""Adapter between algorithm generators and Dash's serializable state."""

from collections.abc import Iterator

from .protocol import AlgorithmState, SortingAlgorithm


def materialize_frames(
    algorithm: SortingAlgorithm,
    data: list[int],
) -> list[dict]:
    """Convert yielded algorithm states into JSON-safe frames.

    Algorithms remain ordinary Python generators. Dash stores the resulting
    frames as JSON so callbacks do not need to keep a live generator object.
    """
    frames: Iterator[AlgorithmState] = algorithm(data.copy())
    serialized = []
    for frame in frames:
        if isinstance(frame, AlgorithmState):
            serialized.append(frame.as_dict())
        else:
            serialized.append(dict(frame))
    return serialized
