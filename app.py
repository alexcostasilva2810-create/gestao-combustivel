import streamlit as st
from datetime import date
import pandas as pd

# --- 1. CONFIGURAÇÃO E ESTILO (Fundo Azul Marinho e Letras Azuis) ---
st.set_page_config(page_title="ZION - Gestão", layout="centered")

st.markdown("""
    <style>
    /* Fundo Azul Marinho */
    .stApp {
        background-color: #001f3f; 
    }
    /* Rótulos em AZUL */
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; }
    /* Título Tanques em VERDE FORTE */
    .texto-verde { color: #00FF00 !important; font-size: 20px !important; font-weight: bold; }
    /* Estilo dos Botões */
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

if 'banco_dados' not in st.session_state:
    st.session_state.banco_dados = []

# --- 2. ABAS DE NAVEGAÇÃO ---
aba1, aba2 = st.tabs(["📝 REGISTRO", "📋 LANÇAMENTOS"])

with aba1:
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    # --- FORMULÁRIO DE PREENCHIMENTO ---
    with st.form("form_registro"):
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"])
            nf = st.number_input("Nº NF", step=1, format="%d")
        with col2:
            qtd = st.number_input("QUANTIDADE (LTS)", step=1, format="%d")
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY")

        st.write("---")
        chave = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        forn = st.text_input("FORNECEDOR")

        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        ca, cb = st.columns(2)
        t_bb = ca.number_input("TANQUE BB (m³)", step=0.01)
        t_be = cb.number_input("TANQUE BE (m³)", step=0.01)

        salvar = st.form_submit_button("✅ SALVAR REGISTRO")

        if salvar:
            st.session_state.banco_dados.append({"Data": dt, "Emp": emp, "NF": nf, "Qtd": qtd})
            st.success("Dados salvos com sucesso!")

    # --- MAPA COLORIDO E PEQUENO (Abaixo do formulário) ---
    st.write("---")
    st.markdown('<p class="texto-verde">📍 Localização Atual</p>', unsafe_allow_html=True)
    
    # Criando o mapa colorido e pequeno (Belém, PA)
    df_mapa = pd.DataFrame({'lat': [-1.4000], 'lon': [-48.3963]})
    st.map(df_mapa, zoom=14, use_container_width=True) 
    st.caption("Ponto de abastecimento detectado via GPS.")

with aba2:
    st.markdown('<h2 style="color:white; text-align:center;">📋 Histórico</h2>', unsafe_allow_html=True)
    if st.session_state.banco_dados:
        st.table(pd.DataFrame(st.session_state.banco_dados))
    else:
        st.info("Nenhum lançamento registrado.")
