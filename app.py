import streamlit as st
import plotly.express as px
import pandas as pd
from dash import html, dcc, Dash
from dash.dependencies import Input, Output

# Read in the data
data = pd.read_csv("precious_metals_prices_2018_2021.csv")
data['DateTime'] = pd.to_datetime(data['DateTime'], format="%Y-%m-%d %H:%M:%S", errors='coerce')

# Create a Dash app
app = Dash(__name__)

# Dash layout
app.layout = html.Div([
    html.H1("Precious Metal Prices"),
    html.P("The cost of precious metals between 2018 and 2021"),

    html.Div([
        html.Div([
            html.Div("Metal", className="menu-title"),
            dcc.Dropdown(
                id="metal-filter",
                options=[{"label": metal, "value": metal} for metal in data.columns[1:]],
                clearable=False,
                value="Gold"
            )
        ], className="menu-area"),

        html.Div([
            html.Div("Date Range", className="menu-title"),
            dcc.DatePickerRange(
                id="date-range",
                min_date_allowed=data.DateTime.min().date(),
                max_date_allowed=data.DateTime.max().date(),
                start_date=data.DateTime.min().date(),
                end_date=data.DateTime.max().date()
            )
        ], className="menu-area")
    ], id="menu-area"),

    dcc.Graph(id="price-chart"),
])

# Dash callback
@app.callback(
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

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Price (USD/oz)",
        font=dict(
            family="Verdana, sans-serif",
            size=18,
            color="white"
        ),
    )

    return fig

# Streamlit app layout
st.title("Streamlit + Dash: Precious Metal Prices")
st.write("This app combines Streamlit for deployment with Dash for interactive plots.")

# Dash app within Streamlit using an iframe
st.components.v1.html(f'<iframe src="{app.run_server(debug=False)}" width="1000" height="600"></iframe>', height=600)

# Streamlit run
if __name__ == '__main__':
    st.run_server(port=8001)  # Specify a different port for Streamlit to avoid conflicts
