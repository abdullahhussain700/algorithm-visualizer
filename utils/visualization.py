"""Pure helpers for turning visualization state into Dash components."""

from dash import html


def render_bars(state: dict | None) -> list:
    """Render bars from state; this function contains no sorting behavior."""
    state = state or {}
    values = state.get("array") or []
    if not values:
        return [html.Div("Generate an array to begin", className="visualization-empty")]

    maximum = max(values, default=1)
    comparing = set(state.get("comparing_indices") or [])
    swapping = set(state.get("swapping_indices") or [])
    sorted_indices = set(state.get("sorted_indices") or [])

    bars = []
    for index, value in enumerate(values):
        if index in swapping:
            visual_class = "bar bar-swapping"
        elif index in comparing:
            visual_class = "bar bar-comparing"
        elif index in sorted_indices:
            visual_class = "bar bar-sorted"
        else:
            visual_class = "bar bar-unsorted"
        bars.append(
            html.Div(
                className=visual_class,
                style={"height": f"{max(6, (value / maximum) * 100):.2f}%"},
                title=f"Index {index}: {value}",
            )
        )
    return bars
