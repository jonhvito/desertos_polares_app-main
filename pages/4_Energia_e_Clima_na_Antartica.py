import streamlit as st
import plotly.express as px
import pandas as pd
from utils.processamento import carregar_dados_climaticos

# Configuração inicial da página
st.set_page_config(page_title="Energia e Clima na Antártica", layout="wide")
st.title("☀️ Energia & Clima na Antártica")

# Carregar dados climáticos
df = carregar_dados_climaticos()

# Legenda visual
st.markdown("""
🎨 **Visualização de Estações**  
- 🔶 Faixas **alaranjadas** indicam o **verão antártico** (dezembro a março)  
- 🔷 Faixas **azuladas** indicam o **inverno antártico** (junho a setembro)
""")

# Função auxiliar para plotar gráficos com faixas sazonais
def plot_gradiente(df, y_col, title, y_label):
    fig = px.scatter(df, x="Date", y=y_col, color=y_col,
                     color_continuous_scale="Turbo",
                     labels={y_col: y_label, "Date": "Data"},
                     title=title)

    fig.update_traces(mode="lines+markers", line_shape="spline", marker=dict(size=4))

    anos_unicos = df["Date"].dt.year.unique()
    for ano in anos_unicos:
        fig.add_vrect(x0=f"{ano}-12-01", x1=f"{ano+1}-03-01",
                      fillcolor="rgba(255,165,0,0.2)", line_width=0)
        fig.add_vrect(x0=f"{ano}-06-01", x1=f"{ano}-09-01",
                      fillcolor="rgba(135,206,250,0.4)", line_width=0)

    fig.update_layout(height=400, margin=dict(t=40, l=30, r=30, b=40))
    return fig

# Gráfico Radiação Solar
st.subheader("☀️ Radiação Solar Mensal (kWh/m²/dia)")
st.plotly_chart(plot_gradiente(df, "ALLSKY_SFC_SW_DWN",
                               "Radiação Solar Global Incidente", "kWh/m²/dia"), use_container_width=True)

# Gráfico Vento
st.subheader("💨 Velocidade Média do Vento a 10 metros (m/s)")
st.plotly_chart(plot_gradiente(df, "WS10M",
                               "Vento Médio Mensal", "m/s"), use_container_width=True)

# Gráfico Temperatura
st.subheader("🌡️ Temperatura Média Mensal (°C)")
st.plotly_chart(plot_gradiente(df, "T2M",
                               "Temperatura Média Mensal", "°C"), use_container_width=True)

# Imagem da Estação McMurdo
st.markdown("### 📍 Estação McMurdo – Local de Referência dos Dados")
st.image("data/maxresdefault.jpg", caption="Estação McMurdo, Antártica. Latitude: -77.85° | Longitude: 166.67°", use_column_width=True)

# Tabela comparativa recente
st.markdown("### 📊 Valores recentes comparados (ano de 2023)")
st.dataframe(
    df[["Date", "ALLSKY_SFC_SW_DWN", "WS10M", "T2M"]].tail(12).rename(columns={
        "ALLSKY_SFC_SW_DWN": "Radiação (kWh/m²/dia)",
        "WS10M": "Vento (m/s)",
        "T2M": "Temp. (°C)"
    }), use_container_width=True
)

# Resumo visual
st.markdown("""
---
### ✅ O que aprendemos nesta seção:
- ☀️ **Verões têm alta radiação** → aumentam o derretimento superficial  
- 💨 **Ventos constantes** → potencial para energia eólica  
- 🌡️ **Temperatura média sobe lentamente** → impacto mesmo abaixo de 0°C  
- 📉 **Clima extremo acelera o processo de desertificação polar**

📌 Esses dados serão base para **simular o futuro** da Antártica na próxima aba.
""")

# Curiosidades sobre o clima da Antártica
with st.expander("🧊 Curiosidades sobre clima e estações na Antártica"):
    st.markdown("""
### 🌎 Inversão de Estações

A **Antártica está no hemisfério sul**, assim como o Brasil.  
Por isso, suas estações do ano são **opostas às do hemisfério norte**:

| Estação | Meses na Antártica |
|---------|--------------------|
| ☀️ **Verão**   | Dezembro – Março     |
| ❄️ **Inverno** | Junho – Setembro     |

🔄 Isso é o oposto da Europa, América do Norte e Ásia!

---

### 📌 Outras Curiosidades Relevantes:
- 🌡️ **Temperaturas na Antártica** podem variar de **-60°C no inverno** até **0°C no verão**.
- ☀️ Durante o verão, há **dias com sol 24h** (sol da meia-noite).
- 🌘 Durante o inverno, há **meses sem nascer do sol** — escuridão total.
- 🧬 A Estação McMurdo é a **maior base de pesquisa** da Antártica, com mais de 1.000 cientistas no verão.
- 🧊 A Antártica é considerada um **“deserto frio”** por causa da **baixa umidade e quase nenhuma precipitação**.

---

📚 **Fato científico importante:**  
Mesmo abaixo de 0°C, o gelo superficial pode derreter devido ao aumento da radiação solar e ventos quentes, contribuindo para a **desertificação polar**.
""")