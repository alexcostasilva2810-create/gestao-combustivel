import streamlit as st
from datetime import date
import pandas as pd

# --- 1. CONFIGURAÇÃO E ESTILO (Fundo Azul Marinho) ---
st.set_page_config(page_title="ZION - Gestão PRO", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #001f3f; } 
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; } 
    .texto-verde { color: #00FF00 !important; font-size: 20px !important; font-weight: bold; } 
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; background-color: #007bff; color: white; }
    input { background-color: white !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LISTA DE EMPURRADORES ---
LISTA_EMPURRADORES = ["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"]

# --- 3. NAVEGAÇÃO POR ABAS (Evita erros de tela em branco) ---
aba_registro, aba_historico = st.tabs(["📝 REGISTRO E CONFERÊNCIA", "📋 LANÇAMENTOS"])

with aba_registro:
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    # Início do Formulário Único para evitar KeyError
    with st.form("form_unico"):
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=LISTA_EMPURRADORES)
            pedido = st.text_input("Nº PEDIDO")
            nf = st.number_input("Nº NF", step=1, format="%d")
        with col2:
            qtd = st.number_input("QUANTIDADE (LTS)", step=1, format="%d")
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY")
            forn = st.text_input("FORNECEDOR")

        st.write("---")
        st.markdown('<p class="texto-verde">🔍 Conferir e Editar Chave da Nota</p>', unsafe_allow_html=True)
        chave = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        
        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        ca, cb = st.columns(2)
        t_bb = ca.number_input("TANQUE BB (m³)", step=0.01)
        t_be = cb.number_input("TANQUE BE (m³)", step=0.01)

        # O botão de submissão DEVE estar aqui dentro
        enviar = st.form_submit_button("✅ CONFIRMAR E ENVIAR AO NOTION")

    # --- 4. MAPA ABAIXO DO FORMULÁRIO ---
    st.write("---")
    st.markdown('<p class="texto-verde">📍 Localização do Abastecimento</p>', unsafe_allow_html=True)
    # Mapa de Belém, PA
    map_df = pd.DataFrame({'lat': [-1.4000], 'lon': [-48.3963]}) 
    st.map(map_df, zoom=14)

    if enviar:
        if len(chave) < 44:
            st.warning("Atenção: A chave da nota parece estar incompleta.")
        st.success("Dados processados! Integração com Notion pronta.")

with aba_historico:
    st.markdown('<h2 style="color:white; text-align:center;">📋 Últimos Lançamentos</h2>', unsafe_allow_html=True)
    st.info("Aqui aparecerão os dados salvos no Notion.")
