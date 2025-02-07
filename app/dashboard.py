import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Flask API endpoints
FLASK_API = "http://localhost:5000"

# Layout of the Dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Fraud Detection Dashboard"), className="text-center mb-4")
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Total Transactions"),
            dbc.CardBody(id="total-transactions", children="Loading..."),
        ]), width=4),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Fraud Cases"),
            dbc.CardBody(id="fraud-cases", children="Loading..."),
        ]), width=4),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Fraud Percentage"),
            dbc.CardBody(id="fraud-percentage", children="Loading..."),
        ]), width=4)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="fraud-trends"), width=6),
        dbc.Col(dcc.Graph(id="fraud-by-location"), width=6),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="fraud-by-device-browser"), width=12)
    ]),
], fluid=True)


# Callbacks for Summary
@app.callback(
    [Output("total-transactions", "children"),
     Output("fraud-cases", "children"),
     Output("fraud-percentage", "children")],
    [Input("total-transactions", "id")]  # Dummy input for initialization
)
def update_summary(_):
    response = requests.get(f"{FLASK_API}/summary").json()
    return (
        f"{response['total_transactions']:,}",
        f"{response['fraud_cases']:,}",
        f"{response['fraud_percentage']:.2f}%"
    )


# Callback for Fraud Trends Line Chart
@app.callback(
    Output("fraud-trends", "figure"),
    [Input("fraud-trends", "id")]
)
def update_fraud_trends(_):
    data = requests.get(f"{FLASK_API}/fraud_trends").json()
    df = pd.DataFrame(data)
    fig = px.line(df, x='purchase_time', y='class', title="Fraud Cases Over Time")
    fig.update_layout(xaxis_title="Month", yaxis_title="Fraud Cases")
    return fig


# Callback for Fraud by Location Bar Chart
@app.callback(
    Output("fraud-by-location", "figure"),
    [Input("fraud-by-location", "id")]
)
def update_fraud_by_location(_):
    data = requests.get(f"{FLASK_API}/fraud_by_location").json()
    df = pd.DataFrame(data)
    fig = px.bar(df, x='country', y='class', title="Fraud Cases by Location")
    fig.update_layout(xaxis_title="Country", yaxis_title="Fraud Cases")
    return fig


# Callback for Fraud by Device and Browser Bar Chart
@app.callback(
    Output("fraud-by-device-browser", "figure"),
    [Input("fraud-by-device-browser", "id")]
)
def update_fraud_by_device_browser(_):
    data = requests.get(f"{FLASK_API}/fraud_by_device_browser").json()
    df = pd.DataFrame(data)
    fig = px.scatter(df, x='device_id', y='browser', size='class', color='browser',
                    title="Fraud Cases by Device and Browser")
    fig.update_layout(xaxis_title="Device", yaxis_title="Browser")
    return fig


if __name__ == "__main__":
    app.run_server(port=8050, debug=True)
