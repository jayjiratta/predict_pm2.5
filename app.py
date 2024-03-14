from dash import Dash 
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
from pycaret.regression import predict_model, load_model

data = pd.read_csv("./datafile/Trang_clean.csv")
data["DATETIMEDATA"] = pd.to_datetime(data["DATETIMEDATA"], format="%Y-%m-%d %H:%M:%S")
data.sort_values("DATETIMEDATA", inplace=True)

data2 = pd.read_csv("./datafile/mean_value.csv")
data2["Date"] = pd.to_datetime(data2["Date"], format="%Y-%m-%d")
data2.sort_values("Date", inplace=True)

PAGE_SIZE = 10

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
app.title = "Air Quality Metrics"

navbar = html.Div(
    className="navbar", 
    children=[
        html.Nav(
            className="nav",
            children=[
                html.A('🤌Analysis🤌', href='/'),
                html.A('👓Prediction👓', href='/page-2'),
                html.A('🪑Table🪑', href='/page-3')
            ]
        )
    ]
)

template_1 = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🌪️", className="header-emoji"),
                html.H1(
                    children="Air Quality Metrics", className="header-title"
                ),
                html.H2(
                    children="Analysis", className="header-second"
                ),
                html.P(
                    children=
"Exploring the Impact of Environmental Factors on Air Quality",
                    className="header-description",
                ),
            ],
            className="header-one",
        ),
    ]
)

template_2 = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🌪️", className="header-emoji"),
                html.H1(
                    children="Air Quality Metrics", className="header-title"
                ),
                html.H2(
                    children="Prediction ", className="header-second"
                ),
                html.P(
                    children=
"Exploring the Impact of Environmental Factors on Air Quality",
                    className="header-description",
                ),
            ],
            className="header-two",
        ),
    ]
)

template_3 = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🌪️", className="header-emoji"),
                html.H1(
                    children="Air Quality Metrics", className="header-title"
                ),
                html.H2(
                    children="Table", className="header-second"
                ),
                html.P(
                    children=
"Exploring the Impact of Environmental Factors on Air Quality",
                    className="header-description",
                ),
            ],
            className="header-two",
        ),
    ]
)

layout_home = html.Div(
    children=[
        navbar,
        template_1,
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
                            min_date_allowed=data["DATETIMEDATA"].min().date(),
                            max_date_allowed=data["DATETIMEDATA"].max().date(),
                            start_date=data["DATETIMEDATA"].min().date(),
                            end_date=data["DATETIMEDATA"].max().date(),
                            display_format='YYYY-MM-DD',
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
    mask = (data["DATETIMEDATA"] >= start_date) & (data["DATETIMEDATA"] <= end_date)
    filtered_data = data.loc[mask, :]
    normal_chart_figure = {
        "data": [
            {
                "x": filtered_data["DATETIMEDATA"],
                "y": filtered_data[variable],
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
            "xaxis": {"title": "Datetime", "fixedrange": True},
            "yaxis": {"title": variable, "fixedrange": True},
            "colorway": ["#b8c9b4"],
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
                "text": f"{variable} mean",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "Date", "fixedrange": True},
            "yaxis": {"title": variable, "fixedrange": True},
            "colorway": ['#b8c9b4'],
        },
    }
    return normal_chart_figure, mean_chart_figure

layout_page2 = html.Div(
    children=[
        navbar,
        template_2,
            html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="PM25-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="PM10-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        
    ]
)

@app.callback(
    Output("PM25-chart", "figure"),
    Output("PM10-chart", "figure"),
    [
        Input('interval-component', 'n_intervals')
    ]
)
def update_chart_prediction(n_intervals):
    train = pd.read_csv('./datafile/train.csv')
    train['DATETIMEDATA'] = pd.to_datetime(train['DATETIMEDATA'])

    loaded_model_PM25 = load_model('PM25_pipeline')
    loaded_model_PM10 = load_model('PM10_pipeline')

    now = pd.Timestamp.now()
    start_date = now.date()
    end_date = start_date + pd.DateOffset(days=7)

    future_dates_PM25 = pd.date_range(start=start_date, end=end_date, freq='D')
    future_data_PM25 = pd.DataFrame({'DATETIMEDATA': future_dates_PM25})
    future_data_PM25['PM10'] = data['PM10'].mean().round(2)
    future_data_PM25['O3'] = data['O3'].mean().round(2)
    future_data_PM25['CO'] = data['CO'].mean().round(2)
    future_data_PM25['NO2'] = data['NO2'].mean().round(2)
    future_data_PM25['WS'] = data['WS'].mean().round(2)

    predictions_PM25 = predict_model(loaded_model_PM25, data=future_data_PM25)
    predictions_PM25 = predictions_PM25.rename(columns={'Label': 'prediction_label'})
    predictions_PM25['prediction_label'] = predictions_PM25['prediction_label'].round(2)

    future_dates_PM10 = pd.date_range(start=start_date, end=end_date, freq='D')
    future_data_PM10 = pd.DataFrame({'DATETIMEDATA': future_dates_PM10})
    future_data_PM10['PM25'] = data['PM25'].mean().round(2)
    future_data_PM10['O3'] = data['O3'].mean().round(2)
    future_data_PM10['CO'] = data['CO'].mean().round(2)
    future_data_PM10['NO2'] = data['NO2'].mean().round(2)
    future_data_PM10['WS'] = data['WS'].mean().round(2)

    predictions_PM10 = predict_model(loaded_model_PM10, data=future_data_PM10)
    predictions_PM10 = predictions_PM10.rename(columns={'Label': 'prediction_label'})
    predictions_PM10['prediction_label'] = predictions_PM10['prediction_label'].round(2)

    merged_table_PM10_PM25_prediction = pd.merge(predictions_PM10, predictions_PM25, on='DATETIMEDATA', how='outer')
    merged_table_PM10_PM25_prediction.to_csv('./datafile/merged_table_PM10_PM25_prediction.csv', index=False)


    PM25_chart_figure = {
        "data": [
            {
                "x": future_dates_PM25,
                "y": predictions_PM25['prediction_label'].round(2),
                "type": "lines",
                'name': 'PM25 Forecast',
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        'layout': {
            'title': { 
                'text' : f'PM25 Forecast for Next 7 Days',
                "x": 0.05,
                "xanchor": "left",
            },
            'xaxis': {'title': 'Date', "fixedrange": True},
            'yaxis': {'title': 'PM25 Forecast', "fixedrange": True},
            "colorway": ["#B5C0D0"],
        },
    }

    PM10_chart_figure = {
        "data": [
            {
                "x": future_dates_PM10,
                "y": predictions_PM10['prediction_label'].round(2),
                "type": "lines",
                'name': 'PM10 Forecast',
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        'layout': {
            'title': { 
                'text' : f'PM10 Forecast for Next 7 Days',
                "x": 0.05,
                "xanchor": "left",
            },
            'xaxis': {'title': 'Date', "fixedrange": True},
            'yaxis': {'title': 'PM10 Forecast', "fixedrange": True},
            "colorway": ["#ccc1b7"],
        },
    }

    return PM25_chart_figure , PM10_chart_figure 

table_predict = pd.read_csv('./datafile/merged_table_PM10_PM25_prediction.csv')
# table_predict = table_predict.drop(columns='Unnamed: 0')
table_predict.rename(columns={'DATETIMEDATA': 'Date'}, inplace=True)

table_analysis = pd.read_csv('./datafile/Trang_date_time.csv')
table_analysis = table_analysis.drop(columns='Unnamed: 0')
desired_order = ['Date','Time', "PM25", "PM10", "O3", "CO", "NO2", "SO2", "WS", "TEMP", "RH", "WD"]
table_analysis = table_analysis[desired_order]

layout_page3 = html.Div(
    children=[
        navbar,
        template_3,
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H3(children="Data Analysis", className="header-table colored-background"),
                        dash_table.DataTable(
                            id="analysis", 
                            columns=[{"name": i, "id": i} for i in desired_order],
                            page_current=0,
                            page_size=PAGE_SIZE,
                            page_action="custom",
                            style_cell={"textAlign": "center"},
                            style_header={"backgroundColor": " rgb(174, 180, 196)"},
                            style_cell_conditional=[
                                {"if": {"column_id": c}, "textAlign": "center"}
                                for c in ["Date", "Region"]
                            ],
                            style_as_list_view=True,
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    children=[
                        html.H3(children="7-Day Data Prediction", className="header-table colored-background"),
                        dash_table.DataTable(
                            id="prediction", 
                            columns=[{"name": i, "id": i} for i in ["Date", "PM25", "PM10"]],
                            style_cell={"textAlign": "center"},
                            style_header={"backgroundColor": " rgb(174, 180, 196)"},
                            style_cell_conditional=[
                                {"if": {"column_id": c}, "textAlign": "center"}
                                for c in ["Date", "Region"]
                            ],
                            style_as_list_view=True,
                        ),
                    ],
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    Output("analysis", "data"),
    Output("prediction", "data"),
    [
        Input('analysis', "page_current"),
        Input('analysis', "page_size"),
    ]
)
def update_table(analysis_page_current, analysis_page_size):
    analysis_data = (table_analysis[desired_order]
                     .iloc[analysis_page_current * analysis_page_size: 
                           (analysis_page_current + 1) * analysis_page_size]
                            .to_dict('records'))
    
    prediction_data = table_predict.to_dict('records')
    return analysis_data, prediction_data

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Interval(id='interval-component',interval=60000)
    ]
)

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return layout_home
    elif pathname == '/page-2':
        return layout_page2
    elif pathname == '/page-3':
        return layout_page3
    else:
        return '404 Page Not Found'

if __name__ == "__main__":
    app.run_server(debug=True)