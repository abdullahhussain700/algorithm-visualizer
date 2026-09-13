# SortLab

SortLab is a Dash workbench for visualizing sorting algorithms. The project
currently provides the application shell, state model, rendering pipeline, and
algorithm interface. Sorting implementations are intentionally left for you.

## Run

```bash
pip install -r requirements.txt
python main.py
```

Open `http://localhost:8050`.

Run `main.py` from the project root. Do not run files inside `components/`,
`callbacks/`, or `algorithms/` directly; they are package modules and expect
the project root to be on Python's import path.

## Architecture

```text
UI components
    -> Dash callbacks
        -> serializable visualization state
            -> algorithm generator frames
                -> bar renderer
```

```text
algorithms/
  bubble.py         Bubble Sort generator
  selection_sort.py Selection Sort generator
  insertion_sort.py Insertion Sort generator
  merge_sort.py     Merge Sort generator
  quick_sort.py     Quick Sort generator
  heap_sort.py      Heap Sort generator
  protocol.py       AlgorithmState and SortingAlgorithm contract
  registry.py       UI metadata and implementation registration points
components/
  layout.py         Page layout and reusable display sections
callbacks/
  controls.py       Array and playback state transitions
  visualization.py  State rendering and algorithm metadata
algorithms/
  runner.py         Generator frames to JSON-safe playback frames
utils/
  array_data.py     Input generation and validation
  state.py          dcc.Store state factories and reset helpers
  visualization.py  Pure state-to-bars renderer
assets/
  styles.css        Application styling
```

`app.py` is only the application factory. `main.py` is the development entry
point. There is no global mutable sorting state; the current state lives in the
`visualization-state` `dcc.Store`.

## Implement an algorithm

Add your implementation in `algorithms/` and make it satisfy the generator
contract:

```python
from collections.abc import Iterator

from .protocol import AlgorithmState


def your_algorithm(data: list[int]) -> Iterator[AlgorithmState]:
    values = data.copy()
    # Implement the algorithm here.
    # Yield an AlgorithmState after each visualization step.
    yield AlgorithmState(array=values)
```

Each frame may provide `array`, `comparing_indices`, `swapping_indices`,
`sorted_indices`, `comparisons`, `swaps`, and `step`.

Then set the matching `implementation` field in `algorithms/registry.py`:

```python
AlgorithmSpec("your-key", "Your Algorithm", "Description", your_algorithm)
```

The callback and renderer consume yielded states without requiring UI code
inside the algorithm.

## Current behavior

All six algorithm names are registered and can be started from the UI. Each
implementation yields `AlgorithmState` frames, so the same playback controls,
statistics, and bar renderer work for every algorithm.

Generate, reset, pause, resume, speed, array-size, and input-pattern controls
are wired to the state model. Once an algorithm is registered, Start
materializes its frames, `dcc.Interval` advances them, and the renderer marks
the visualization complete at the final frame.
