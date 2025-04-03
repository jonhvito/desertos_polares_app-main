# ❄️ Desertificação nos Desertos Polares

![banner](https://img.shields.io/badge/streamlit-dashboard-blueviolet?style=for-the-badge)
![python](https://img.shields.io/badge/python-3.9+-brightgreen?style=for-the-badge)
![status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow?style=for-the-badge)

> Painel interativo que une ciência climática, dados energéticos e visualização intuitiva para entender o avanço da desertificação na Antártica.

---

## 🎯 Objetivo
Criar uma plataforma interativa para **visualizar, explorar e interpretar** as mudanças climáticas nos **desertos polares**, com foco na **Antártica**, analisando a **redução do gelo marinho** e o **potencial energético renovável** emergente.

---

## 🌐 Descrição
Este painel explora:

- 📉 A **diminuição do gelo marinho** ao longo das décadas
- ☀️ O **potencial solar e eólico** em diferentes regiões da Antártica
- 📊 A **sazonalidade climática** e suas tendências
- 🔁 A ligação entre mudanças climáticas e **desertificação polar**

🛰️ Dados reais da **NASA POWER** e do **NSIDC** são utilizados com base científica.

---

## 📁 Estrutura de Arquivos

```bash
├── app.py                     # Página inicial do dashboard
├── processamento.py           # Pré-processamento e carregamento dos dados
├── /pages/                    # Páginas do Streamlit
│   ├── 1_mapas_e_graficos.py      # Extensão diária e média anual do gelo
│   ├── 2_tendencias_sazonais.py   # Tendência por estação
│   ├── 3_mapa_energetico.py       # Potencial energético por coordenada
│   └── 4_energia_e_clima.py       # Séries históricas de variáveis climáticas
└── /data/                    # Arquivos CSV e imagens auxiliares
```

---

## 📊 Fontes de Dados

- **NSIDC** – [National Snow and Ice Data Center](https://nsidc.org/)
- **NASA POWER** – [Prediction Of Worldwide Energy Resources](https://power.larc.nasa.gov/)

> Os dados são tratados, limpos e organizados no script `processamento.py`.

---

## 🚀 Funcionalidades Principais

- Mapa interativo com **pontos de alto potencial energético**
- Gráficos com **faixas sazonais coloridas** para facilitar a leitura
- Destaques visuais com ícones e anotações 📌
- **Curiosidades e interpretações** para usuários leigos ou especialistas

---

## 🛠️ Tecnologias Utilizadas

- `Python 3`
- `Streamlit`
- `Plotly (Express e Graph Objects)`
- `Matplotlib`
- `Pandas`, `NumPy`

---

## 📚 Aplicações Educacionais
Este painel pode ser usado em cursos de:

- Engenharia de Energias Renováveis
- Ciências Ambientais e Meteorologia
- Geografia Física
- Comunicação Científica e Popularização da Ciência

---

## 🔮 Futuras Expansões

- Simulações de cenário com modelos preditivos (ML/IPCC)
- Exportação de gráficos e relatórios em PDF/HTML
- Sistema de alertas para eventos extremos
- Hospedagem em plataforma como Streamlit Cloud

---

## 📌 Execução

Instale as dependências e execute:

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

### 🌍 Projeto desenvolvido para fins educacionais e científicos. Licença livre para uso acadêmico.

