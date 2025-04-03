import streamlit as st
import pandas as pd
import plotly.express as px
from utils.processamento import calcular_media_anual_por_ponto

# Configuração inicial
def setup_page():
    st.set_page_config(page_title="Comparativo Climático e Energético", layout="wide")
    st.title("🌍🔄 Comparativo Climático e Energético entre Anos")

@st.cache_data
def load_data():
    df = pd.read_csv("data/dados_climaticos_unificados.csv")
    cols_numeric = ["ALLSKY_SFC_SW_DWN", "WS10M", "T2M", "T2M_MAX", "T2M_MIN", "RH2M", "PS"]
    df[cols_numeric] = df[cols_numeric].apply(pd.to_numeric, errors="coerce")
    return df

# Interface de seleção
def select_interface(df, variaveis_energia):
    col1, col2 = st.columns(2)

    with col1:
        variavel_label = st.selectbox("🔧 Variável climática:", list(variaveis_energia.keys()))
        variavel = variaveis_energia[variavel_label]

    with col2:
        anos = sorted(df["YEAR"].unique())
        ano1 = st.selectbox("📅 Ano de referência:", anos, index=len(anos)-2)
        ano2 = st.selectbox("📅 Ano de comparação:", anos, index=len(anos)-1)

    return variavel_label, variavel, ano1, ano2

# Preparar dados para comparação
def preparar_comparacao(df, variavel, variavel_label, ano1, ano2):
    df_media = calcular_media_anual_por_ponto(df, variavel)
    df_media[variavel] = df_media[variavel].round(2)

    df_v1 = df_media[df_media["YEAR"] == ano1].rename(columns={variavel: f"{variavel_label} - {ano1}"})
    df_v2 = df_media[df_media["YEAR"] == ano2].rename(columns={variavel: f"{variavel_label} - {ano2}"})

    df_comp = pd.merge(df_v1, df_v2, on=["Latitude", "Longitude"], how="inner")
    df_comp["Diferença"] = df_comp[f"{variavel_label} - {ano2}"] - df_comp[f"{variavel_label} - {ano1}"]

    media_ano1 = df_comp[f"{variavel_label} - {ano1}"].mean()
    media_ano2 = df_comp[f"{variavel_label} - {ano2}"].mean()
    diferenca_media = media_ano2 - media_ano1

    return df_comp, media_ano1, media_ano2, diferenca_media

# Plotar mapa comparativo
def plotar_mapa(df_comp, variavel_label, ano1, ano2):
    fig = px.scatter_geo(
        df_comp,
        lat="Latitude",
        lon="Longitude",
        color="Diferença",
        color_continuous_scale="RdBu",
        template="plotly_dark",
        title=f"Variação espacial de {variavel_label}",
        hover_data={
            f"{variavel_label} - {ano1}": ':.2f',
            f"{variavel_label} - {ano2}": ':.2f',
            "Diferença": ':.2f'
        },
        projection="orthographic",
        labels={"Diferença": f"Δ {variavel_label}"}
    )

    fig.update_layout(
        geo=dict(
            projection=dict(type="orthographic", rotation=dict(lat=-90)),
            showland=True,
            landcolor="white",
            showocean=True,
            oceancolor="lightblue"
        ),
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)

# Execução principal do app
setup_page()
df = load_data()

variaveis_energia = {
    "☀️ Energia Solar (Irradiação) [kWh/m²/dia]": "ALLSKY_SFC_SW_DWN",
    "💨 Energia Eólica (Velocidade do Vento) [m/s]": "WS10M",
    "🌡️ Temperatura Média (°C)": "T2M",
    "🌡️ Temperatura Máxima (°C)": "T2M_MAX",
    "🌡️ Temperatura Mínima (°C)": "T2M_MIN",
    "💧 Umidade Relativa (%)": "RH2M",
    "🔽 Pressão (hPa)": "PS"
}

variavel_label, variavel, ano1, ano2 = select_interface(df, variaveis_energia)
df_comp, media_ano1, media_ano2, diferenca_media = preparar_comparacao(df, variavel, variavel_label, ano1, ano2)

col_map, col_info = st.columns([3, 1])

with col_map:
    st.write(f"### Mudança em {variavel_label} de {ano1} para {ano2}")
    plotar_mapa(df_comp, variavel_label, ano1, ano2)

with col_info:
    st.markdown("### 📈 Comparação Global:")
    st.markdown(f"**{ano1}** – média: `{media_ano1:.2f}`")
    st.markdown(f"**{ano2}** – média: `{media_ano2:.2f}`")
    st.markdown(f"**Δ Diferença:** `{diferenca_media:.2f}`")

# Interpretação
with st.expander("🧭 Como interpretar o mapa?"):
    st.markdown(f"""
- O mapa mostra a diferença média anual de **{variavel_label.lower()}** entre **{ano1}** e **{ano2}**.
- Cores azuladas indicam redução e avermelhadas indicam aumento.
- Útil para entender padrões climáticos e energéticos ao longo do tempo.
""")

# Explicação das variáveis
with st.expander("📘 O que representa cada variável?"):
    st.markdown("""
- ☀️ **Energia Solar** – Potencial fotovoltaico (kWh/m²/dia).
- 💨 **Energia Eólica** – Velocidade média do vento (m/s).
- 🌡️ **Temperaturas** – Médias e extremos diários (°C).
- 💧 **Umidade Relativa** – Vapor d’água no ar (%).
- 🔽 **Pressão** – Pressão atmosférica (hPa).
""")
