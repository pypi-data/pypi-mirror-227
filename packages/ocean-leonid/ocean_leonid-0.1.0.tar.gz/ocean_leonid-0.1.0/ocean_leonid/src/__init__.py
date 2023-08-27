from dash import Dash

from .layout import get_layout


def viz():
    app = Dash(__name__)
    app.layout = get_layout()
    return app
