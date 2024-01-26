import streamlit as st
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
import multiprocessing

# Read in the data
data = pd.read_csv("precious_metals_prices_2018_2021.csv")
data['DateTime'] = pd.to_datetime(data['DateTime'], format="%Y-%m-%d %H:%M:%S", errors='coerce')

# Create a plotly plot for use by dcc.Graph().
fig = px.line(
    data,
    title="Precious Metal Prices 2018-2021",
    x="DateTime",
    y=["Gold"],
    color_discrete_map={"Gold": "gold"}
)

# Define a Dash app
dash_app = dash.Dash(__name__)
dash_app.title = "Precious Metal Prices 2018-2021"
dash_app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="header-area",
            children=[
                html.H1(
                    id="header-title",
                    children="Precious Metal Prices",
                ),
                html.P(
                    id="header-description",
                    children=("The cost of precious metals", html.Br(), "between 2018 and 2021"),
                ),
            ],
        ),
        html.Div(
            id="menu-area",
            children=[
                html.Div(
                    children=[
                        html.Div(
                            className="menu-title",
                            children="Metal"
                        ),
                        dcc.Dropdown(
                            id="metal-filter",
                            className="dropdown",
                            options=[{"label": metal, "value": metal} for metal in data.columns[1:]],
                            clearable=False,
                            value="Gold"
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            className="menu-title",
                            children="Date Range"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.DateTime.min().date(),
                            max_date_allowed=data.DateTime.max().date(),
                            start_date=data.DateTime.min().date(),
                            end_date=data.DateTime.max().date()
                        )
                    ]
                )
            ]
        ),
        html.Div(
            id="graph-container",
            children=dcc.Graph(
                id="price-chart",
                figure=fig,
                config={"displayModeBar": False}
            ),
        ),
    ]
)

@dash_app.callback(
    Output("price-chart", "figure"),
    Input("metal-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)
def update_chart(metal, start_date, end_date):
    filtered_data = data.loc[(data.DateTime >= start_date) & (data.DateTime <= end_date)]
    # Create a plotly plot for use by dcc.Graph().
    updated_fig = px.line(
        filtered_data,
        title="Precious Metal Prices 2018-2021",
        x="DateTime",
        y=[metal],
        color_discrete_map={"Gold": "gold"}
    )
    return updated_fig

# Function to run Dash app
def run_dash():
    dash_app.run_server(debug=True, use_reloader=False)

# Run Streamlit app
st.title("Streamlit App")
st.write("This is a Streamlit app.")

# Run Dash app in a separate process
if __name__ == '__main__':
    dash_process = multiprocessing.Process(target=run_dash)
    dash_process.start()
    st.write("Dash app is running in a separate process.")

