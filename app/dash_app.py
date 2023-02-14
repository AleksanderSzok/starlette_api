import json
import logging

from dash import Dash, dcc, html, Input, Output, State
import requests

app = Dash(__name__)

colors = {"background": "#000000", "text": "#7FDBFF"}

base_url = "http://starlette_app:8000"

app.layout = html.Div(
    [
        html.H1(children="Paste json!", style={"color": colors["text"]}),
        html.Div(
            [
                dcc.Textarea(
                    id="json-input",
                    value='{"a":1}',
                    style={
                        "color": colors["text"],
                        "width": "220px",
                        "height": "220px",
                        "font-size": "18px",
                        "backgroundColor": colors["background"],
                    },
                )
            ]
        ),
        html.Div(
            dcc.Input(
                id="element-input",
                placeholder="element name for json arrays",
                type="text",
                style={
                    "color": colors["text"],
                    "backgroundColor": colors["background"],
                    "font-size": "16px",
                    "width": "220px",
                    "height": "40px",
                },
            )
        ),
        html.Br(),
        html.Button(children="Change to xml!", n_clicks=0, id="btn-1"),
        html.Br(),
        html.Br(),
        html.Div(id="output", style={"whiteSpace": "pre", "color": colors["text"]}),
    ],
    style={"backgroundColor": colors["background"]},
)


@app.callback(
    Output(component_id="output", component_property="children"),
    Input(component_id="btn-1", component_property="n_clicks"),
    State(component_id="element-input", component_property="value"),
    State(component_id="json-input", component_property="value"),
)
def update_output_div(n_clicks, element_name, json_data):
    data = {"json": json_data, "element_name": element_name}
    data = json.dumps(data)
    r = requests.post(url=f"{base_url}/to_xml", data=data)
    return html.Div(r.text)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=False)
