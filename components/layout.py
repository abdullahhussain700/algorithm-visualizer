"""Page composition for the sorting visualizer."""

from dash import dcc, html

from algorithms import ALGORITHMS, get_algorithm_spec
from utils.array_data import DATA_TYPES, MAX_ARRAY_SIZE, MIN_ARRAY_SIZE
from utils.state import create_visualization_state
from utils.visualization import render_bars


def create_layout():
    """Build the static shell and the stores consumed by callbacks."""
    initial_state = create_visualization_state()
    initial_spec = get_algorithm_spec("bubble")
    return html.Div(
        className="app-shell",
        children=[
            dcc.Store(id="visualization-state", data=initial_state),
            dcc.Interval(id="visualization-tick", interval=200, n_intervals=0, disabled=True),
            html.Header(
                className="topbar",
                children=[
                    html.Div(
                        className="brand-lockup",
                        children=[
                            html.Div("SV", className="brand-mark"),
                            html.Div([
                                html.Div("SORTLAB", className="brand-name"),
                                html.Div("Sorting algorithm visualizer", className="brand-subtitle"),
                            ]),
                        ],
                    ),
                    html.Div([
                        html.Span(className="status-dot"),
                        html.Span("LEARN BY SORTING", className="topbar-label"),
                    ], className="topbar-status"),
                ],
            ),
            html.Main(
                className="page-shell",
                children=[
                    html.Div(
                        className="page-intro",
                        children=[
                            html.Div("SORTING ALGORITHM VISUALIZER", className="eyebrow"),
                            html.H1("SortLab"),
                            html.P("Compare algorithms one state at a time."),
                        ],
                    ),
                    html.Section(
                        className="control-panel panel",
                        children=[
                            html.Div([
                                html.Label("Algorithm", htmlFor="algorithm-selector"),
                                dcc.Dropdown(
                                    id="algorithm-selector",
                                    options=ALGORITHMS,
                                    value="bubble",
                                    clearable=False,
                                    searchable=False,
                                    className="control-dropdown",
                                ),
                            ], className="control-field algorithm-field"),
                            html.Div([
                                html.Label("Array size", htmlFor="array-size"),
                                dcc.Slider(
                                    id="array-size",
                                    min=MIN_ARRAY_SIZE,
                                    max=MAX_ARRAY_SIZE,
                                    step=1,
                                    value=32,
                                    marks=None,
                                    tooltip={"placement": "bottom", "always_visible": False},
                                    className="control-slider",
                                ),
                                html.Div([html.Span(str(MIN_ARRAY_SIZE)), html.Span(id="array-size-value", children="32 values"), html.Span(str(MAX_ARRAY_SIZE))], className="slider-meta"),
                            ], className="control-field size-field"),
                            html.Div([
                                html.Label("Input pattern", htmlFor="data-type"),
                                dcc.Dropdown(id="data-type", options=DATA_TYPES, value="random", clearable=False, searchable=False, className="control-dropdown"),
                            ], className="control-field pattern-field"),
                            html.Div([
                                html.Label("Playback speed", htmlFor="speed-slider"),
                                dcc.Slider(id="speed-slider", min=1, max=10, value=5, marks=None, tooltip={"placement": "bottom", "always_visible": False}, className="control-slider"),
                                html.Div([html.Span("SLOW"), html.Span(id="speed-value", children="5x"), html.Span("FAST")], className="speed-meta"),
                            ], className="control-field speed-field"),
                            html.Div([
                                html.Button("Generate", id="generate-button", className="button button-secondary", n_clicks=0),
                                html.Button("Previous", id="previous-button", className="button button-secondary", n_clicks=0, disabled=True),
                                html.Button("Next", id="next-button", className="button button-secondary", n_clicks=0, disabled=True),
                                html.Button("Start", id="start-button", className="button button-primary", n_clicks=0),
                                html.Button("Pause", id="pause-button", className="button button-secondary", n_clicks=0),
                                html.Button("Reset", id="reset-button", className="button button-quiet", n_clicks=0),
                            ], className="action-row"),
                        ],
                    ),
                    html.Section(
                        className="visualizer-panel panel",
                        children=[
                            html.Div([
                                html.Div([
                                    html.Div(id="algorithm-name", className="panel-title", children="Bubble Sort"),
                                    html.Div(id="algorithm-description", className="panel-description", children=initial_spec.description),
                                ]),
                                html.Div(id="status-label", className="status-badge status-ready", children="READY"),
                            ], className="panel-heading"),
                            html.Div(id="notification", className="notification", children="Ready to visualize."),
                            html.Div([
                                html.Div("LIVE ARRAY STATE", className="chart-caption"),
                                html.Div(className="bar-gridlines", children=[html.Span() for _ in range(4)]),
                                html.Div(id="bars-container", className="bars", children=render_bars(initial_state)),
                            ], className="chart-area"),
                            html.Div([
                                html.Span([html.I(className="legend-swatch swatch-unsorted"), "Unsorted"]),
                                html.Span([html.I(className="legend-swatch swatch-comparing"), "Comparing"]),
                                html.Span([html.I(className="legend-swatch swatch-swapping"), "Swapping"]),
                                html.Span([html.I(className="legend-swatch swatch-sorted"), "Sorted"]),
                            ], className="legend"),
                        ],
                    ),
                    html.Section(
                        className="learning-panel panel",
                        children=[
                            html.Div("ABOUT THIS ALGORITHM", className="section-kicker"),
                            html.Div(id="algorithm-how-it-works", className="how-it-works", children=initial_spec.how_it_works),
                            html.Div(
                                className="algorithm-facts",
                                children=[
                                    _fact_value("Stability", "algorithm-stability", "Stable"),
                                    _fact_value("Memory", "algorithm-memory", "In-place"),
                                ],
                            ),
                        ],
                    ),
                    html.Section(
                        className="stats-grid",
                        children=[
                            _stat_card("Comparisons", "comparisons-value", "0"),
                            _stat_card("Swaps", "swaps-value", "0"),
                            _stat_card("Steps", "step-value", "0"),
                            _stat_card("Array size", "array-size-stat", str(len(initial_state["array"]))),
                            _stat_card("Executions", "executions-value", "0"),
                        ],
                    ),
                    html.Section(
                        className="complexity-panel panel",
                        children=[
                            html.Div("THEORETICAL COMPLEXITY", className="complexity-heading"),
                            html.Div(id="complexity-name", className="complexity-name", children="Bubble Sort"),
                            html.Div(
                                className="complexity-grid",
                                children=[
                                    _complexity_value("Best", "complexity-best", "O(n)"),
                                    _complexity_value("Average", "complexity-average", "O(n^2)"),
                                    _complexity_value("Worst", "complexity-worst", "O(n^2)"),
                                    _complexity_value("Space", "complexity-space", "O(1)"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _stat_card(label: str, component_id: str, value: str):
    return html.Div([html.Div(label, className="stat-label"), html.Div(value, id=component_id, className="stat-value")], className="stat-card")


def _complexity_value(label: str, component_id: str, value: str):
    return html.Div([html.Div(label, className="complexity-label"), html.Div(value, id=component_id, className="complexity-value")], className="complexity-item")


def _fact_value(label: str, component_id: str, value: str):
    return html.Div([html.Div(label, className="fact-label"), html.Div(value, id=component_id, className="fact-value")], className="fact-item")
