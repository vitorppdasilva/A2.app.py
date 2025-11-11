import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- CONFIG BÁSICA ----------------
st.set_page_config(
    page_title="Painel de Criminalidade – RS (dados.gov.br)",
    layout="wide"
)

st.title("📊 Painel de Ocorrências Criminais – Rio Grande do Sul")
st.write(
    """
    Este painel utiliza dados oficiais de **ocorrências criminais no estado do Rio Grande do Sul**,
    disponibilizados no Portal Brasileiro de Dados Abertos (**dados.gov.br**).
    A ideia é aproximar o estudo de **Direito Penal** da análise empírica de dados de criminalidade.
    """
)

# ---------------- CARREGAMENTO DOS DADOS ----------------
@st.cache_data
def carregar_dados():
    """
    Lê o arquivo CSV baixado do dados.gov.br e padroniza os nomes das colunas.
    IMPORTANTE: se os nomes das colunas do seu CSV forem diferentes,
    basta ajustar o dicionário do .rename() abaixo.
    """
    df = pd.read_csv("ocorrencias_rs.csv", sep=";", encoding="latin1")

    # AJUSTE OS NOMES AQUI CONFORME O SEU ARQUIVO
    df = df.rename(columns={
        "ANO": "Ano",
        "MUNICIPIO": "Municipio",
        "NATUREZA": "TipoCrime",
        "OCORRENCIAS": "Ocorrencias"
    })

    # remove linhas com dados faltantes básicos
    df = df.dropna(subset=["Ano", "Municipio", "TipoCrime", "Ocorrencias"])

    # garante tipos corretos
    df["Ano"] = df["Ano"].astype(int)
    df["Ocorrencias"] = df["Ocorrencias"].astype(int)

    return df

df = carregar_dados()

st.markdown(
    "🔗 **Fonte oficial dos dados:** "
    "[Ocorrências criminais no estado do Rio Grande do Sul – dados.gov.br]"
    "(https://dados.gov.br/dados/conjuntos-dados/ocorrencias-criminais-no-estado-do-rio-grande-do-sul)"
)

# ---------------- FILTROS (BARRA LATERAL) ----------------
st.sidebar.header("🔍 Filtros")

anos = st.sidebar.multiselect(
    "Ano",
    options=sorted(df["Ano"].unique()),
    default=sorted(df["Ano"].unique())[-5:]  # últimos 5 anos da série
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

df_filtrado = df.copy()
if anos:
    df_filtrado = df_filtrado[df_filtrado["Ano"].isin(anos)]
if tipos:
    df_filtrado = df_filtrado[df_filtrado["TipoCrime"].isin(tipos)]
if municipios:
    df_filtrado = df_filtrado[df_filtrado["Municipio"].isin(municipios)]

# ---------------- INDICADORES RESUMO ----------------
col1, col2, col3 = st.columns(3)

total_ocorrencias = int(df_filtrado["Ocorrencias"].sum())
total_municipios = df_filtrado["Municipio"].nunique()
total_tipos = df_filtrado["TipoCrime"].nunique()

col1.metric("Total de ocorrências no recorte", f"{total_ocorrencias:,}".replace(",", "."))
col2.metric("Municípios contemplados", total_municipios)
col3.metric("Tipos de crime analisados", total_tipos)

st.write("---")

# ---------------- GRÁFICO 1 – CRIMES POR MUNICÍPIO ----------------
st.subheader("📍 Ocorrências por município")

df_mun = (
    df_filtrado.groupby(["Municipio"], as_index=False)["Ocorrencias"]
    .sum()
    .sort_values("Ocorrencias", ascending=False)
    .head(20)  # top 20 para não poluir
)

fig_mun = px.bar(
    df_mun,
    x="Municipio",
    y="Ocorrencias",
    title="Top 20 municípios por número de ocorrências",
    labels={"Municipio": "Município", "Ocorrencias": "Nº de ocorrências"},
)
fig_mun.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_mun, use_container_width=True)

# ---------------- GRÁFICO 2 – EVOLUÇÃO TEMPORAL ----------------
st.subheader("📈 Evolução das ocorrências por ano e tipo de crime")

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

# ---------------- TABELA DETALHADA ----------------
st.subheader("📋 Dados detalhados (após filtros)")
st.dataframe(df_filtrado.sort_values(["Ano", "Municipio", "TipoCrime"]))

st.write("---")
st.caption(
    "Aplicativo desenvolvido para a disciplina de Programação, utilizando dados oficiais "
    "de ocorrências criminais (dados.gov.br) e relacionando-os com temas de Direito Penal."
)
