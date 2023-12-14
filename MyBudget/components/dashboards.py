from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar

from globals import *
from app import app

from dash_bootstrap_templates import template_from_url, ThemeChangerAIO

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

graph_margin = dict(l=25, r=25, t=25, b=0)


# =========  Layout  =========== #
def render_layout(username):
    layout = dbc.Col(
        [
            dbc.Row(
                [
                    # balance
                    dbc.Col(
                        [
                            dbc.CardGroup(
                                [
                                    dbc.Card(
                                        [
                                            html.Legend("Saldo"),
                                            html.H5(
                                                "R$ -",
                                                id="p-balance-dashboards",
                                                style={},
                                            ),
                                        ],
                                        style={
                                            "padding-left": "20px",
                                            "padding-top": "10px",
                                        },
                                    ),
                                    dbc.Card(
                                        html.Div(
                                            className="fa fa-university",
                                            style=card_icon,
                                        ),
                                        color="warning",
                                        style={
                                            "maxWidth": 75,
                                            "height": 100,
                                            "margin-left": "-10px",
                                        },
                                    ),
                                ]
                            )
                        ],
                        width=4,
                    ),
                    # Receita
                    dbc.Col(
                        [
                            dbc.CardGroup(
                                [
                                    dbc.Card(
                                        [
                                            html.Legend("Receita"),
                                            html.H5("R$ -", id="p-revenue-dashboards"),
                                        ],
                                        style={
                                            "padding-left": "20px",
                                            "padding-top": "10px",
                                        },
                                    ),
                                    dbc.Card(
                                        html.Div(
                                            className="fa fa-smile-o", style=card_icon
                                        ),
                                        color="success",
                                        style={
                                            "maxWidth": 75,
                                            "height": 100,
                                            "margin-left": "-10px",
                                        },
                                    ),
                                ]
                            )
                        ],
                        width=4,
                    ),
                    # Despesa
                    dbc.Col(
                        [
                            dbc.CardGroup(
                                [
                                    dbc.Card(
                                        [
                                            html.Legend("Despesas"),
                                            html.H5("R$ -", id="p-expense-dashboards"),
                                        ],
                                        style={
                                            "padding-left": "20px",
                                            "padding-top": "10px",
                                        },
                                    ),
                                    dbc.Card(
                                        html.Div(
                                            className="fa fa-meh-o", style=card_icon
                                        ),
                                        color="danger",
                                        style={
                                            "maxWidth": 75,
                                            "height": 100,
                                            "margin-left": "-10px",
                                        },
                                    ),
                                ]
                            )
                        ],
                        width=4,
                    ),
                ],
                style={"margin": "10px"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    html.Legend(
                                        "Filtrar lançamentos", className="card-title"
                                    ),
                                    html.Label("Categorias das receitas"),
                                    html.Div(
                                        dcc.Dropdown(
                                            id="dropdown-revenue",
                                            clearable=False,
                                            style={"width": "100%"},
                                            persistence=True,
                                            persistence_type="session",
                                            multi=True,
                                        )
                                    ),
                                    html.Label(
                                        "Categorias das despesas",
                                        style={"margin-top": "10px"},
                                    ),
                                    dcc.Dropdown(
                                        id="dropdown-expense",
                                        clearable=False,
                                        style={"width": "100%"},
                                        persistence=True,
                                        persistence_type="session",
                                        multi=True,
                                    ),
                                    html.Legend(
                                        "Período de Análise",
                                        style={"margin-top": "10px"},
                                    ),
                                    dcc.DatePickerRange(
                                        month_format="Do MMM, YY",
                                        end_date_placeholder_text="Data...",
                                        start_date=datetime.today(),
                                        end_date=datetime.today() + timedelta(days=31),
                                        with_portal=True,
                                        updatemode="singledate",
                                        id="date-picker-config",
                                        style={"z-index": "100"},
                                    ),
                                ],
                                style={"height": "100%", "padding": "20px"},
                            ),
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(id="graph1"),
                            style={"height": "100%", "padding": "10px"},
                        ),
                        width=8,
                    ),
                ],
                style={"margin": "10px"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(dcc.Graph(id="graph2"), style={"padding": "10px"}),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Card(dcc.Graph(id="graph3"), style={"padding": "10px"}),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Card(dcc.Graph(id="graph4"), style={"padding": "10px"}),
                        width=3,
                    ),
                ],
                style={"margin": "10px"},
            ),
        ]
    )
    return layout


# =========  Callbacks  =========== #
# Dropdown Receita
@app.callback(
    [
        Output("dropdown-revenue", "options"),
        Output("dropdown-revenue", "value"),
        Output("p-revenue-dashboards", "children"),
    ],
    Input("store-revenues", "data"),
)
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df["Valor"].sum()
    val = df.Categoria.unique().tolist()

    return [
        ([{"label": x, "value": x} for x in df.Categoria.unique()]),
        val,
        f"R$ {valor}",
    ]


# Dropdown Despesa
@app.callback(
    [
        Output("dropdown-expense", "options"),
        Output("dropdown-expense", "value"),
        Output("p-expense-dashboards", "children"),
    ],
    Input("store-expenses", "data"),
)
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df["Valor"].sum()
    val = df.Categoria.unique().tolist()

    return [
        ([{"label": x, "value": x} for x in df.Categoria.unique()]),
        val,
        f"R$ {valor}",
    ]


# VALOR - saldo
@app.callback(
    Output("p-balance-dashboards", "children"),
    [Input("store-expenses", "data"), Input("store-revenues", "data")],
)
def balance_total(expenses, revenues):
    df_expenses = pd.DataFrame(expenses)
    df_revenues = pd.DataFrame(revenues)

    valor = df_revenues["Valor"].sum() - df_expenses["Valor"].sum()

    return f"R$ {valor}"


# Gráfico 1
@app.callback(
    Output("graph1", "figure"),
    [
        Input("store-expenses", "data"),
        Input("store-revenues", "data"),
        Input("dropdown-expense", "value"),
        Input("dropdown-revenue", "value"),
        Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    ],
)
def update_output(data_expense, data_revenue, expense, revenue, theme):
    df_ds = pd.DataFrame(data_expense).sort_values(by="Data", ascending=True)
    df_rc = pd.DataFrame(data_revenue).sort_values(by="Data", ascending=True)

    dfs = [df_ds, df_rc]
    for df in dfs:
        df["Acumulo"] = df["Valor"].cumsum()
        df["Data"] = pd.to_datetime(df["Data"])
        df["Mes"] = df["Data"].apply(lambda x: x.month)

    df_revenues_mes = df_rc.groupby("Mes")["Valor"].sum()
    df_expenses_mes = df_ds.groupby("Mes")["Valor"].sum()
    df_balance_mes = df_revenues_mes - df_expenses_mes
    df_balance_mes.to_frame()

    df_balance_mes = df_balance_mes.reset_index()
    df_balance_mes["Acumulado"] = df_balance_mes["Valor"].cumsum()
    # df_balance_mes["Mes"] = df["Mes"].apply(lambda x: calendar.month_abbr[x])

    df_ds = df_ds[df_ds["Categoria"].isin(expense)]
    df_rc = df_rc[df_rc["Categoria"].isin(revenue)]

    fig = go.Figure()

    # fig.add_trace(go.Scatter(name='Despesas', x=df_ds['Data'], y=df_ds['Acumulo'], fill='tonexty', mode='lines'))
    fig.add_trace(
        go.Scatter(
            name="Receitas",
            x=df_rc["Data"],
            y=df_rc["Acumulo"],
            fill="tonextx",
            mode="lines",
        )
    )
    # fig.add_trace(go.Scatter(name='balance Mensal', x=df_balance_mes['Mes'], y=df_balance_mes['Acumulado'], mode='lines'))

    fig.update_layout(
        margin=graph_margin, height=350, template=template_from_url(theme)
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig


# Gráfico 2
@app.callback(
    Output("graph2", "figure"),
    [
        Input("store-revenues", "data"),
        Input("store-expenses", "data"),
        Input("dropdown-revenue", "value"),
        Input("dropdown-expense", "value"),
        Input("date-picker-config", "start_date"),
        Input("date-picker-config", "end_date"),
        Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    ],
)
def graph2_show(
    data_revenue, data_expense, revenue, expense, start_date, end_date, theme
):
    df_ds = pd.DataFrame(data_expense)
    df_rc = pd.DataFrame(data_revenue)

    dfs = [df_ds, df_rc]

    df_rc["Output"] = "Receitas"
    df_ds["Output"] = "Despesas"
    df_final = pd.concat(dfs)

    mask = (df_final["Data"] > start_date) & (df_final["Data"] <= end_date)
    df_final = df_final.loc[mask]

    df_final = df_final[
        df_final["Categoria"].isin(revenue) | df_final["Categoria"].isin(expense)
    ]

    fig = px.bar(df_final, x="Data", y="Valor", color="Output", barmode="group")
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

    return fig


# Gráfico 3
@app.callback(
    Output("graph3", "figure"),
    [
        Input("store-revenues", "data"),
        Input("dropdown-revenue", "value"),
        Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    ],
)
def pie_revenue(data_revenue, revenue, theme):
    df = pd.DataFrame(data_revenue)
    df = df[df["Categoria"].isin(revenue)]

    fig = px.pie(df, values=df.Valor, names=df.Categoria, hole=0.2)
    fig.update_layout(title={"text": "Receitas"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))  #
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

    return fig


# Gráfico 4
@app.callback(
    Output("graph4", "figure"),
    [
        Input("store-expenses", "data"),
        Input("dropdown-expense", "value"),
        Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    ],
)
def pie_expense(data_expense, expense, theme):  #
    df = pd.DataFrame(data_expense)
    df = df[df["Categoria"].isin(expense)]

    fig = px.pie(df, values=df.Valor, names=df.Categoria, hole=0.2)
    fig.update_layout(title={"text": "Despesas"})

    fig.update_layout(margin=graph_margin, template=template_from_url(theme))  #
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

    return fig
