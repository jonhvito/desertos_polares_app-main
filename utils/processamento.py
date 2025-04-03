import pandas as pd
import numpy as np
from io import StringIO

# ========= DADOS DE GELO MARINHO (NSIDC) ========= #

DATA_PATH = "data/N_seaice_extent_daily_v3.0.csv"

def carregar_dados(caminho=DATA_PATH):
    df = pd.read_csv(caminho)
    df = df[1:].copy()  # remove linha de cabeçalho extra
    df.columns = ["Year", "Month", "Day", "Extent", "Missing", "Source"]
    df["Year"] = df["Year"].astype(int)
    df["Month"] = df["Month"].astype(int)
    df["Day"] = df["Day"].astype(int)
    df["Extent"] = pd.to_numeric(df["Extent"], errors="coerce")
    df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
    df = df[df["Year"] <= 2024]
    df.sort_values("Date", inplace=True)
    return df.reset_index(drop=True)

def media_anual(df):
    df["Year"] = df["Date"].dt.year
    return df.groupby("Year")["Extent"].mean().reset_index()

def media_mensal(df):
    df["Month"] = df["Date"].dt.month
    return df.groupby("Month")["Extent"].mean().reset_index()

def media_por_estacao(df):
    df["Month"] = df["Date"].dt.month
    df["Estacao"] = df["Month"].apply(classificar_estacao)
    return df.groupby("Estacao")["Extent"].mean().reindex(["Verão", "Outono", "Inverno", "Primavera"])

def tendencia_estacional(df):
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Estacao"] = df["Month"].apply(classificar_estacao)
    return df.groupby(["Year", "Estacao"])["Extent"].mean().reset_index()

def classificar_estacao(mes):
    if mes in [12, 1, 2]:
        return "Verão"
    elif mes in [3, 4, 5]:
        return "Outono"
    elif mes in [6, 7, 8]:
        return "Inverno"
    else:
        return "Primavera"

# ========= DADOS CLIMÁTICOS (NASA POWER) ========= #

def carregar_dados_climaticos(path='data/nasa_power_antarctica.csv'):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start_index = next(i for i, line in enumerate(lines) if line.startswith("PARAMETER"))
    clean_lines = lines[start_index:]
    df_raw = pd.read_csv(StringIO("".join(clean_lines)))
    df_raw.replace(-999, np.nan, inplace=True)

    df_melted = df_raw.melt(id_vars=["PARAMETER", "YEAR"],
                            value_vars=["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                                         "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
                            var_name="Month", value_name="Value")

    df_pivot = df_melted.pivot_table(index=["YEAR", "Month"],
                                     columns="PARAMETER", values="Value").reset_index()

    df_pivot.columns.name = None
    df_pivot.rename(columns={"YEAR": "Year", "Month": "Month"}, inplace=True)

    month_map = {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,
                 'JUL':7,'AUG':8,'SEP':9,'OCT':10,'NOV':11,'DEC':12}
    df_pivot["Month"] = df_pivot["Month"].map(month_map)
    df_pivot["Date"] = pd.to_datetime(dict(year=df_pivot["Year"], month=df_pivot["Month"], day=15))

    return df_pivot

# ========= NOVA FUNÇÃO: MÉDIA ANUAL POR PONTO ========= #

def calcular_media_anual_por_ponto(df, variavel):
    """
    Retorna a média anual da variável selecionada agrupada por Latitude e Longitude.
    """
    df[variavel] = pd.to_numeric(df[variavel], errors="coerce")  # garante formato numérico
    return (
        df.groupby(["YEAR", "Latitude", "Longitude"], as_index=False)
          .agg({variavel: "mean"})
    )
