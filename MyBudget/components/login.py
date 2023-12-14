import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask
from flask_login import login_user
from database import db
from werkzeug.security import check_password_hash
from components.user import User
from dash.exceptions import PreventUpdate
from app import app

# Layout da página de login
card_style = {
    "width": "300px",
    "min-height": "300px",
    "padding-top": "25px",
    "padding-right": "25px",
    "padding-left": "25px",
}


def login_layout(message):
    message = "Ocorreu algum erro durante o login." if message == "error" else message
    render_layout = dbc.Card(
        [
            dbc.Form(
                [
                    html.H1("Login"),
                    html.Div(
                        [
                            dbc.Label("Email"),
                            dbc.Input(
                                type="email",
                                id="login-email",
                                style={"border": "1px solid #48484873"},
                            ),
                        ],
                        className="mb-2",
                    ),
                    html.Div(
                        [
                            dbc.Label("Senha"),
                            dbc.Input(
                                type="password",
                                id="login-password",
                                style={"border": "1px solid #48484873"},
                            ),
                        ],
                        className="mb-2",
                    ),
                    dbc.Button(
                        "Entrar",
                        id="login-button",
                        color="primary",
                        className="btn btn-primary mt-3",
                    ),
                ],
                style={
                    "justify-content": "center",
                    "display": "grid",
                },
            ),
            html.Div(
                [
                    html.Label("Ou", style={"margin-right": "5px"}),
                    dcc.Link("Registre-se", href="/register"),
                ],
                style={
                    "padding": "20px",
                    "justify-content": "center",
                    "display": "flex",
                },
            ),
        ],
        className="align-self-center",
        style=card_style,
    )
    return render_layout


# Callback para o login
@app.callback(
    Output("login-state", "data"),
    [Input("login-button", "n_clicks")],
    [
        dash.dependencies.State("login-email", "value"),
        dash.dependencies.State("login-password", "value"),
    ],
)
def success_login(n_clicks, email, password):
    if n_clicks == None:
        raise PreventUpdate
        # Verifique as credenciais no MongoDB
    user = db.users.find_one({"email": email})
    if user and password is not None:
        if check_password_hash(user.get("password"), password):
            user_data = User(user)
            login_user(user_data)
            return (
                "success"  # html.Div("Login bem-sucedido!", style={"color": "green"})
            )
        else:
            return "error"  # html.Div(                    "Login falhou. Verifique suas credenciais.", style={"color": "red"}                )
    else:
        return "error"  # html.Div(                "Login falhou. Verifique suas credenciais.", style={"color": "red"}            )
