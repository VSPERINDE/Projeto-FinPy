from dash import html, dcc
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from flask_login import current_user, LoginManager
from app import *
from database import db
from components import home, login, register

# from globals import *

# DataFrames and Dcc.Store

# df_revenues = pd.read_csv("df_revenues.csv", index_col=0, parse_dates=True)
# df_revenues_aux = df_revenues.to_dict()
#
# df_expenses = pd.read_csv("df_expenses.csv", index_col=0, parse_dates=True)
# df_expenses_aux = df_expenses.to_dict()
#
# list_revenues = pd.read_csv("df_cat_revenues.csv", index_col=0)
# list_revenues_aux = list_revenues.to_dict()
#
# list_expenses = pd.read_csv("df_cat_expenses.csv", index_col=0)
# list_expenses_aux = list_expenses.to_dict()

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

# =========  Layout  =========== #

app.layout = dbc.Container(
    children=[
        # dcc.Store(id="store-revenues", data=df_revenues_aux),
        # dcc.Store(id="store-expenses", data=df_expenses_aux),
        # dcc.Store(id="stored-cat-revenues", data=list_revenues_aux),
        # dcc.Store(id="stored-cat-expenses", data=list_expenses_aux),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Location(id="base-url", refresh=False),
                        dcc.Store(id="login-state", data=""),
                        dcc.Store(id="register-state", data=""),
                        html.Div(
                            id="page-content",
                            style={
                                "height": "100vh",
                                "display": "flex",
                                "justify-content": "center",
                            },
                        ),
                    ]
                ),
            ]
        ),
    ],
    fluid=True,
    style={"padding": "0px"},
    className="dbc",
)


@login_manager.user_loader
def load_user(id):
    return db.users.find_one({"id": id})


@app.callback(
    Output("base-url", "pathname"),
    [Input("login-state", "data"), Input("register-state", "data")],
)
def render_page_content(login_state, register_state):
    ctx = dash.callback_context
    if ctx.triggered:
        trigg_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigg_id == "login-state" and login_state == "success":
            return "/home"
        if trigg_id == "login-state" and login_state == "error":
            return "/login"

        elif trigg_id == "register-state":
            print(register_state, register_state == "")
            if register_state == "":
                return "/login"
            else:
                return "/register"
    else:
        return "/"


@app.callback(
    Output("page-content", "children"),
    Input("base-url", "pathname"),
    [State("login-state", "data"), State("register-state", "data")],
)
def render_page_content(pathname, login_state, register_state):
    if pathname == "/login" or pathname == "/":
        return login.login_layout(login_state)

    if pathname == "/register":
        return register.register_layout(register_state)

    if pathname == "/home":
        print(current_user)
        if current_user.is_authenticated:
            return home.render_layout(current_user.username)
        else:
            return login.login_layout(register_state)


if __name__ == "__main__":
    app.run_server(port=8051, debug=True)
