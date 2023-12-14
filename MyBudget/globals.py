import pandas as pd
import os

if ("df_expenses.csv" in os.listdir()) and ("df_revenues.csv" in os.listdir()):
    df_expenses = pd.read_csv("df_expenses.csv", index_col=0, parse_dates=True)
    df_revenues = pd.read_csv("df_revenues.csv", index_col=0, parse_dates=True)
    df_expenses["Data"] = pd.to_datetime(df_expenses["Data"])
    df_revenues["Data"] = pd.to_datetime(df_revenues["Data"])
    df_expenses["Data"] = df_expenses["Data"].apply(lambda x: x.date())
    df_revenues["Data"] = df_revenues["Data"].apply(lambda x: x.date())

else:
    data_structure = {
        "Valor": [],
        "Efetuado": [],
        "Fixo": [],
        "Data": [],
        "Categoria": [],
        "Descrição": [],
    }

    df_revenues = pd.DataFrame(data_structure)
    df_expenses = pd.DataFrame(data_structure)
    df_expenses.to_csv("df_expenses.csv")
    df_revenues.to_csv("df_revenues.csv")


if ("df_cat_revenues.csv" in os.listdir()) and ("df_cat_expenses.csv" in os.listdir()):
    df_cat_revenues = pd.read_csv("df_cat_revenues.csv", index_col=0)
    df_cat_expenses = pd.read_csv("df_cat_expenses.csv", index_col=0)
    cat_revenues = df_cat_revenues.values.tolist()
    cat_expenses = df_cat_expenses.values.tolist()

else:
    cat_revenues = {"Categoria": ["Salário", "Investimentos", "Comissão"]}
    cat_expenses = {
        "Categoria": ["Alimentação", "Aluguel", "Gasolina", "Saúde", "Lazer"]
    }

    df_cat_revenues = pd.DataFrame(cat_revenues, columns=["Categoria"])
    df_cat_expenses = pd.DataFrame(cat_expenses, columns=["Categoria"])
    df_cat_revenues.to_csv("df_cat_revenues.csv")
    df_cat_expenses.to_csv("df_cat_expenses.csv")
