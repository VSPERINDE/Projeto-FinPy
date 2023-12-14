import os
import dash
import tabula
import io
import base64
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
from dash_bootstrap_templates import ThemeChangerAIO
import plotly.express as px
import numpy as np
import pandas as pd

from globals import *

# ========= Layout ========= #


def render_layout(username):
    layout = dbc.Col(
        [
            html.H1("FinPy - Projeto Financeiro", className="text-primary"),
            html.P("By VSPERINDE", className="text-info"),
            html.Hr(),
            # Seção Perfil ---------------------------
            dbc.Row(
                [
                    dbc.Button(
                        id="botao_avatar",
                        children=[
                            html.Img(
                                src="/assets/img_hom.png",
                                id="avatar_change",
                                alt="Avatar",
                                className="perfil_avatar",
                            )
                        ],
                        style={
                            "background-color": "transparent",
                            "border-color": "transparent",
                        },
                    ),
                ],
                id="row-avatar",
            ),
            dbc.Row([
                dbc.Col(html.Div([
                    html.Label(username, className='form-label'),
                ], id='user'), width=3),
            ]),
            # Seção Novo ---------------------------
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Button(
                                color="success",
                                id="open-new-revenue",
                                children=["+ Receita"],
                                className="plus-button",
                            )
                        ],
                        width=6,
                        className="col-plus-button",
                    ),
                    dbc.Col(
                        [
                            dbc.Button(
                                color="danger",
                                id="open-new-expense",
                                children=["- Despesa"],
                                className="plus-button",
                            )
                        ],
                        width=6,
                        className="col-plus-button",
                    ),
                ]
            ),
            # Seção Modal ---------------------------
            # Nova receita
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Adicionar Receita")),
                    dbc.ModalBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label("Descrição: "),
                                            dbc.Input(
                                                placeholder="Ex.: Sálario, participação de lucros...",
                                                id="txt-revenue",
                                            ),
                                        ],
                                        width=6,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label("Valor: "),
                                            dbc.Input(
                                                placeholder="$100.00",
                                                id="value-revenue",
                                                value="",
                                            ),
                                        ],
                                        width=6,
                                    ),
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label("Data: "),
                                            dcc.DatePickerSingle(
                                                id="date-revenue",
                                                min_date_allowed=date(2020, 1, 1),
                                                max_date_allowed=date(
                                                    datetime.now().year + 10, 12, 31
                                                ),
                                                date=datetime.today(),
                                                style={"width": "100%"},
                                            ),
                                        ],
                                        width=4,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label("Extras"),
                                            dbc.Checklist(
                                                options=[
                                                    {
                                                        "label": "Foi recebida",
                                                        "value": 1,
                                                    },
                                                    {
                                                        "label": "Receita Recorrente",
                                                        "value": 2,
                                                    },
                                                ],
                                                value=[1],
                                                id="switches-input-revenue",
                                                switch=True,
                                            ),
                                        ],
                                        width=4,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Label("Categoria da receita"),
                                            dbc.Select(
                                                id="select-revenue",
                                                options=[
                                                    {"label": i, "value": i}
                                                    for i in cat_revenues
                                                ],
                                                value=cat_revenues[0],
                                            ),
                                        ],
                                        width=4,
                                    ),
                                ],
                                style={"margin-top": "25px"},
                            ),
                            dbc.Row(
                                [
                                    dbc.Accordion(
                                        [
                                            dbc.AccordionItem(
                                                children=[
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                [
                                                                    html.Legend(
                                                                        "Adicionar categoria",
                                                                        style={
                                                                            "color": "green"
                                                                        },
                                                                    ),
                                                                    dbc.Input(
                                                                        type="text",
                                                                        placeholder="Nova categoria...",
                                                                        id="input-add-revenue",
                                                                        value="",
                                                                    ),
                                                                    html.Br(),
                                                                    dbc.Button(
                                                                        "Adicionar",
                                                                        className="btn btn-success",
                                                                        id="add-category-revenue",
                                                                        style={
                                                                            "margin-top": "20px"
                                                                        },
                                                                    ),
                                                                    html.Br(),
                                                                    html.Div(
                                                                        id="category-div-add-revenue",
                                                                        style={},
                                                                    ),
                                                                ],
                                                                width=5,
                                                                style={
                                                                    "margin": "20px"
                                                                },
                                                            ),
                                                            dbc.Col(
                                                                [
                                                                    html.Legend(
                                                                        "Excluir categorias",
                                                                        style={
                                                                            "color": "red"
                                                                        },
                                                                    ),
                                                                    dbc.Checklist(
                                                                        id="checklist-selected-style-revenue",
                                                                        options=[
                                                                            {
                                                                                "label": i,
                                                                                "value": i,
                                                                            }
                                                                            for i in cat_revenues
                                                                        ],
                                                                        value=[],
                                                                        label_checked_style={
                                                                            "color": "red"
                                                                        },
                                                                        input_checked_style={
                                                                            "backgroundColor": "blue",
                                                                            "borderColor": "orange",
                                                                        },
                                                                    ),
                                                                    dbc.Button(
                                                                        "Remover",
                                                                        color="warning",
                                                                        id="remove-category-revenue",
                                                                        style={
                                                                            "margin-top": "20px"
                                                                        },
                                                                    ),
                                                                ],
                                                                width=5,
                                                                style={
                                                                    "margin": "20px",
                                                                },
                                                            ),
                                                        ]
                                                    )
                                                ],
                                                title="Adicionar/Remover Categorias",
                                            )
                                        ],
                                        flush=True,
                                        start_collapsed=True,
                                        id="accordion-revenue",
                                    ),
                                    html.Div(
                                        id="id_test_revenue",
                                        style={"padding-top": "20px"},
                                    ),
                                    dbc.ModalFooter(
                                        [
                                            dbc.Button(
                                                "Adicionar Receita",
                                                id="save_revenue",
                                                color="success",
                                            ),
                                            dbc.Popover(
                                                dbc.PopoverBody("Receita Salva"),
                                                target="save_revenue",
                                                placement="left",
                                                trigger="click",
                                            ),
                                        ]
                                    ),
                                ],
                                style={"margin-top": "25px"},
                            ),
                        ]
                    ),
                ],
                style={"background-color": "rgba(17, 140, 79, 0.05)"},
                id="modal-new-revenue",
                size="lg",
                is_open=False,
                centered=True,
                backdrop=True,
            ),
            # Nova Despesa
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Adicionar Despesa")),
                    dbc.ModalBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label("Descrição: "),
                                            dbc.Input(
                                                placeholder="Ex.: Conta de luz, restaurante, gasolina...",
                                                id="txt-expense",
                                            ),
                                        ],
                                        width=6,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label("Valor: "),
                                            dbc.Input(
                                                placeholder="$100.00",
                                                id="value-expense",
                                                value="",
                                            ),
                                        ],
                                        width=6,
                                    ),
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label("Data: "),
                                            dcc.DatePickerSingle(
                                                id="date-expense",
                                                min_date_allowed=date(2020, 1, 1),
                                                max_date_allowed=date(
                                                    datetime.now().year + 10, 12, 31
                                                ),
                                                date=datetime.today(),
                                                style={"width": "100%"},
                                            ),
                                        ],
                                        width=4,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label("Extras"),
                                            dbc.Checklist(
                                                options=[
                                                    {"label": "Foi paga", "value": 1},
                                                    {
                                                        "label": "Despesa Recorrente",
                                                        "value": 2,
                                                    },
                                                ],
                                                value=[1],
                                                id="switches-input-expense",
                                                switch=True,
                                            ),
                                        ],
                                        width=4,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Label("Categoria da despesa"),
                                            dbc.Select(
                                                id="select-expense",
                                                options=[
                                                    {"label": i, "value": i}
                                                    for i in cat_expenses
                                                ],
                                                value=cat_expenses[0],
                                            ),
                                        ],
                                        width=4,
                                    ),
                                ],
                                style={"margin-top": "25px"},
                            ),
                            dbc.Row(
                                [
                                    dbc.Accordion(
                                        [
                                            dbc.AccordionItem(
                                                children=[
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                [
                                                                    html.Legend(
                                                                        "Adicionar categoria",
                                                                        style={
                                                                            "color": "green"
                                                                        },
                                                                    ),
                                                                    dbc.Input(
                                                                        type="text",
                                                                        placeholder="Nova categoria...",
                                                                        id="input-add-expense",
                                                                        value="",
                                                                    ),
                                                                    html.Br(),
                                                                    dbc.Button(
                                                                        "Adicionar",
                                                                        className="btn btn-success",
                                                                        id="add-category-expense",
                                                                        style={
                                                                            "margin-top": "20px"
                                                                        },
                                                                    ),
                                                                    html.Br(),
                                                                    html.Div(
                                                                        id="category-div-add-expense",
                                                                        style={},
                                                                    ),
                                                                ],
                                                                width=6,
                                                            ),
                                                            dbc.Col(
                                                                [
                                                                    html.Legend(
                                                                        "Excluir categorias",
                                                                        style={
                                                                            "color": "red"
                                                                        },
                                                                    ),
                                                                    dbc.Checklist(
                                                                        id="checklist-selected-style-expense",
                                                                        options=[
                                                                            {
                                                                                "label": i,
                                                                                "value": i,
                                                                            }
                                                                            for i in cat_expenses
                                                                        ],
                                                                        value=[],
                                                                        label_checked_style={
                                                                            "color": "red"
                                                                        },
                                                                        input_checked_style={
                                                                            "backgroundColor": "blue",
                                                                            "borderColor": "orange",
                                                                        },
                                                                    ),
                                                                    dbc.Button(
                                                                        "Remover",
                                                                        color="warning",
                                                                        id="remove-category-expense",
                                                                        style={
                                                                            "margin-top": "20px"
                                                                        },
                                                                    ),
                                                                ],
                                                                width=6,
                                                            ),
                                                        ]
                                                    )
                                                ],
                                                title="Adicionar/Remover Categorias",
                                            )
                                        ],
                                        flush=True,
                                        start_collapsed=True,
                                        id="accordion-expense",
                                    ),
                                    html.Div(
                                        id="id_test_expense",
                                        style={"padding-top": "20px"},
                                    ),
                                    dbc.ModalFooter(
                                        [
                                            dbc.Button(
                                                "Adicionar Despesa",
                                                id="save_expense",
                                                color="success",
                                            ),
                                            dbc.Popover(
                                                dbc.PopoverBody("Despesa Salva"),
                                                target="save_expense",
                                                placement="left",
                                                trigger="click",
                                            ),
                                        ]
                                    ),
                                ],
                                style={"margin-top": "25px"},
                            ),
                        ]
                    ),
                ],
                style={"background-color": "rgba(17, 140, 79, 0.05)"},
                id="modal-new-expense",
                size="lg",
                is_open=False,
                centered=True,
                backdrop=True,
            ),
            # section Nav
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Dashboard", href="/dashboards", active="exact"),
                    dbc.NavLink("Extratos", href="/extratos", active="exact"),
                ],
                vertical=True,
                pills=True,
                id="nav_buttons",
                style={"margin-botton": "50px"},
            ),
            html.Hr(),
            # Section upload
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.P("Upload extratos: "),
                                    dcc.Upload(
                                        id="upload-data",
                                        children=[
                                            html.A(
                                                "Clique e selecione um arquivo PDF",
                                                id="upload-label",
                                            ),
                                        ],
                                        className="upload-area",
                                        multiple=True,
                                    ),
                                    html.Button(
                                        "Enviar",
                                        id="submit-button",
                                        n_clicks=0,
                                        className="submit-button",
                                    ),
                                    html.Div(id="output-data", className="output-text"),
                                ],
                            ),
                        ],
                    )
                ]
            ),
            ThemeChangerAIO(
                aio_id="theme", radio_props={"value": dbc.themes.BOOTSTRAP}
            ),
        ],
        id="sidebar_finished",
        style={"margin": "10px"},
    )
    return layout


# =========  Callbacks  =========== #
# Pop-up receita


@app.callback(
    Output("modal-new-revenue", "is_open"),
    Input("open-new-revenue", "n_clicks"),
    State("modal-new-revenue", "is_open"),
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open


# Pop-up despesa
@app.callback(
    Output("modal-new-expense", "is_open"),
    Input("open-new-expense", "n_clicks"),
    State("modal-new-expense", "is_open"),
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open


# Add/Remove categoria despesa
@app.callback(
    [
        Output("category-div-add-expense", "children"),
        Output("category-div-add-expense", "style"),
        Output("select-expense", "options"),
        Output("checklist-selected-style-expense", "options"),
        Output("checklist-selected-style-expense", "value"),
        Output("stored-cat-expenses", "data"),
    ],
    [
        Input("add-category-expense", "n_clicks"),
        Input("remove-category-expense", "n_clicks"),
    ],
    [
        State("input-add-expense", "value"),
        State("checklist-selected-style-expense", "value"),
        State("stored-cat-expenses", "data"),
    ],
)
def add_category(n, n2, txt, check_delete, data):
    cat_expenses = list(data["Categoria"].values())

    txt1 = []
    style1 = {}

    if n:
        if txt == "" or txt == None:
            txt1 = "O campo de texto não pode estar vazio para o registro de uma nova categoria."
            style1 = {"color": "red"}

        else:
            cat_expenses = (
                cat_expenses + [txt] if txt not in cat_expenses else cat_expenses
            )
            txt1 = f"A categoria {txt} foi adicionada com sucesso!"
            style1 = {"color": "green"}

    if n2:
        if len(check_delete) > 0:
            cat_expenses = [i for i in cat_expenses if i not in check_delete]

    opt_expense = [{"label": i, "value": i} for i in cat_expenses]
    df_cat_expenses = pd.DataFrame(cat_expenses, columns=["Categoria"])
    df_cat_expenses.to_csv("df_cat_expenses.csv")
    data_return = df_cat_expenses.to_dict()

    return [txt1, style1, opt_expense, opt_expense, [], data_return]


# Add/Remove categoria receita
@app.callback(
    [
        Output("category-div-add-revenue", "children"),
        Output("category-div-add-revenue", "style"),
        Output("select-revenue", "options"),
        Output("checklist-selected-style-revenue", "options"),
        Output("checklist-selected-style-revenue", "value"),
        Output("stored-cat-revenues", "data"),
    ],
    [
        Input("add-category-revenue", "n_clicks"),
        Input("remove-category-revenue", "n_clicks"),
    ],
    [
        State("input-add-revenue", "value"),
        State("checklist-selected-style-revenue", "value"),
        State("stored-cat-revenues", "data"),
    ],
)
def add_category(n, n2, txt, check_delete, data):
    cat_revenues = list(data["Categoria"].values())

    txt1 = []
    style1 = {}

    if n:
        if txt == "" or txt == None:
            txt1 = "O campo de texto não pode estar vazio para o registro de uma nova categoria."
            style1 = {"color": "red"}

    if n and not (txt == "" or txt == None):
        cat_revenues = cat_revenues + [txt] if txt not in cat_revenues else cat_revenues
        txt1 = f"A categoria {txt} foi adicionada com sucesso!"
        style1 = {"color": "green"}

    if n2:
        if check_delete == []:
            pass
        else:
            cat_revenues = [i for i in cat_revenues if i not in check_delete]

    opt_revenue = [{"label": i, "value": i} for i in cat_revenues]
    df_cat_revenues = pd.DataFrame(cat_revenues, columns=["Categoria"])
    df_cat_revenues.to_csv("df_cat_revenues.csv")
    data_return = df_cat_revenues.to_dict()

    return [txt1, style1, opt_revenue, opt_revenue, [], data_return]


# Enviar Form receita
@app.callback(
    Output("store-revenues", "data"),
    Input("save_revenue", "n_clicks"),
    [
        State("txt-revenue", "value"),
        State("value-revenue", "value"),
        State("date-revenue", "date"),
        State("switches-input-revenue", "value"),
        State("select-revenue", "value"),
        State("store-revenues", "data"),
    ],
)
def save_form_revenue(n, description, value, date, switches, category, dict_revenues):
    df_revenues = pd.DataFrame(dict_revenues)

    if n and not (value == "" or value == None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        category = category[0] if type(category) == list else category

        recebido = 1 if 1 in switches else 0
        fixo = 0 if 2 in switches else 0

        df_revenues.loc[df_revenues.shape[0]] = [
            value,
            recebido,
            fixo,
            date,
            category,
            description,
        ]
        df_revenues.to_csv("df_revenues.csv")

    data_return = df_revenues.to_dict()
    return data_return


# Enviar Form despesa
@app.callback(
    Output("store-expenses", "data"),
    Input("save_expense", "n_clicks"),
    [
        State("value-expense", "value"),
        State("switches-input-expense", "value"),
        State("select-expense", "value"),
        State("date-expense", "date"),
        State("txt-expense", "value"),
        State("store-expenses", "data"),
    ],
)
def save_form_expense(n, value, switches, category, date, description, dict_expenses):
    df_expenses = pd.DataFrame(dict_expenses)

    if n and not (value == "" or value == None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        category = category[0] if type(category) == list else category

        recebido = 1 if 1 in switches else 0
        fixo = 0 if 2 in switches else 0

        if description == None or description == "":
            description = 0

        df_expenses.loc[df_expenses.shape[0]] = [
            value,
            recebido,
            fixo,
            date,
            category,
            description,
        ]
        df_expenses.to_csv("df_expenses.csv")

    data_return = df_expenses.to_dict()
    return data_return


# callback para o upload do arquivo
@app.callback(
    Output("output-data", "children"),
    Input("submit-button", "n_clicks"),
    State("upload-data", "contents"),
    prevent_initial_call=True,
)
def process_pdf(n_clicks, contents):
    if n_clicks > 0 and contents is not None:
        # Lê o conteúdo do arquivo PDF
        decoded_content = contents.encode("utf-8")
        df = tabula.read_pdf(io.BytesIO(decoded_content), pages="all")

        # Salva o DataFrame como um arquivo CSV no computador
        if not df:
            return "Nenhuma tabela encontrada no PDF."
        else:
            csv_file = "output.csv"
            df.to_csv(csv_file, index=False)

            return f'Arquivo CSV salvo como "{csv_file}" no seu computador.'
