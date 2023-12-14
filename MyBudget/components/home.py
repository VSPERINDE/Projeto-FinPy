from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from flask_login import current_user

# import from folders
from app import *
from components import sidebar, dashboards, extratos

# =========  Layout  =========== #
content = html.Div(id="main-content")


def render_layout(username):
    layout = dbc.Container(
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [dcc.Location(id="url"), sidebar.render_layout(username)], md=2
                    ),
                    dbc.Col([html.Div(id="main-content")], md=10),
                ]
            )
        ],
        fluid=True,
        style={"padding": "0px"},
        className="dbc",
    )
    return layout


@app.callback(Output("main-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/home" or pathname == "/dashboards":
        return dashboards.render_layout(current_user.username)

    if pathname == "/extratos":
        return extratos.render_layout(current_user.username)
