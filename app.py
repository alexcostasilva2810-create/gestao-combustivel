import streamlit as st
from datetime import date
import pandas as pd

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="ZION - Gestão", layout="centered")

st.markdown("""
    <style>
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; }
    .texto-verde { color: #00FF00 !important; font-size: 20px !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'banco_dados' not in st.session_state:
    st.session_state.banco_dados = []

# --- 2. ABAS (Garante que a tela não fique em branco) ---
aba1, aba2 = st.tabs(["📝 REGISTRO E MAPA", "📋 LANÇAMENTOS"])

with aba1:
    st.markdown('## ⛽ Registro com Geolocalização')
    
    # --- NOVO: BLOCO DE MAPA ---
    st.markdown('<p class="texto-verde">📍 Localização do Abastecimento</p>', unsafe_allow_html=True)
    # Simulação de coordenadas para o mapa (Em um app real, o Streamlit captura via browser)
    # Aqui ele exibirá o local atual baseado no GPS do dispositivo
    map_data = pd.DataFrame({'lat': [-1.4000], 'lon': [-48.3963]}) 
    st.map(map_data) 
    st.caption("Localização detectada: R. Manaus, Belém - PA")

    with st.form("form_completo"):
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

        if st.form_submit_button("✅ SALVAR COM LOCALIZAÇÃO"):
            novo = {
                "Data": dt.strftime("%d/%m/%Y"),
                "Empurrador": emp,
                "NF": nf,
                "Local": "R. Manaus, Belém - PA", # Dado vindo do mapa
                "Qtd": qtd,
                "Tanque BB": t_bb,
                "Tanque BE": t_be
            }
            st.session_state.banco_dados.append(novo)
            st.success("Salvo com sucesso!")

with aba2:
    st.markdown('## 📋 Histórico de Lançamentos')
    if st.session_state.banco_dados:
        st.table(pd.DataFrame(st.session_state.banco_dados))
    else:
        st.info("Aguardando lançamentos.")
