from dash import Dash, dcc, html, Input, Output, State
import requests

app = Dash(__name__)

colors = {"background": "#000000", "text": "#7FDBFF"}

app.layout = html.Div(
    [
        html.H1(children="Paste json!", style={"color": colors["text"]}),
        html.Div(
            [
                dcc.Textarea(
                    id="my-input",
                    value='{"a":1}',
                    style={
                        "color": colors["text"],
                        "width": "180px",
                        "font-size": "18px",
                        "backgroundColor": colors["background"],
                    },
                )
            ]
        ),
        html.Br(),
        html.Button(children="Change to xml!", n_clicks=0, id="btn-1"),
        html.Br(),
        html.Br(),
        html.Div(id="my-output", style={"whiteSpace": "pre", "color": colors["text"]}),
    ],
    style={"backgroundColor": colors["background"]},
)


@app.callback(
    Output(component_id="my-output", component_property="children"),
    Input(component_id="btn-1", component_property="n_clicks"),
    State("my-input", "value"),
)
def update_output_div(n_clicks, input_value):
    r = requests.post(url="http://127.0.0.1:8000/to_xml", data=input_value)
    return html.Div(r.text)


if __name__ == "__main__":
    app.run_server(debug=True)
