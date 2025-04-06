import streamlit as st

# Configurações iniciais
st.set_page_config(page_title="Introdução", layout="wide")
st.title("🌐 Desertificação nos Desertos Polares")
st.markdown("### Bem-vindo à aplicação interativa sobre mudanças climáticas na Antártica!")


# Descrição geral
st.markdown("""
Este projeto foi desenvolvido como parte do curso de **Engenharia de Energias Renováveis**, com foco em compreender e visualizar o processo de **desertificação polar**, especialmente na região da **Antártica**.

Através de dados climáticos e energéticos reais (NASA POWER, NSIDC), esta plataforma oferece uma análise detalhada das transformações ambientais que afetam os desertos frios do planeta.
""")

# Estrutura do app
st.markdown("### 🔍 O que você encontrará nesta aplicação:")

st.markdown("""
            
- 📅 **Evolução Histórica do Gelo**


- **📈 Tendências Sazonais:**  
  -Análise da extensão do gelo marinho ao longo das décadas, separada por estações do ano.
  

- **📊 Energia e Clima:**  
  -Gráficos interativos com dados de radiação solar, ventos, temperatura e outros elementos climáticos.


- **📍 Mapa Energético:**  
  -Mapa geográfico com pontos de coleta de dados, destacando locais com potencial energético renovável.
  

- **🧭 Comparação Energética:**  
  -Comparação direta entre dois anos para qualquer variável climática ou energética.
  
  
  
- 🔮 **Simulador de Cenário Futuro**:  
  - Ferramenta interativa para visualizar possíveis cenários futuros com base em alterações climáticas previstas.


""")

# Dados e fontes
st.markdown("### 📁 Fontes de dados:")

st.markdown("""
- NASA POWER Data Viewer – Parâmetros meteorológicos e de radiação solar  
- NSIDC – Extensão do gelo marinho  
- Dados organizados mensalmente (2000–2023)
""")

# Chamada final
st.info("Utilize o menu lateral à esquerda para navegar pelas seções. **Boa exploração!**")
