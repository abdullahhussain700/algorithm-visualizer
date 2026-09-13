from dash import Dash

from components import create_layout
from callbacks import register_callbacks


def create_app() -> Dash:
    """Create the application, layout, and modular callbacks."""
    app = Dash(__name__, title="SortLab")
    app.layout = create_layout()
    register_callbacks(app)
    return app
