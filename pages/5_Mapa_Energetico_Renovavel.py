import streamlit as st
import pandas as pd
import plotly.express as px
from utils.processamento import calcular_media_anual_por_ponto

st.set_page_config(page_title="Mapa Energético Renovável", layout="wide")
st.title("📍 Mapa Energético – Pontos com Potencial de Energia Renovável")

@st.cache_data
def load_data():
    df = pd.read_csv("data/dados_climaticos_unificados.csv")
    df["ALLSKY_SFC_SW_DWN"] = pd.to_numeric(df["ALLSKY_SFC_SW_DWN"], errors="coerce")
    df["WS10M"] = pd.to_numeric(df["WS10M"], errors="coerce")
    return df

# Carregar dados
df = load_data()

# Seleção de variáveis
variaveis_energia = {
    "Energia Solar (Irradiação) [kWh/m²/dia]": "ALLSKY_SFC_SW_DWN",
    "Energia Eólica (Velocidade do Vento) [m/s]": "WS10M"
}

col1, col2 = st.columns(2)
with col1:
    variavel_label = st.selectbox("🔧 Variável climática:", list(variaveis_energia.keys()))
    variavel = variaveis_energia[variavel_label]

with col2:
    anos_disponiveis = sorted(df["YEAR"].unique())
    ano = st.selectbox("📅 Ano:", anos_disponiveis, index=len(anos_disponiveis) - 1)

# Calcular média anual por ponto
df_media_anual = calcular_media_anual_por_ponto(df, variavel)
df_media_anual[variavel] = df_media_anual[variavel].round(2)

# Filtrar ano selecionado
df_filtrado = df_media_anual[df_media_anual["YEAR"] == ano].copy()

# Critérios de viabilidade energética
criterios_viabilidade = {
    "ALLSKY_SFC_SW_DWN": 2.0,
    "WS10M": 7.0
}

# Aplicar critério de destaque
df_filtrado["Destaque"] = df_filtrado[variavel] >= criterios_viabilidade[variavel]

# Exibir resumo
st.write(f"🔍 Média anual de {variavel_label} em {ano}:")
st.write(f"- Mínimo: {df_filtrado[variavel].min():.2f}")
st.write(f"- Máximo: {df_filtrado[variavel].max():.2f}")
st.write(f"- Pontos com alto potencial: {df_filtrado['Destaque'].sum()}/{len(df_filtrado)}")

# Gerar mapa
fig = px.scatter_geo(
    df_filtrado,
    lat="Latitude",
    lon="Longitude",
    color=variavel,
    color_continuous_scale="viridis",
    projection="orthographic",
    title=f"{variavel_label} em {ano} (★ = Alta Viabilidade)",
    template="plotly_dark",
    labels={variavel: variavel_label},
    hover_data={variavel: ':.2f'}
)

# Adicionar destaque visual
if df_filtrado["Destaque"].any():
    pontos_destaque = df_filtrado[df_filtrado["Destaque"]]
    fig.add_scattergeo(
        lat=pontos_destaque["Latitude"],
        lon=pontos_destaque["Longitude"],
        mode="markers",
        marker=dict(color="gold", size=12, symbol="star"),
        name="Alta Viabilidade"
    )
else:
    st.warning("⚠️ Nenhum ponto atingiu o critério de destaque para este ano!")

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

# Explicação interpretativa
with st.expander("🧭 Como interpretar o mapa?"):
    st.markdown(f"""
- Cada ponto indica uma localização média anual na Antártica.
- As cores mostram a intensidade média anual de **{variavel_label.lower()}**.
- Pontos com ★ (estrela dourada) destacam áreas com alta viabilidade energética.

### Critérios de Viabilidade

**Energia Eólica (m/s):**

| Velocidade | Avaliação |
|------------|-----------|
| >8,0       | Excelente |
| 7,0–8,0    | Muito Boa |
| 6,0–7,0    | Boa       |
| 5,0–6,0    | Moderada  |
| <5,0       | Marginal  |

**Energia Solar (kWh/m²/dia):**

| Irradiação | Avaliação |
|------------|-----------|
| >5,0       | Excelente |
| 4,0–5,0    | Boa       |
| 3,0–4,0    | Moderada  |
| 2,0–3,0    | Marginal  |
| <2,0       | Pouco viável |

> Ventos na Antártica frequentemente superam 7 m/s (alta viabilidade), enquanto a radiação solar é geralmente marginal.
""")

with st.expander("📁 Fonte dos dados"):
    st.markdown("""
- [NASA POWER Data Access Viewer](https://power.larc.nasa.gov/data-access-viewer/)
- Parâmetros: `ALLSKY_SFC_SW_DWN`, `WS10M`, `T2M`, entre outros.
- Dados mensais agregados (2000–2023).
""")
