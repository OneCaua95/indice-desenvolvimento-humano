import streamlit as st
import tempfile
import streamlit.components.v1 as components
import plotly.express as px
from source.extract import Extract
from source.transform import Transform
from source.analysis import Analysis

st.set_page_config(page_title="Análise de Dados", layout="wide")

@st.cache_data
def load_data():
    data = Extract().get_data()
    return data

def show_graph(df, column, title="Gráfico de Análise"):
    fig = px.bar(df, x="Nome", y=column, title=title, labels={"Nome": "Nome", column: title})
    st.plotly_chart(fig)

def show_line_graph(df, column, title="Gráfico de Análise - País"):
    fig = px.line(df, x="Ano", y=column, title=title, labels={"Ano": "Ano", column: title})
    st.plotly_chart(fig)

def show_metrics(df_min, df_max, df_mean, df_std, worst_value, best_value):

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Valor Mínimo", value=df_min)
    with col2:
        st.metric(label="Valor Máximo", value=df_max)
    with col3:
        st.metric(label="Média", value=df_mean)
    with col4:
        st.metric(label="Desvio Padrão", value=df_std)

    col5, col6 = st.columns(2)

    with col5:
        st.metric(label="Melhor Valor", value=best_value)
    with col6:
        st.metric(label="Pior Valor", value=worst_value)

def analysis_state(year, column):
    df, df_min, df_mean, df_max, df_std, worst_value, best_value = Analysis().get_analysis_by_state(year, column)
    
    st.title(f"Análise do Estado para o Ano {year}")
    show_metrics(df_min, df_max, df_mean, df_std, worst_value, best_value)
    
    st.title("Heatmap de Índice de Desenvolvimento Humano Brasil")
    
    mapa = Analysis().get_state_heatmap(year, column)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        mapa.save(tmpfile.name)
        temp_html = tmpfile.name

    with open(temp_html, "r", encoding="utf-8") as file:
        map_html = file.read()
    components.html(map_html, height=500, width=1400)

def analysis_region(year, column):
    df, df_min, df_mean, df_max, df_std, worst_value, best_value = Analysis().get_analysis_by_region(year, column)
    
    st.write(f"### Análise da Região Metropolitana para o Ano {year}")
    show_metrics(df_min, df_max, df_mean, df_std, worst_value, best_value)
    
    show_graph(df, column, f"Análise do {column} - Região Metropolitana")

def analysis_country(column):
    df, df_min, df_mean, df_max, df_std, worst_value, best_value = Analysis().get_analysis_by_country(column)
    
    st.write(f"### Análise do País")
    show_metrics(df_min, df_max, df_mean, df_std, worst_value, best_value)
    
    show_line_graph(df, column, f"Análise do {column} - País")

def main():
    
    data = load_data()
    transformed_data = Transform().transform_data()

    available_years = sorted(transformed_data["Ano"].unique())  
    
    st.sidebar.title("Configurações")
    option = st.sidebar.radio("Escolha a Análise", ["Por Estado", "Por Região Metropolitana", "Por País"])

    if option in ["Por Estado", "Por Região Metropolitana"]:
        year = st.sidebar.selectbox("Escolha o Ano", available_years, index=available_years.index(2020) if 2020 in available_years else 0)
        column = st.sidebar.selectbox("Escolha o Indicador", ["IDH Municipal", "Expectativa de vida", "IDHM Longevidade", "IDHM Educação", "IDHM Renda", "Índice Gini", "Índice Theil"])
    else:
        year = None
        column = st.sidebar.selectbox("Escolha o Indicador", ["IDH Municipal", "Expectativa de vida", "IDHM Longevidade", "IDHM Educação", "IDHM Renda", "Índice Gini", "Índice Theil"])
    
    if option == "Por Estado":
        analysis_state(year, column)
    elif option == "Por Região Metropolitana":
        analysis_region(year, column)
    else:
        analysis_country(column)

if __name__ == "__main__":
    main()



