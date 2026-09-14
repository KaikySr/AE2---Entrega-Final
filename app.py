"""
app.py
------------------------------------------------------------
Painel de Inclusao Digital - Sitio Cercado (Curitiba/PR)
Atividade Extensionista II - CST em Ciencia de Dados (UNINTER)

Aplicativo web (Streamlit) que le as respostas de um questionario
aplicado na comunidade e transforma os dados em indicadores e
graficos que ajudam os monitores do telecentro a PRIORIZAR as
oficinas de inclusao digital.

Executar:
    pip install -r requirements.txt
    streamlit run app.py
"""

import os
import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Painel de Inclusao Digital", layout="wide")

CAMINHO_DADOS = os.path.join("dados", "respostas_comunidade.csv")

HABILIDADES = {
    "ligar_e_usar_computador": "Ligar e usar o computador",
    "navegar_internet": "Navegar na internet",
    "enviar_email": "Enviar e-mail",
    "usar_apps_gov_br": "Usar servicos gov.br",
    "buscar_emprego_online": "Buscar emprego online",
    "seguranca_senhas": "Seguranca / senhas",
}


@st.cache_data
def carregar_dados(caminho):
    df = pd.read_csv(caminho)
    return df


def nivel_medio_habilidades(df):
    """Retorna um DataFrame ordenado com a media de cada habilidade (0 a 3)."""
    medias = df[list(HABILIDADES.keys())].mean().rename(index=HABILIDADES)
    out = medias.reset_index()
    out.columns = ["habilidade", "nivel_medio"]
    return out.sort_values("nivel_medio")


# ------------------------------------------------------------------ UI
st.title("Painel de Inclusao Digital")
st.caption(
    "Telecentro comunitario - bairro Sitio Cercado, Curitiba/PR | "
    "Atividade Extensionista II - Ciencia de Dados"
)

if not os.path.exists(CAMINHO_DADOS):
    st.error(
        "Base nao encontrada. Rode 'python gerar_dados.py' para criar "
        "os dados de exemplo ou coloque o CSV em dados/respostas_comunidade.csv."
    )
    st.stop()

df = carregar_dados(CAMINHO_DADOS)

# ----- Filtros
st.sidebar.header("Filtros")
faixas = st.sidebar.multiselect(
    "Faixa etaria",
    sorted(df["faixa_etaria"].unique()),
    default=sorted(df["faixa_etaria"].unique()),
)
df_f = df[df["faixa_etaria"].isin(faixas)] if faixas else df

# ----- Indicadores (KPIs)
total = len(df_f)
sem_internet = (df_f["tem_internet_casa"] == "Nao").mean() * 100 if total else 0
sem_pc = (df_f["dispositivo_principal"] == "Nenhum").mean() * 100 if total else 0
nivel_geral = df_f[list(HABILIDADES.keys())].mean().mean() if total else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Respondentes", total)
c2.metric("Sem internet em casa", f"{sem_internet:.0f}%")
c3.metric("Sem dispositivo proprio", f"{sem_pc:.0f}%")
c4.metric("Nivel medio (0-3)", f"{nivel_geral:.2f}")

st.divider()

# ----- Grafico 1: habilidades com maior lacuna (base p/ priorizacao)
st.subheader("Onde estao as maiores lacunas de habilidade")
st.write(
    "Quanto menor o nivel medio (escala 0 a 3), maior a necessidade de oficina "
    "naquela habilidade."
)
tab_hab = nivel_medio_habilidades(df_f)
gr1 = (
    alt.Chart(tab_hab)
    .mark_bar()
    .encode(
        x=alt.X("nivel_medio:Q", title="Nivel medio (0 a 3)", scale=alt.Scale(domain=[0, 3])),
        y=alt.Y("habilidade:N", sort="x", title=""),
        tooltip=["habilidade", alt.Tooltip("nivel_medio:Q", format=".2f")],
    )
)
st.altair_chart(gr1, width='stretch')

col_a, col_b = st.columns(2)

# ----- Grafico 2: distribuicao por faixa etaria
with col_a:
    st.subheader("Perfil por faixa etaria")
    tab_faixa = df_f["faixa_etaria"].value_counts().reset_index()
    tab_faixa.columns = ["faixa_etaria", "qtd"]
    gr2 = (
        alt.Chart(tab_faixa)
        .mark_bar()
        .encode(
            x=alt.X("faixa_etaria:N", title="Faixa etaria"),
            y=alt.Y("qtd:Q", title="Respondentes"),
            tooltip=["faixa_etaria", "qtd"],
        )
    )
    st.altair_chart(gr2, width='stretch')

# ----- Grafico 3: interesse por oficina
with col_b:
    st.subheader("Oficinas de maior interesse")
    tab_of = df_f["interesse_oficina"].value_counts().reset_index()
    tab_of.columns = ["oficina", "qtd"]
    gr3 = (
        alt.Chart(tab_of)
        .mark_bar()
        .encode(
            x=alt.X("qtd:Q", title="Respondentes"),
            y=alt.Y("oficina:N", sort="-x", title=""),
            tooltip=["oficina", "qtd"],
        )
    )
    st.altair_chart(gr3, width='stretch')

# ----- Recomendacao automatica de priorizacao
st.divider()
st.subheader("Sugestao de priorizacao das oficinas")
top = tab_hab.head(3)["habilidade"].tolist()
st.success(
    "Com base nas menores medias, priorizar oficinas para: "
    + "; ".join(top)
    + "."
)

with st.expander("Ver dados brutos"):
    st.dataframe(df_f, width='stretch')
