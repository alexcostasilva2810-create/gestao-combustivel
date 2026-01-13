import streamlit as st
from datetime import date
import pandas as pd
import time
import requests #

# --- 1. CONFIGURAÇÃO DA PÁGINA E ESTILO ---
st.set_page_config(page_title="ZION - Gestão PRO", page_icon="⛽", layout="centered")

# CSS para usar plataforma.jpg como fundo
st.markdown("""
    <style>
    .stApp {
        background-image: url("app/static/plataforma.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 31, 63, 0.85);
        z-index: -1;
    }
    .login-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 40px;
        border-radius: 20px;
        border: 2px solid #007bff;
        backdrop-filter: blur(15px);
        text-align: center;
    }
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE ESTADOS (PREVINE KEYERROR) ---
#
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'registro'
if 'dados_nf' not in st.session_state: st.session_state.dados_nf = {}

# Governança
USUARIOS = {"admin": "zion01", "gestor": "zion02", "usuario1": "123"}

# --- 3. TELA DE LOGIN (ZION.jpg) ---
if not st.session_state.autenticado:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    try:
        st.image("ZION.jpg", width=200) #
    except:
        st.write("### ZION GESTÃO PRO")
    
    with st.form("login_form"):
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.form_submit_button("ACESSAR SISTEMA"): #
            if u in USUARIOS and USUARIOS[u] == s:
                st.session_state.autenticado = True
                st.session_state.user_logado = u
                st.rerun()
            else:
                st.error("Dados incorretos")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 4. TELA DE REGISTRO ---
if st.session_state.tela == 'registro':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_cadastro"):
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=["JACARANDA", "CUMARU", "SAMAUMA"])
            nf_num = st.text_input("Nº NF")
            forn = st.text_input("FORNECEDOR")
        with col2:
            # Correção do formato da data
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY") 
            qtd = st.number_input("QUANTIDADE (LTS)", step=1)
            valor = st.number_input("VALOR NF", step=0.01)

        st.write("---")
        t_bb = st.number_input("TANQUE BB (m³)", step=0.01)
        t_be = st.number_input("TANQUE BE (m³)", step=0.01)
        chave = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)

        if st.form_submit_button("CONFERIR DADOS"): #
            st.session_state.dados_nf = {
                "emp": emp, "nf": nf_num, "dt": dt, "qtd": qtd, 
                "forn": forn, "valor": valor, "t_bb": t_bb, "t_be": t_be, "chave": chave
            }
            st.session_state.tela = 'edicao'
            st.rerun()

# --- 5. TELA DE CONFERÊNCIA (SOLUÇÃO KEYERROR) ---
elif st.session_state.tela == 'edicao':
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    
    # Se os dados sumirem por erro de reload, volta para o início com segurança
    if not st.session_state.dados_nf:
        st.session_state.tela = 'registro'
        st.rerun()

    d = st.session_state.dados_nf
    with st.form("form_confirm"):
        # Exibição segura dos dados
        st.write(f"**Empurrador:** {d['emp']} | **Nota:** {d['nf']}")
        st.write(f"**Realizado:** {d['qtd']} LTS | **Data:** {d['dt'].strftime('%d/%m/%Y')}") #
        
        if st.form_submit_button("🚀 SALVAR NO NOTION"): #
            # Aqui entra a sua função enviar_ao_notion(d)
            st.success("Dados enviados!")
            time.sleep(1)
            st.session_state.tela = 'registro'
            st.rerun()

    if st.button("🔄 CORRIGIR"):
        st.session_state.tela = 'registro'
        st.rerun()
