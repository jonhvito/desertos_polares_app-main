import requests
import pandas as pd
import numpy as np
import time
from io import StringIO

# === Parâmetros fixos ===
PARAMS = "ALLSKY_SFC_SW_DWN,WS10M,T2M"
START_YEAR = 2000
END_YEAR = 2023
COMMUNITY = "RE"
FORMAT = "CSV"

# === Grid de pontos na Antártica (ajustado para cobertura da API) ===
def gerar_grid_antartica(lat_ini=-82.5, lat_fim=-70.0, lon_ini=-180, lon_fim=180, n_lat=4, n_lon=5):
    latitudes = np.linspace(lat_ini, lat_fim, n_lat)
    longitudes = np.linspace(lon_ini, lon_fim, n_lon)
    grid = [(round(lat, 2), round(lon, 2)) for lat in latitudes for lon in longitudes]
    return grid

# === Função para baixar CSV da API para 1 ponto ===
def coletar_dados_por_ponto(lat, lon):
    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
    query = {
        "parameters": PARAMS,
        "start": START_YEAR,
        "end": END_YEAR,
        "latitude": lat,
        "longitude": lon,
        "format": FORMAT,
        "community": COMMUNITY
    }

    try:
        response = requests.get(url, params=query, timeout=15)
        if response.status_code != 200:
            print(f"❌ HTTP {response.status_code} para lat={lat}, lon={lon}")
            return None

        content = response.text
        start_index = next(i for i, line in enumerate(content.splitlines()) if line.startswith("YEAR"))
        csv_data = "\n".join(content.splitlines()[start_index:])
        df = pd.read_csv(StringIO(csv_data))

        # Agrupar por ano (média anual)
        df_grouped = df.groupby("YEAR")[["ALLSKY_SFC_SW_DWN", "WS10M", "T2M"]].mean().reset_index()
        df_grouped["Latitude"] = lat
        df_grouped["Longitude"] = lon

        return df_grouped

    except Exception as e:
        print(f"⚠️ Erro na coleta ({lat}, {lon}): {e}")
        return None

# === Loop para todos os pontos ===
def coletar_todos_os_pontos():
    grid = gerar_grid_antartica()
    all_data = []

    for idx, (lat, lon) in enumerate(grid):
        print(f"📡 {idx+1}/{len(grid)} - lat={lat}, lon={lon}")
        dados = coletar_dados_por_ponto(lat, lon)
        if dados is not None:
            all_data.append(dados)
        else:
            print(f"⚠️ Falhou em lat={lat}, lon={lon}")
        time.sleep(1.2)

    if not all_data:
        print("❌ Nenhum dado foi coletado.")
        return pd.DataFrame()

    return pd.concat(all_data, ignore_index=True)

# === Execução principal ===
if __name__ == "__main__":
    print("🚀 Coletando dados da Antártica via NASA POWER API (monthly → anual)...\n")
    df_final = coletar_todos_os_pontos()

    if df_final.empty:
        print("⚠️ Nenhum dado salvo. Verifique conexão ou limites da API.")
    else:
        path = "data/dados_climaticos_antartica.csv"
        df_final.to_csv(path, index=False)
        print(f"\n✅ Arquivo salvo com sucesso em: {path}")
        print(df_final.head())
        print(f"\n🔍 Total de registros: {len(df_final)}")
