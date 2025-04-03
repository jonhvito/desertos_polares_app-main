import streamlit as st
import pandas as pd
import plotly.express as px
from utils.processamento import calcular_media_anual_por_ponto, media_anual, carregar_dados

# Configuração inicial
def setup_page():
    st.set_page_config(page_title="Simulador de Cenário Futuro", layout="wide")
    st.title("🔮 Simulador de Cenário Futuro na Antártica")

# Carregar dados climáticos
@st.cache_data
def load_climate_data():
    df = pd.read_csv("data/dados_climaticos_unificados.csv")
    numeric_cols = ["ALLSKY_SFC_SW_DWN", "WS10M", "T2M"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    return df

# Interface de simulação
def simulation_controls():
    st.sidebar.header("🛠️ Ajuste seu cenário")
    irradiancia_delta = st.sidebar.slider("☀️ Variação na Irradiação Solar (kWh/m²/dia)", -1.0, 2.0, 0.5, 0.1)
    vento_delta = st.sidebar.slider("💨 Variação na Velocidade do Vento (%)", -30, 30, 0, 5)
    temp_delta = st.sidebar.slider("📈 Aumento de Temperatura Média (°C)", 0.0, 5.0, 1.5, 0.1)
    return irradiancia_delta, vento_delta, temp_delta

# Preparar dados simulados
def prepare_simulation(df_clima, irradiancia_delta, vento_delta, temp_delta):
    ano_base = df_clima["YEAR"].max()

    df_solar = calcular_media_anual_por_ponto(df_clima, "ALLSKY_SFC_SW_DWN")
    df_vento = calcular_media_anual_por_ponto(df_clima, "WS10M")
    df_temp = calcular_media_anual_por_ponto(df_clima, "T2M")

    df_sim = df_solar.merge(df_vento, on=["Latitude", "Longitude", "YEAR"])
    df_sim = df_sim.merge(df_temp, on=["Latitude", "Longitude", "YEAR"])

    df_sim["Solar_Sim"] = (df_sim["ALLSKY_SFC_SW_DWN"] + irradiancia_delta).round(2)
    df_sim["Vento_Sim"] = (df_sim["WS10M"] * (1 + vento_delta / 100)).round(2)
    df_sim["Temp_Sim"] = (df_sim["T2M"] + temp_delta).round(2)

    return df_sim, ano_base

# Função para plotar mapas simulados
def plot_simulation_map(df, column, title, color_scale):
    fig = px.scatter_geo(
        df,
        lat="Latitude", lon="Longitude", color=column,
        color_continuous_scale=color_scale,
        projection="orthographic",
        title=title,
        template="plotly_dark",
        labels={column: title}
    )
    fig.update_geos(projection_rotation=dict(lat=-90))
    st.plotly_chart(fig, use_container_width=True)

# Simular extensão do gelo marinho
def gelo_projection(temp_delta, df_gelo):
    TAXA_QUEDA_POR_GRAU = 0.25
    df_anual = media_anual(df_gelo)
    base_gelo = df_anual[df_anual["Year"] == df_anual["Year"].max()]["Extent"].values[0]
    gelo_proj = base_gelo - (TAXA_QUEDA_POR_GRAU * temp_delta)

    st.subheader("🧊 Projeção de Extensão de Gelo Marinho")
    col1, col2 = st.columns(2)
    col1.metric(label="Extensão Atual (estimada)", value=f"{base_gelo:.2f} mi km²")
    col2.metric(label=f"Extensão Projeta com +{temp_delta:.1f}°C", value=f"{gelo_proj:.2f} mi km²",
                delta=f"{gelo_proj - base_gelo:.2f} mi km²")

# Executar aplicação
setup_page()
df_clima = load_climate_data()
irradiancia_delta, vento_delta, temp_delta = simulation_controls()
df_sim, ano_base = prepare_simulation(df_clima, irradiancia_delta, vento_delta, temp_delta)

# Plotagem dos resultados
st.subheader("☀️ Irradiação Solar Simulada")
plot_simulation_map(df_sim, "Solar_Sim", f"Irradiação Solar Simulada (+{irradiancia_delta} kWh/m²/dia)", "YlOrRd")

st.subheader("💨 Velocidade do Vento Simulada")
plot_simulation_map(df_sim, "Vento_Sim", f"Velocidade do Vento Simulada ({vento_delta:+}%)", "Blues")

st.subheader("🌡️ Temperatura Média Simulada")
plot_simulation_map(df_sim, "Temp_Sim", f"Temperatura Média Simulada (+{temp_delta:.1f} °C)", "thermal")

# Projeção do gelo
df_gelo = carregar_dados()
gelo_projection(temp_delta, df_gelo)

# Explicação sobre a simulação
with st.expander("📘 Como funciona esta simulação?"):
    st.markdown("""
- Os dados simulados são baseados em projeções de aumento de temperatura, irradiação e vento.
- A projeção da extensão de gelo assume uma perda média de **0.25 milhão km² por °C** adicional, baseada na tendência histórica (1979–2023).
- Este simulador é **educacional** e não substitui modelos climáticos completos.
""")