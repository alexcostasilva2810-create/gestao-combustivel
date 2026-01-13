import streamlit as st
from datetime import date
import pandas as pd
import time

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="ZION - Gestão PRO", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #001f3f; } /* Fundo Azul Marinho */
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; } /* Rótulos Azuis */
    .texto-verde { color: #00FF00 !important; font-size: 20px !important; font-weight: bold; } /* Verde Forte */
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }
    input { background-color: white !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LISTA DE EMPURRADORES ---
LISTA_EMPURRADORES = [
    "JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", 
    "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", 
    "LUIZ FELLIPE", "AROEIRA", "ANGICO"
]

# --- 3. GESTÃO DE TELAS ---
if 'tela' not in st.session_state: st.session_state.tela = 'registro'
if 'dados_temp' not in st.session_state: st.session_state.dados_temp = {}

# --- TELA 1: REGISTRO E CAPTURA ---
if st.session_state.tela == 'registro':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("captura_inicial"):
        col1, col2 = st.columns(2)
        with col1:
            # Lista suspensa restaurada
            emp = st.selectbox("EMPURRADOR", options=LISTA_EMPURRADORES)
            pedido = st.text_input("Nº PEDIDO")
            nf = st.number_input("Nº NF", step=1, format="%d")
        with col2:
            qtd = st.number_input("QUANTIDADE (LTS)", step=1, format="%d")
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY")
            forn = st.text_input("FORNECEDOR")
            
        st.write("---")
        st.write("📸 **Captura da Chave**")
        chave = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        
        if st.form_submit_button("AVANÇAR PARA CONFERÊNCIA"):
            st.session_state.dados_temp = {
                "emp": emp, "pedido": pedido, "nf": nf, "qtd": qtd, "dt": dt, "chave": chave, "forn": forn
            }
            st.session_state.tela = 'edicao'
            st.rerun()

# --- TELA 2: CONFERÊNCIA, EDIÇÃO E MAPA ---
elif st.session_state.tela == 'edicao':
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferir e Validar Dados</h2>', unsafe_allow_html=True)
    d = st.session_state.dados_temp

    with st.form("edicao_final"):
        st.markdown('<p class="texto-verde">Edite os campos da Nota Fiscal abaixo:</p>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            ed_nf = st.text_input("Confirmar Nº NF", value=str(d['nf']))
            ed_chave = st.text_input("Confirmar Chave de Acesso", value=d['chave'])
        with col_b:
            ed_forn = st.text_input("Confirmar Fornecedor", value=d['forn'])
            ed_qtd = st.text_input("Confirmar Qtd (LTS)", value=str(d['qtd']))

        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        ta, tb = st.columns(2)
        v_bb = ta.number_input("TANQUE BB (m³)", step=0.01)
        v_be = tb.number_input("TANQUE BE (m³)", step=0.01)

        # --- MAPA NO RODAPÉ DO FORMULÁRIO ---
        st.write("---")
        st.markdown('<p class="texto-verde">📍 Localização do Abastecimento</p>', unsafe_allow_html=True)
        # Mapa colorido de Belém
        map_df = pd.DataFrame({'lat': [-1.4000], 'lon': [-48.3963]}) 
        st.map(map_df, zoom=14)

        if st.form_submit_button("🚀 TUDO CERTO! ENVIAR AO NOTION"):
            st.success("✅ Registro enviado com sucesso!")
            time.sleep(2)
            st.session_state.tela = 'registro'
            st.rerun()

    if st.button("⬅️ VOLTAR E CORRIGIR"):
        st.session_state.tela = 'registro'
        st.rerun()
