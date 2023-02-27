from dash import Dash, html, dcc
import plotly
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import time

app = Dash(__name__)

data = {
    "ch1": [],
    "ch2": [],
    "ch3": [],
    "time": [],
    "preprocessed": [],
}
d_len = 0
is_match = False


def make_raw():
    fig = plotly.subplots.make_subplots(
        rows=1, cols=3, horizontal_spacing=0.05)
    fig.update_layout(
        margin=dict(l=0, r=0, t=25, b=25),
        dragmode=False,
        showlegend=False
    )

    titles = ["Brain Channel", "Reference Channel", "Ground Channel"]

    for i, channel in enumerate(['ch1', 'ch2', 'ch3']):
        c = i+1
        fig.append_trace({
            "x": data['time'],
            "y": data[channel],
            "name": titles[i],
            "mode": "lines",
            "type": "scatter"
        }, row=1, col=c)
        fig.update_xaxes(
            title_text=titles[i] + " (time, s)", row=1, col=c)
        if i == 0:
            fig.update_yaxes(title_text="Voltage",
                             autorange=True, row=1, col=c)
        else:
            fig.update_yaxes(showticklabels=False,
                             autorange=True, row=1, col=c)
    return fig


def make_preproc():
    preprocessed_graph = plotly.subplots.make_subplots(rows=1, cols=1)
    preprocessed_graph.update_layout(
        margin=dict(l=10, r=10, t=0, b=0),
        dragmode=False
    )
    preprocessed_graph.add_trace(
        {"x": data['time'], "y": data['preprocessed'], "mode": "lines", "type": "scatter"}, row=1, col=1)
    preprocessed_graph.update_xaxes(title_text="Time (s)")
    preprocessed_graph.update_yaxes(title_text="Voltage", autorange=True)
    return preprocessed_graph


REFRESH_RATE = 1.2  # s
FS = 75

app.layout = html.Div(children=[
    html.H1(children="Detecting Blinks using a Brain-Computer Interface"),
    html.H2(children="Realtime Raw Data"),
    dcc.Graph(id="channelgraphs", animate=True, figure=make_raw(), className="channelgraph", config={
        'displayModeBar': False
    }),
    html.H2(children="Preprocessed Data"),
    dcc.Graph(id="preprocessed", animate=True,
              config={"displayModeBar": False}, figure=make_preproc(), className="preprocess"),
    html.Div(id='blink-indicator', className='indicator', children=[
        html.H3(children="Blink")
    ]),
    html.Div(id='hidden-div', style={'display': 'none'}),
    html.Button('Reset Graphs', id='reset_button'),
    dcc.Interval(
        id='timer',
        interval=REFRESH_RATE*1000
    ),
])


def update_data(new, match):
    global data, is_match, d_len
    data = new
    #print("UPDATED DATA", data)
    is_match = match
    d_len += 1


@app.callback(Output('channelgraphs', 'extendData'),
              Input('timer', 'n_intervals'))
def update_raw(n):
    return [{
        "x": [data['time'], data['time'], data['time']],
        "y": [data['ch1'], data['ch2'], data['ch3']]
    }, [0, 1, 2]]


@app.callback(Output("preprocessed", 'extendData'),
              Input('timer', 'n_intervals'))
def update_preproc(n):
    return [{"x": [data['time']], "y": [data['preprocessed']]}, [0]]


@app.callback(Output('blink-indicator', 'className'),
              Input('timer', 'n_intervals'))
def update_indicator(n):
    # while n != None and d_len < n:
    #    time.sleep(0.1)
    if is_match:
        return 'indicator yes'
    return 'indicator'


@app.callback([Output('channelgraphs', 'figure'), Output("preprocessed", 'figure')], Input('reset_button', 'n_clicks'))
def reset_graph(n):
    if n == 0:
        raise PreventUpdate
    print("button click")
    global data
    data = {
        "ch1": [],
        "ch2": [],
        "ch3": [],
        "time": [],
        "preprocessed": [],
    }
    return [make_raw(), make_preproc()]


def run_server():
    app.run_server()


if __name__ == "__main__":
    run_server()
