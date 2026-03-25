from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# GA4 SETUP
PROPERTY_ID = "{YOUR_PROPERTY_ID}"

client = BetaAnalyticsDataClient.from_service_account_json("credentials.json")

# FUNCTION TO FETCH DATA
def fetch_data(days):
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[DateRange(start_date=days, end_date="yesterday")],
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="activeUsers")]
    )

    response = client.run_report(request)

    data = []
    for row in response.rows:
        data.append({
            "date": row.dimension_values[0].value,
            "activeUsers": int(row.metric_values[0].value)
        })

    return pd.DataFrame(data)

# DASH APP
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Google Analytics Dashboard"),

    dcc.Dropdown(
        id='date-range',
        options=[
            {'label': 'Last 7 Days', 'value': '7daysAgo'},
            {'label': 'Last 30 Days', 'value': '30daysAgo'}
        ],
        value='7daysAgo',
        style={'width': '50%'}
    ),

    dcc.Graph(id='graph')
])

@app.callback(
    Output('graph', 'figure'),
    Input('date-range', 'value')
)
def update_graph(date_range):
    df = fetch_data(date_range)

    fig = px.line(df, x='date', y='activeUsers',
                  title=f"Active Users ({date_range})")

    return fig

# RUN APP
if __name__ == '__main__':
    app.run(debug=True)
