from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("Trang_clean.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Variable", className="menu-title"),
                        dcc.Dropdown(
                            id="variable-filter",
                            options=[
                                {"label": col, "value": col}
                                for col in ["PM25", "PM10", "O3", "CO", "NO2", "SO2", "WS", "TEMP", "RH", "WD"]
                            ],
                            value="PM25",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                            display_format='YYYY-MM-DD'
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="variable-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("variable-chart", "figure"),
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("variable-filter", "value"),
    ],
)
def update_chart(start_date, end_date, variable):
    mask = (data['Date'] >= start_date) & (data['Date'] <= end_date)
    filtered_data = data.loc[mask, :]
    chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data[variable],
                "type": "lines",
                "hovertemplate": f"{variable}: %{{y}}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": f"{variable}",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "Date", "fixedrange": True},
            "yaxis": {"title": variable, "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)