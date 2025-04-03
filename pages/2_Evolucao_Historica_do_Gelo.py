import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from utils.processamento import carregar_dados, media_anual

# Configuração inicial da página
st.set_page_config(page_title="Evolução Histórica do Gelo", layout="wide")
st.title("📈 Evolução Histórica do Gelo")

# Funções auxiliares

def plot_extensao_diaria(df):
    fig, ax = plt.subplots(figsize=(13, 4))
    ax.plot(df["Date"], df["Extent"], color="navy", linewidth=0.5)

    anos_unicos = df["Date"].dt.year.unique()
    ano_min = anos_unicos.min()

    for year in anos_unicos:
        ax.axvspan(pd.Timestamp(year, 1, 1), pd.Timestamp(year, 3, 31),
                   color='#d95f02', alpha=0.2, label="Verão" if year == ano_min else None)
        ax.axvspan(pd.Timestamp(year, 7, 1), pd.Timestamp(year, 9, 30),
                   color='#2166ac', alpha=0.2, label="Inverno" if year == ano_min else None)

    # Anotações
    ax.annotate("↓ Verão: derretimento (mínimo de gelo)",
                xy=(pd.Timestamp("2010-02-15"), 4.5),
                xytext=(pd.Timestamp("2010-01-01"), 6.5),
                arrowprops=dict(arrowstyle="->", color="#d95f02"),
                fontsize=9, color="#d95f02", weight="bold")

    ax.annotate("↑ Inverno: congelamento (máximo de gelo)",
                xy=(pd.Timestamp("2010-08-15"), 15),
                xytext=(pd.Timestamp("2010-06-01"), 13),
                arrowprops=dict(arrowstyle="->", color="#2166ac"),
                fontsize=9, color="#2166ac", weight="bold")

    ax.set(xlabel="Ano", ylabel="Extensão (milhões km²)",
           title="Extensão Diária do Gelo Marinho com Análise Sazonal (1979–2024)")
    ax.grid(True)
    ax.legend(loc="upper right")

    st.pyplot(fig)

def plot_media_anual(df_ano):
    fig = px.line(df_ano, x="Year", y="Extent", markers=True,
                  labels={"Extent": "Extensão média (milhões km²)", "Year": "Ano"},
                  title="Média Anual da Extensão do Gelo Marinho")
    st.plotly_chart(fig, use_container_width=True)

# Carregar e processar dados
df = carregar_dados()
df_ano = media_anual(df)

# Gráfico de linha da extensão diária
st.subheader("Extensão Diária do Gelo Marinho com Análise Sazonal (1979–2024)")
plot_extensao_diaria(df)

st.markdown("""
🔍 **O que esse gráfico mostra:**  
Este gráfico exibe a extensão diária do gelo marinho na Antártica de 1979 a 2024.  
As **faixas azuis** indicam o **inverno (julho a setembro)** — período de **máximo congelamento**.  
As **faixas laranjas** indicam o **verão (janeiro a março)** — período de **derretimento máximo**.  
As setas no gráfico ajudam a identificar claramente os picos e vales sazonais.
""")

# Gráfico interativo da média anual
st.subheader("Média Anual da Extensão do Gelo Marinho")
plot_media_anual(df_ano)

st.markdown("""
📊 **O que esse gráfico mostra:**  
Este gráfico mostra a média anual da extensão do gelo em milhões de km².  
É possível observar uma **tendência de queda** ao longo das décadas, especialmente **após 2016**, reforçando a tese de alterações climáticas.
""")

# Bloco explicativo interativo
st.markdown("---")
with st.expander("🧠 Ajuda para interpretar os gráficos"):
    st.markdown("""
### 📘 Como interpretar os gráficos:

#### 📈 Extensão Diária do Gelo Marinho

- Exibe a **extensão diária do gelo** registrada de 1979 a 2024.
- Representa valores **diários reais**, não médias.
- A forma ondulada mostra o **ciclo sazonal**: aumento no inverno, derretimento no verão.
- **Faixas azuis** destacam **máximo congelamento** (julho a setembro).
- **Faixas laranjas** mostram **mínimo de gelo** (janeiro a março).

🧠 **Nota:** O eixo X representa anos contínuos, com marcadores a cada 10 anos para facilitar visualização.

#### 📊 Extensão Média Anual

- Exibe a **média anual** da extensão do gelo.
- Evidencia **tendências de longo prazo**.
- Queda acentuada após 2016 indica impacto potencial das mudanças climáticas.

---

🌍 **A Antártica funciona como um espelho climático:**  
menos gelo → mais absorção de calor → mais aquecimento → mais desertificação.
    """)