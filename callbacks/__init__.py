"""Dash callback registration."""

from .controls import register_control_callbacks
from .visualization import register_visualization_callbacks


def register_callbacks(app):
    """Register each callback group with the Dash app."""
    register_control_callbacks(app)
    register_visualization_callbacks(app)
