import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- CONFIGURAÇÃO BÁSICA ----------------
st.set_page_config(
    page_title="Painel de Criminalidade – Minas Gerais (dados.mg.gov.br)",
    layout="wide"
)

st.title("📊 Painel de Ocorrências Criminais – Minas Gerais")
st.write(
    """
    Este painel utiliza dados oficiais de **crimes violentos em Minas Gerais (2023)**,
    disponibilizados no Portal de Dados Abertos do Governo de Minas Gerais (**dados.mg.gov.br**).
    O objetivo é aproximar o estudo de **Direito Penal** da análise empírica de dados reais de criminalidade.
    """
)

# ---------------- CARREGAMENTO DOS DADOS ----------------
@st.cache_data
def carregar_dados():
    # Lê o arquivo Excel real do dados.mg.gov.br
    df = pd.read_excel("crimes_violentos_2023.xlsx")

    # Renomeia colunas principais (ajuste se o nome no Excel for diferente)
    df = df.rename(columns={
        "Ano": "Ano",
        "Município": "Municipio",
        "Natureza": "TipoCrime",
        "Ocorrências": "Ocorrencias"
    })

    # Remove dados vazios e ajusta tipos
    df = df.dropna(subset=["Ano", "Municipio", "TipoCrime", "Ocorrencias"])
    df["Ano"] = df["Ano"].astype(int)
    df["Ocorrencias"] = df["Ocorrencias"].astype(int)

    return df

df = carregar_dados()

# Link oficial da fonte
st.markdown(
    "🔗 **Fonte oficial dos dados:** "
    "[Crimes Violentos 2023 – Governo de Minas Gerais (dados.mg.gov.br)]"
    "(https://dados.mg.gov.br/dataset/crimes-violentos/resource/38229449-86c1-4240-b48d-d4f680d661c4)"
)

# ---------------- FILTROS ----------------
st.sidebar.header("🔍 Filtros")

anos = st.sidebar.multiselect(
    "Ano",
    options=sorted(df["Ano"].unique()),
    default=sorted(df["Ano"].unique())
)

tipos = st.sidebar.multiselect(
    "Tipo de crime",
    options=sorted(df["TipoCrime"].unique()),
    default=sorted(df["TipoCrime"].unique())[:5]
)

municipios = st.sidebar.multiselect(
    "Município",
    options=sorted(df["Municipio"].unique()),
    default=None
)

# Aplica filtros
df_filtrado = df.copy()
if anos:
    df_filtrado = df_filtrado[df_filtrado["Ano"].isin(anos)]
if tipos:
    df_filtrado = df_filtrado[df_filtrado["TipoCrime"].isin(tipos)]
if municipios:
    df_filtrado = df_filtrado[df_filtrado["Municipio"].isin(municipios)]

# ---------------- INDICADORES ----------------
col1, col2, col3 = st.columns(3)
total_ocorrencias = int(df_filtrado["Ocorrencias"].sum())
total_municipios = df_filtrado["Municipio"].nunique()
total_tipos = df_filtrado["TipoCrime"].nunique()

col1.metric("Total de ocorrências", f"{total_ocorrencias:,}".replace(",", "."))
col2.metric("Municípios contemplados", total_municipios)
col3.metric("Tipos de crime analisados", total_tipos)

st.write("---")

# ---------------- GRÁFICO 1 ----------------
st.subheader("📍 Ocorrências por município")
df_mun = (
    df_filtrado.groupby(["Municipio"], as_index=False)["Ocorrencias"]
    .sum()
    .sort_values("Ocorrencias", ascending=False)
    .head(20)
)

fig_mun = px.bar(
    df_mun,
    x="Municipio",
    y="Ocorrencias",
    title="Top 20 municípios com mais ocorrências",
    labels={"Municipio": "Município", "Ocorrencias": "Nº de ocorrências"},
)
fig_mun.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_mun, use_container_width=True)

# ---------------- GRÁFICO 2 ----------------
st.subheader("📈 Evolução das ocorrências por tipo de crime")
df_ano_tipo = (
    df_filtrado.groupby(["Ano", "TipoCrime"], as_index=False)["Ocorrencias"]
    .sum()
)
fig_ano = px.line(
    df_ano_tipo,
    x="Ano",
    y="Ocorrencias",
    color="TipoCrime",
    markers=True,
    labels={"Ano": "Ano", "Ocorrencias": "Nº de ocorrências", "TipoCrime": "Tipo de crime"},
)
st.plotly_chart(fig_ano, use_container_width=True)

# ---------------- TABELA FINAL ----------------
st.subheader("📋 Dados detalhados (após filtros)")
st.dataframe(df_filtrado.sort_values(["Ano", "Municipio", "TipoCrime"]))

st.write("---")
st.caption(
    "Aplicativo desenvolvido para a disciplina de Programação Aplicada, "
    "utilizando dados oficiais do Governo de Minas Gerais (dados.mg.gov.br) "
    "e relacionando-os com temas de Direito Penal."
)
