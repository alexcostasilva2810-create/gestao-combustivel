import streamlit as st
from datetime import date
import pandas as pd
import time
import requests

# --- BLOCO 1: CONFIGURAÇÃO E IDENTIDADE ---
st.set_page_config(page_title="ZION - Gestão PRO", page_icon="⛽", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #001f3f; } 
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; } 
    .texto-verde { color: #00FF00 !important; font-size: 20px !important; font-weight: bold; } 
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }
    
    /* Estilização para simular janela flutuante de login */
    .login-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #007bff;
        backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- BLOCO 2: GOVERNANÇA (13 ACESSOS) ---
USUARIOS_AUTORIZADOS = {
    "admin": "zion01", "gestor": "zion02", "usuario1": "123", "usuario2": "234",
    "usuario3": "345", "usuario4": "456", "usuario5": "567", "usuario6": "678",
    "usuario7": "789", "usuario8": "890", "usuario9": "901", "usuario10": "012",
    "usuario11": "124"
}

if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'registro'
if 'dados_nf' not in st.session_state: st.session_state.dados_nf = {}

# --- BLOCO 3: INTERFACE DE LOGIN FLUTUANTE ---
if not st.session_state.autenticado:
    st.markdown('<br><br>', unsafe_allow_html=True)
    # Container centralizado para simular a tela flutuante
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h2 style="color:white; text-align:center;">⛽ ZION Gestão PRO</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:#007bff; text-align:center;">Entre com as suas credenciais para aceder ao registo</p>', unsafe_allow_html=True)
        
        with st.form("login_flutuante"):
            u = st.text_input("Utilizador")
            s = st.text_input("Palavra-passe", type="password")
            entrar = st.form_submit_button("ACEDER AO SISTEMA")
            
            if entrar:
                if u in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[u] == s:
                    st.session_state.autenticado = True
                    st.session_state.user_logado = u
                    st.success(f"Bem-vindo, {u}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Credenciais inválidas. Tente novamente.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- BLOCO 4: REGISTO (SÓ APARECE APÓS LOGIN) ---
if st.session_state.tela == 'registro':
    st.markdown(f'<p style="color:gray; text-align:right;">Sessão: {st.session_state.user_logado}</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="color:white; text-align:center;">📝 Novo Registo de Combustível</h2>', unsafe_allow_html=True)
    
    # Restante do código de registo (Scanner, Colunas, Tanques) permanece aqui...
    # [Mantendo a lógica de colunas e botões de retorno conforme solicitado anteriormente]
    
    with st.form("form_registo_principal"):
        # Scanner e Chave
        st.camera_input("Escanear NF")
        chave_input = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"])
            forn = st.text_input("FORNECEDOR")
        with col2:
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY")
            nf_num = st.text_input("Nº DA NOTA")

        if st.form_submit_button("AVANÇAR"):
            st.session_state.dados_nf = {"emp": emp, "nf": nf_num, "dt": dt, "forn": forn, "chave": chave_input}
            st.session_state.tela = 'edicao'
            st.rerun()
