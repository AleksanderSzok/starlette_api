from dash import Dash, dcc, html, Input, Output, State

from json_to_xml_converter import JsonToXml

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H2("Paste json!"),
        html.Div([dcc.Textarea(id="my-input", value='{"a":1}')]),
        html.Button(children="Change to xml!", n_clicks=0, id="btn-1"),
        html.Br(),
        html.Div(id="my-output", style={"whiteSpace": "pre"}),
    ]
)


@app.callback(
    Output(component_id="my-output", component_property="children"),
    Input(component_id="btn-1", component_property="n_clicks"),
    State("my-input", "value"),
)
def update_output_div(n_clicks, input_value):
    xml = JsonToXml(json_string=input_value)
    xml.json_to_xml()
    return html.Div(str(xml))


if __name__ == "__main__":
    app.run_server(debug=True)
