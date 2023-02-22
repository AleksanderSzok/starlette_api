import base64
import dataclasses
import json

from dash import Dash, dcc, html, Input, Output, State, ctx
import requests

app = Dash(__name__)

colors = {"background": "#000000", "text": "#7FDBFF"}

base_url = "http://starlette_app:8000"

# base_url = "http://127.0.0.1:8000"


@dataclasses.dataclass
class DataStorage:
    data: str


app.storage = DataStorage(data="")

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
        html.Div(
            [
                html.Button("Download XML", id="btn-download-xml"),
                dcc.Download(id="download-xml"),
            ]
        ),
        dcc.Upload(
            children=html.Button("Upload File"),
            id="upload-component",
        ),
        html.Button(children="Change to xml!", n_clicks=0, id="change-button"),
        html.Br(),
        html.Br(),
        html.Div(id="output", style={"whiteSpace": "pre", "color": colors["text"]}),
    ],
    style={"backgroundColor": colors["background"]},
)


@app.callback(
    Output(component_id="output", component_property="children"),
    Output(component_id="upload-component", component_property="contents"),
    Input(component_id="change-button", component_property="n_clicks"),
    State(component_id="element-input", component_property="value"),
    State(component_id="json-input", component_property="value"),
    Input(component_id="upload-component", component_property="contents"),
    Input(component_id="upload-component", component_property="filename"),
)
def update_output_div(n_clicks_change, element_name, json_data, upload_data, filename):
    if ctx.triggered_id == "upload-component" and "json" in filename:
        _, upload_data = upload_data.split(",")
        decoded = base64.b64decode(upload_data)
        json_data = json.loads(decoded)
    data = {"json": json_data, "element_name": element_name}
    data = json.dumps(data)
    r = requests.post(url=f"{base_url}/to_xml", data=data)
    app.storage = DataStorage(data=r.text)
    return html.Div(r.text), None


@app.callback(
    Output(component_id="download-xml", component_property="data"),
    Input(component_id="btn-download-xml", component_property="n_clicks"),
    prevent_initial_call=True,
)
def download_xml(n_click):
    return dict(content=app.storage.data, filename="output.txt")


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=False)
    # app.run_server(debug=False)
