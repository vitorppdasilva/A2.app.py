# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Análise de Crimes no Brasil", layout="wide")

st.title("📊 Painel de Análise de Criminalidade no Brasil")
st.write(
    """
    Este aplicativo interativo apresenta dados sobre crimes no Brasil,
    com foco em crimes contra o patrimônio, permitindo filtrar por tipo de crime,
    estado e ano. A base utilizada é um conjunto fictício inspirado em dados do portal
    [dados.gov.br](https://dados.gov.br/).
    """
)

# --- BASE DE DADOS (EXEMPLO SIMPLES) ---
# Você pode substituir esse CSV por um dataset real do dados.gov.br
data = {
    "Ano": [2020, 2020, 2020, 2021, 2021, 2021, 2022, 2022, 2022],
    "Estado": ["SP", "RJ", "MG", "SP", "RJ", "MG", "SP", "RJ", "MG"],
    "TipoCrime": ["Furto", "Furto", "Furto", "Roubo", "Roubo", "Roubo", "Estelionato", "Estelionato", "Estelionato"],
    "Ocorrencias": [23000, 15000, 12000, 19000, 13000, 11000, 21000, 14000, 10000],
}
df = pd.DataFrame(data)

# --- FILTROS ---
st.sidebar.header("🔍 Filtros")
tipo_crime = st.sidebar.multiselect(
    "Selecione o tipo de crime:", options=df["TipoCrime"].unique(), default=df["TipoCrime"].unique()
)
estado = st.sidebar.multiselect(
    "Selecione o estado:", options=df["Estado"].unique(), default=df["Estado"].unique()
)
ano = st.sidebar.multiselect(
    "Selecione o ano:", options=df["Ano"].unique(), default=df["Ano"].unique()
)

# --- APLICAÇÃO DOS FILTROS ---
df_filtrado = df.query("TipoCrime == @tipo_crime & Estado == @estado & Ano == @ano")

# --- GRÁFICO 1: Crimes por Estado ---
fig1 = px.bar(
    df_filtrado,
    x="Estado",
    y="Ocorrencias",
    color="TipoCrime",
    barmode="group",
    title="Ocorrências de Crimes por Estado",
    text="Ocorrencias",
)
st.plotly_chart(fig1, use_container_width=True)

# --- GRÁFICO 2: Evolução por Ano ---
fig2 = px.line(
    df_filtrado,
    x="Ano",
    y="Ocorrencias",
    color="TipoCrime",
    markers=True,
    title="Evolução dos Crimes ao Longo dos Anos",
)
st.plotly_chart(fig2, use_container_width=True)

# --- TABELA E RESUMO ---
st.subheader("📋 Dados Filtrados")
st.dataframe(df_filtrado)

total = int(df_filtrado["Ocorrencias"].sum())
st.metric("Total de ocorrências selecionadas", total)

st.write("---")
st.caption("Desenvolvido como projeto de Direito Penal e Programação – FGV")
