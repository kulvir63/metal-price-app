import streamlit as st
from streamlit_dashboards import st_decks
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Read in the data
data = pd.read_csv("precious_metals_prices_2018_2021.csv")
data['DateTime'] = pd.to_datetime(data['DateTime'], format="%Y-%m-%d %H:%M:%S", errors='coerce')

# Dash app
dash_app = dash.Dash(__name__)
dash_app.title = "Precious Metal Prices 2018-2021"

# Dash layout
dash_app.layout = html.Div(
    children=[
        html.H1("Precious Metal Prices"),
        dcc.Graph(id="price-chart"),
    ]
)

# Dash callback
@dash_app.callback(
    Output("price-chart", "figure"),
    [Input("metal-filter", "value"),
     Input("date-range", "start_date"),
     Input("date-range", "end_date")]
)
def update_chart(metal, start_date, end_date):
    filtered_data = data.loc[(data.DateTime >= start_date) & (data.DateTime <= end_date)]
    fig = px.line(
        filtered_data,
        title="Precious Metal Prices 2018-2021",
        x="DateTime",
        y=[metal],
        color_discrete_map={
            "Platinum": "#E5E4E2",
            "Gold": "gold",
            "Silver": "silver",
            "Palladium": "#CED0DD",
            "Rhodium": "#E2E7E1",
            "Iridium": "#3D3C3A",
            "Ruthenium": "#C9CBC8"
        }
    )
    return fig

# Streamlit app
st.title("Streamlit Dash App")

# Embed the Dash app in Streamlit
st_decks([dash_app])

if __name__ == '__main__':
    st.run(dash_app)
