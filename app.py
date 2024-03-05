from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("Trang_clean.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)
data["Datetime"] = pd.to_datetime(data["Date"].astype(str) + " " + data["Time"].astype(str))

data2 = pd.read_csv("mean_value.csv")
data2["Date"] = pd.to_datetime(data2["Date"], format="%Y-%m-%d")
data2.sort_values("Date", inplace=True)

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

template = html.Div(
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
    ]
)

layout_home = html.Div(
    children=[
        template,
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
                html.Div(
                    children=dcc.Graph(
                        id="mean-chart", config={"displayModeBar": False},
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
    Output("mean-chart", "figure"),
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("variable-filter", "value"),
    ],
)
def update_chart(start_date, end_date, variable):
    mask = (data['Date'] >= start_date) & (data['Date'] <= end_date)
    filtered_data = data.loc[mask, :]
    normal_chart_figure = {
        "data": [
            {
                "x": filtered_data["Datetime"],
                "y": filtered_data[variable],
                "mode": "markers",
                "type": "scatter",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": f"{variable}",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "Datetime", "fixedrange": True},
            "yaxis": {"title": variable, "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    mask2 = (data2['Date'] >= start_date) & (data2['Date'] <= end_date)
    filtered_data2 = data2.loc[mask2, :]
    mean_chart_figure = {
        "data": [
            {
                "x": filtered_data2["Date"],
                "y": filtered_data2[variable],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
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
    return normal_chart_figure, mean_chart_figure

layout_page2 = html.Div(
    children=[
        template,
        dcc.Markdown('# This will be the content of Page 2')
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)