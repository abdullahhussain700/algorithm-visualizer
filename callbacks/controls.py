"""Callbacks for array generation and playback controls."""

from dash import Input, Output, State

from algorithms import get_algorithm, materialize_frames
from utils.array_data import normalize_size
from utils.state import create_visualization_state, reset_visualization_state


def register_control_callbacks(app):
    @app.callback(
        Output("visualization-state", "data"),
        Output("visualization-tick", "disabled"),
        Output("visualization-tick", "interval"),
        Output("previous-button", "disabled"),
        Output("next-button", "disabled"),
        Input("generate-button", "n_clicks"),
        Input("reset-button", "n_clicks"),
        Input("algorithm-selector", "value"),
        Input("array-size", "value"),
        Input("data-type", "value"),
        Input("speed-slider", "value"),
        Input("previous-button", "n_clicks"),
        Input("next-button", "n_clicks"),
        Input("start-button", "n_clicks"),
        Input("pause-button", "n_clicks"),
        Input("visualization-tick", "n_intervals"),
        State("visualization-state", "data"),
        prevent_initial_call=True,
    )
    def update_state(
        generate_clicks,
        reset_clicks,
        algorithm,
        size,
        data_type,
        speed,
        previous_clicks,
        next_clicks,
        start_clicks,
        pause_clicks,
        tick_count,
        state,
    ):
        from dash import ctx

        state = state or create_visualization_state(algorithm=algorithm)
        action = ctx.triggered_id
        interval = _playback_interval(speed)
        if action == "previous-button":
            updated = _move_frame(state, -1)
            return updated, True, interval, _at_first_frame(updated), _at_last_frame(updated)
        if action == "next-button":
            updated = _move_frame(state, 1)
            return updated, True, interval, _at_first_frame(updated), _at_last_frame(updated)
        if action == "visualization-tick":
            updated = _move_frame(state, 1, "running")
            return updated, updated.get("status") == "completed", interval, _at_first_frame(updated), _at_last_frame(updated)
        if action == "speed-slider":
            updated = {**state, "speed": int(speed or 5)}
            return updated, updated.get("status") != "running", interval, _at_first_frame(updated), _at_last_frame(updated)
        if action == "reset-button":
            updated = reset_visualization_state(state)
            return updated, True, interval, True, True
        if action == "start-button":
            if state.get("status") == "running":
                return state, False, interval, _at_first_frame(state), _at_last_frame(state)
            if state.get("frames") and state.get("status") == "paused":
                updated = {**state, "status": "running", "message": "Visualization resumed."}
                return updated, False, interval, _at_first_frame(updated), _at_last_frame(updated)
            implementation = get_algorithm(algorithm)
            if implementation is None:
                updated = {**state, "algorithm": algorithm, "status": "unavailable", "message": "This algorithm hasn't been implemented yet."}
                return updated, True, interval, _at_first_frame(updated), _at_last_frame(updated)
            frames = materialize_frames(implementation, state.get("original_array", []))
            if not frames:
                updated = {**state, "algorithm": algorithm, "status": "unavailable", "message": "This algorithm did not provide any visualization states."}
                return updated, True, interval, _at_first_frame(updated), _at_last_frame(updated)
            updated = {**state, "algorithm": algorithm, "frames": frames, "frame_index": 0, "executions": state.get("executions", 0) + 1, "status": "running", "message": "Visualization running."}
            return updated, False, interval, True, len(frames) <= 1
        if action == "pause-button":
            if state.get("status") != "running":
                updated = {**state, "message": "Nothing is running to pause."}
                return updated, True, interval, _at_first_frame(updated), _at_last_frame(updated)
            updated = {**state, "status": "paused", "message": "Visualization paused."}
            return updated, True, interval, _at_first_frame(updated), _at_last_frame(updated)
        updated = create_visualization_state(normalize_size(size), data_type, algorithm, speed)
        return updated, True, interval, True, True

    @app.callback(
        Output("array-size-value", "children"),
        Output("speed-value", "children"),
        Input("array-size", "value"),
        Input("speed-slider", "value"),
    )
    def display_control_values(size, speed):
        return f"{normalize_size(size)} values", f"{int(speed or 5)}x"


def _playback_interval(speed):
    """Convert the UI speed value into a stable timer interval."""
    return max(180, 900 - (int(speed or 5) * 70))


def _move_frame(state, direction, active_status="paused"):
    """Move to a stored frame without keeping generator objects in Dash."""
    frames = state.get("frames") or []
    if not frames:
        return state
    current = int(state.get("frame_index", 0))
    target = max(0, min(len(frames) - 1, current + direction))
    frame = frames[target]
    completed = target == len(frames) - 1
    return {
        **state,
        **frame,
        "frame_index": target,
        "status": "completed" if completed else active_status,
        "message": "Visualization complete." if completed else "Visualization ready.",
    }


def _at_first_frame(state):
    return int(state.get("frame_index", 0)) <= 0


def _at_last_frame(state):
    frames = state.get("frames") or []
    return not frames or int(state.get("frame_index", 0)) >= len(frames) - 1
