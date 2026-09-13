"""Serializable application state used by Dash stores."""

from .array_data import generate_array


def create_visualization_state(
    size: int | float | None = 32,
    data_type: str | None = "random",
    algorithm: str | None = "bubble",
    speed: int | float | None = 5,
) -> dict:
    """Create a ready-to-render state with no algorithm execution."""
    array = generate_array(size, data_type)
    return {
        "array": array,
        "original_array": array.copy(),
        "algorithm": algorithm,
        "data_type": data_type or "random",
        "speed": max(1, min(10, int(speed or 5))),
        "frames": [],
        "frame_index": 0,
        "executions": 0,
        "step": 0,
        "status": "ready",
        "message": "Ready to visualize.",
        "comparisons": 0,
        "swaps": 0,
        "comparing_indices": [],
        "swapping_indices": [],
        "sorted_indices": [],
    }


def reset_visualization_state(state: dict | None) -> dict:
    """Return the current array to its original values and clear counters."""
    state = state or create_visualization_state()
    original = list(state.get("original_array") or [])
    if not original:
        return {
            **state,
            "array": [],
            "step": 0,
            "status": "ready",
            "message": "The array is empty. Generate values to begin.",
            "comparisons": 0,
            "swaps": 0,
            "comparing_indices": [],
            "swapping_indices": [],
            "sorted_indices": [],
            "frames": [],
            "frame_index": 0,
        }
    return {
        **state,
        "array": original,
        "step": 0,
        "status": "ready",
        "message": "Array reset. Ready to visualize.",
        "comparisons": 0,
        "swaps": 0,
        "comparing_indices": [],
        "swapping_indices": [],
        "sorted_indices": [],
        "frames": [],
        "frame_index": 0,
    }


def state_from_algorithm_frame(state: dict, frame: dict) -> dict:
    """Merge an algorithm frame into app state without adding UI concerns."""
    return {
        **state,
        **frame,
        "status": "running",
        "message": "Visualization running.",
    }
