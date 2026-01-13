import streamlit as st
from datetime import date
import pandas as pd
import time
import requests #

# --- 1. CONFIGURAÇÃO E ESTILO (RESTAURANDO FUNDO PETROLÍFERO) ---
st.set_page_config(page_title="ZION - Gestão PRO", page_icon="⛽", layout="centered")

# CSS para carregar plataforma.jpg e estilizar o retângulo
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
    /* Ajuste do Retângulo de Título */
    .titulo-container {
        border: 2px solid #007bff;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        background-color: rgba(255, 255, 255, 0.05);
    }
    .login-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #007bff;
        backdrop-filter: blur(15px);
        text-align: center;
    }
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO SEGURA (EVITA KEYERROR) ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'registro'
if 'dados_nf' not in st.session_state: st.session_state.dados_nf = {}

# Governança (13 Usuários)
USUARIOS = {"admin": "zion01", "gestor": "zion02", "usuario1": "123"}

# --- 3. TELA DE ACESSO COM LOGO E TÍTULO NO RETÂNGULO ---
if not st.session_state.autenticado:
    # Retângulo de Título Ajustado
    st.markdown('<div class="titulo-container"><h1 style="color:white; margin:0;">ZION TECNOLOGIA</h1></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    try:
        st.image("ZION.jpg", width=250) # Logo do repositório
    except:
        st.write("### ZION")
    
    with st.form("login_form"):
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        # Submit button obrigatório
        if st.form_submit_button("ACESSAR SISTEMA"):
            if u in USUARIOS and USUARIOS[u] == s:
                st.session_state.autenticado = True
                st.session_state.user_logado = u
                st.rerun()
            else:
                st.error("Credenciais Inválidas")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 4. TELA DE REGISTRO (DATA BRASILEIRA) ---
if st.session_state.tela == 'registro':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_reg"):
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=["JACARANDA", "CUMARU", "SAMAUMA"])
            nf = st.text_input("Nº NF")
        with col2:
            # Forçando formato brasileiro
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY")
            qtd = st.number_input("QUANTIDADE (LTS)", step=1)

        # Campos de Tanques adicionados
        t_bb = st.number_input("TANQUE BB (m³)", step=0.01)
        t_be = st.number_input("TANQUE BE (m³)", step=0.01)

        if st.form_submit_button("CONFERIR"):
            st.session_state.dados_nf = {
                "emp": emp, "nf": nf, "dt": dt, 
                "qtd": qtd, "t_bb": t_bb, "t_be": t_be
            }
            st.session_state.tela = 'edicao'
            st.rerun()

# --- 5. TELA DE CONFERÊNCIA (ESTABILIZADA) ---
elif st.session_state.tela == 'edicao':
    # Proteção contra KeyError: volta ao registro se os dados sumirem
    if not st.session_state.dados_nf:
        st.session_state.tela = 'registro'
        st.rerun()

    d = st.session_state.dados_nf
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    
    with st.form("conf_form"):
        st.write(f"**Empurrador:** {d['emp']} | **Nota:** {d['nf']}")
        st.write(f"**Quantidade:** {d['qtd']} LTS | **Data:** {d['dt'].strftime('%d/%m/%Y')}") #
        
        if st.form_submit_button("✅ SALVAR NO NOTION"):
            st.success("Dados prontos para envio!")
            time.sleep(1)
            st.session_state.tela = 'registro'
            st.rerun()
    
    if st.button("🔄 CORRIGIR"):
        st.session_state.tela = 'registro'
        st.rerun()
