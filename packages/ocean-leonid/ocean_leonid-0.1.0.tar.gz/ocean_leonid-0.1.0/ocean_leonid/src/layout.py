import plotly.graph_objs as go
from dash import dcc, html

from .apis import get_combine_data


def get_layout():
    df = get_combine_data()

    fig = go.Figure()

    uk_values = go.Scatter(
        x=df["date"],
        y=df["annualised_rate_uk"],
        name="UK CPIH",
        mode="lines",
    )
    fig.add_trace(uk_values)

    au_values = go.Scatter(
        x=df["date"],
        y=df["annualised_rate_au"],
        name="AU CPI",
        mode="lines",
    )
    fig.add_trace(au_values)

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="%",
        title="Inflation (CPI)",
        showlegend=True,
        legend={"title": "Variable"},
    )

    return html.Div(
        [
            dcc.Graph(id="inflation_graph", figure=fig),
        ],
    )
