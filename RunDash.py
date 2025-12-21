import time, random, warnings
warnings.filterwarnings("ignore")
import numpy as np
from datetime import datetime
import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import os

app = Dash(__name__)
server = app.server  # Heroku needs this

PRESET = ["Hebbal", "Whitefield", "Yelahanka"]
history = {j: [] for j in PRESET}

def get_traffic(j):
    base = random.randint(20, 60)
    peak = random.randint(20, 40) if datetime.now().hour in [8,9,17,18] else 0
    return min(base + peak, 100)

def update_data():
    for j in PRESET:
        v = get_traffic(j)
        history[j].append(v)
        if len(history[j]) > 50:
            history[j] = history[j][-50:]

app.layout = html.Div([
    html.H1("🚦 Live Traffic Dashboard"),
    dcc.Dropdown(id="junctions", options=[{"label": j, "value": j} for j in PRESET], value=PRESET[0]),
    dcc.Graph(id="graph"),
    dcc.Interval(id="interval", interval=3000, n_intervals=0)
])

@app.callback(Output("graph", "figure"), [Input("junctions", "value"), Input("interval", "n_intervals")])
def update_graph(selected, n):
    update_data()
    fig = go.Figure()
    for j in [selected] if isinstance(selected, str) else selected:
        fig.add_trace(go.Scatter(y=history[j][-20:], name=j, line=dict(width=3)))
    fig.update_layout(template="plotly_dark", title="Live Traffic")
    return fig

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8055, debug=False)
