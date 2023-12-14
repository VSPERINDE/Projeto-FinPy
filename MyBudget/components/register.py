import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask
from database import db
from app import app
from flask_login import login_user
from components.user import User
from werkzeug.security import generate_password_hash
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO

card_style = {
    "width": "300px",
    "min-height": "300px",
    "padding-top": "25px",
    "padding-right": "25px",
    "padding-left": "25px",
}


# Layout da página de registro
def register_layout(message):
    message = (
        "Ocorreu algum erro durante o registro." if message == "error" else message
    )
    render_layout = dbc.Card(
        [
            dbc.Form(
                [
                    html.H1("Registro de Usuário"),
                    html.Div(
                        [
                            dbc.Label("Username"),
                            dbc.Input(
                                type="username",
                                id="username",
                                style={"border": "1px solid #48484873"},
                            ),
                        ],
                        className="mb-2",
                    ),
                    html.Div(
                        [
                            dbc.Label("Email"),
                            dbc.Input(
                                type="email",
                                id="email",
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
                                id="password",
                                style={"border": "1px solid #48484873"},
                            ),
                        ],
                        className="mb-2",
                    ),
                    dbc.Button(
                        "Registrar",
                        id="register-button",
                        color="primary",
                        className="btn btn-primary mt-3",
                    ),
                ],
                style={
                    "justify-content": "center",
                    "display": "grid",
                },
            ),
            html.Div(id="register-message"),
            html.Div(
                [
                    html.Label("Ou faça ", style={"margin-right": "5px"}),
                    dcc.Link("Login", href="/login"),
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


# Callback para o registro de usuário
@app.callback(
    Output("register-message", "children"),
    [Input("register-button", "n_clicks")],
    [
        dash.dependencies.State("username", "value"),
        dash.dependencies.State("email", "value"),
        dash.dependencies.State("password", "value"),
    ],
)
def register_user(n_clicks, username, email, password):
    if n_clicks:
        # Verifique se o usuário já existe no MongoDB
        user = db.users.find_one({"email": email})
        if user:
            return html.Div(
                "Este email já está em uso. Tente outro.", style={"color": "red"}
            )
        else:
            if username is not None and password is not None and email is not None:
                # Crie um novo usuário
                hashed_password = generate_password_hash(password, method="sha256")

                new_user_data = User(
                    {
                        "username": username,
                        "email": email,
                        "password": hashed_password,
                    }
                )
                db.users.insert_one(new_user_data)

                # Crie uma instância da classe Usuario
                new_user = db.users.find_one({"email": email})

                # Faça login do novo usuário
                login_user(new_user)

                return html.Div(
                    "Registro realizado com sucesso. Faça login.",
                    style={"color": "green"},
                )
            else:
                return html.Div(
                    "Nenhum campo pode ser vazio. Tente novamente.",
                    style={"color": "red"},
                )
