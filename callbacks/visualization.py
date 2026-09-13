"""Callbacks that render state and algorithm metadata."""

from dash import Input, Output

from algorithms import get_algorithm_spec
from utils.visualization import render_bars


def register_visualization_callbacks(app):
    @app.callback(
        Output("bars-container", "children"),
        Output("comparisons-value", "children"),
        Output("swaps-value", "children"),
        Output("step-value", "children"),
        Output("array-size-stat", "children"),
        Output("executions-value", "children"),
        Output("status-label", "children"),
        Output("status-label", "className"),
        Output("notification", "children"),
        Input("visualization-state", "data"),
    )
    def render_visualization(state):
        state = state or {}
        status = state.get("status", "ready")
        status_label = {"ready": "READY", "running": "RUNNING", "paused": "PAUSED", "completed": "DONE", "unavailable": "UNAVAILABLE"}.get(status, "READY")
        status_class = f"status-badge status-{status}"
        return (
            render_bars(state),
            str(state.get("comparisons", 0)),
            str(state.get("swaps", 0)),
            str(state.get("step", 0)),
            str(len(state.get("array") or [])),
            str(state.get("executions", 0)),
            status_label,
            status_class,
            state.get("message", "Ready to visualize."),
        )

    @app.callback(
        Output("algorithm-name", "children"),
        Output("algorithm-description", "children"),
        Output("complexity-name", "children"),
        Output("complexity-best", "children"),
        Output("complexity-average", "children"),
        Output("complexity-worst", "children"),
        Output("complexity-space", "children"),
        Output("algorithm-stability", "children"),
        Output("algorithm-memory", "children"),
        Output("algorithm-how-it-works", "children"),
        Input("algorithm-selector", "value"),
    )
    def update_algorithm_metadata(algorithm):
        spec = get_algorithm_spec(algorithm)
        if spec is None:
            return "Choose an algorithm", "Select an algorithm to view its details.", "No algorithm selected", "-", "-", "-", "-", "-", "-", "Select an algorithm to view how it works."
        return (
            spec.label,
            spec.description,
            spec.label,
            spec.best_time,
            spec.average_time,
            spec.worst_time,
            spec.space,
            "Stable" if spec.stable else "Unstable",
            "In-place" if spec.in_place else "Not in-place",
            spec.how_it_works,
        )
