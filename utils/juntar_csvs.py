import os
from io import StringIO

import numpy as np
import pandas as pd

# Caminho da pasta com os CSVs brutos
PASTA_BRUTA = os.path.join(os.path.dirname(__file__), "..", "data", "dados_brutos")
PASTA_BRUTA = os.path.abspath(PASTA_BRUTA)

ARQUIVO_SAIDA = os.path.join(os.path.dirname(__file__), "..", "data", "dados_climaticos_unificados.csv")
ARQUIVO_SAIDA = os.path.abspath(ARQUIVO_SAIDA)

def limpar_e_processar_arquivo(path_arquivo):
    with open(path_arquivo, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    # Localiza onde começa a parte de dados (linha que começa com PARAMETER)
    start_index = next(i for i, line in enumerate(linhas) if line.startswith("PARAMETER"))
    conteudo_limpo = "".join(linhas[start_index:])

    df_raw = pd.read_csv(StringIO(conteudo_limpo))
    df_raw.replace(-999, np.nan, inplace=True)

    # Converte para formato mensal agrupado
    df_melted = df_raw.melt(id_vars=["PARAMETER", "YEAR"],
                            value_vars=["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                                        "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
                            var_name="Month", value_name="Value")

    df_pivot = df_melted.pivot_table(index=["YEAR", "Month"],
                                     columns="PARAMETER", values="Value").reset_index()

    # Mapeia mês para número e cria coluna de data
    month_map = {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,
                 'JUL':7,'AUG':8,'SEP':9,'OCT':10,'NOV':11,'DEC':12}
    df_pivot["Month"] = df_pivot["Month"].map(month_map)
    df_pivot["Date"] = pd.to_datetime(dict(year=df_pivot["YEAR"], month=df_pivot["Month"], day=15))

    # Extrai lat/lon do nome do arquivo
    nome = os.path.basename(path_arquivo)
    partes = nome.replace(".csv", "").split("_")
    lat = float(partes[2])
    lon = float(partes[4])

    df_pivot["Latitude"] = lat
    df_pivot["Longitude"] = lon

    return df_pivot
def processar_todos_os_csvs():
    if not os.path.exists(PASTA_BRUTA):
        print(f"❌ Pasta '{PASTA_BRUTA}' não encontrada. Crie a pasta e coloque os arquivos .csv nela.")
        return

    arquivos = [f for f in os.listdir(PASTA_BRUTA) if f.endswith(".csv")]
    todos_os_dados = []

    for arquivo in arquivos:
        caminho = os.path.join(PASTA_BRUTA, arquivo)
        print(f"🔍 Processando {arquivo}")
        try:
            df = limpar_e_processar_arquivo(caminho)
            todos_os_dados.append(df)
        except Exception as e:
            print(f"⚠️ Erro ao processar {arquivo}: {e}")

    if not todos_os_dados:
        print("❌ Nenhum dado processado.")
        return

    df_final = pd.concat(todos_os_dados, ignore_index=True)
    df_final.to_csv(ARQUIVO_SAIDA, index=False)
    print(f"\n✅ Dados combinados salvos em: {ARQUIVO_SAIDA}")
    print(df_final.head())
    print(f"\n📊 Total de registros: {len(df_final)}")

if __name__ == "__main__":
    processar_todos_os_csvs()
