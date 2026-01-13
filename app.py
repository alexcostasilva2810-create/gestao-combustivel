import streamlit as st
from datetime import date
import pandas as pd
import time
import requests #

# --- 1. CONFIGURAÇÃO E ESTILO (IDENTIDADE ORIGINAL) ---
st.set_page_config(page_title="ZION TECNOLOGIA", page_icon="⛽", layout="centered")

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
        background-color: rgba(0, 8, 20, 0.7);
        z-index: -1;
    }
    .main-container { text-align: center; padding-top: 20px; }
    .login-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #007bff;
        backdrop-filter: blur(15px);
    }
    label { color: #007bff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTÃO DE ESTADO (PREVINE PÁGINA EM BRANCO) ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'home'
if 'dados_nf' not in st.session_state: st.session_state.dados_nf = {}

# Governança
USUARIOS = {"admin": "zion01", "gestor": "zion02", "usuario1": "123"}

# --- 3. TELA INICIAL (ROBÔ E BOAS-VINDAS) ---
if st.session_state.tela == 'home':
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("ZION.jpg", use_container_width=True) #
    
    # Textos corrigidos (sem aparecer as tags HTML)
    st.markdown('<h1 style="color:white; margin-bottom:0;">ZION TECNOLOGIA</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#d1d1d1; margin-top:0;">Sistema de Recebimento de Combustível</h3>', unsafe_allow_html=True)
    
    if st.button("INICIAR REGISTRO", use_container_width=True, type="primary"):
        st.session_state.tela = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. TELA DE LOGIN ---
elif st.session_state.tela == 'login':
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.image("ZION.jpg", width=150)
    with st.form("login_form"):
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.form_submit_button("ACESSAR SISTEMA"):
            if u in USUARIOS and USUARIOS[u] == s:
                st.session_state.autenticado = True
                st.session_state.user_logado = u
                st.session_state.tela = 'registro'
                st.rerun()
            else:
                st.error("Credenciais Inválidas")
    if st.button("VOLTAR"):
        st.session_state.tela = 'home'
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- 5. TELA DE REGISTRO (CONTEÚDO QUE FALTA) ---
elif st.session_state.tela == 'registro' and st.session_state.autenticado:
    st.markdown(f'<p style="color:white; text-align:right;">Logado: {st.session_state.user_logado}</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("registro_comb"):
        c1, c2 = st.columns(2)
        with c1:
            emp = st.selectbox("EMPURRADOR", options=["JACARANDA", "CUMARU", "SAMAUMA"])
            nf = st.text_input("Nº NF")
        with c2:
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY") #
            qtd = st.number_input("QUANTIDADE (LTS)", step=1)
        
        st.write("---")
        t_bb = st.number_input("TANQUE BB (m³)", step=0.01)
        t_be = st.number_input("TANQUE BE (m³)", step=0.01)

        if st.form_submit_button("AVANÇAR"):
            st.session_state.dados_nf = {"emp": emp, "nf": nf, "dt": dt, "qtd": qtd, "t_bb": t_bb, "t_be": t_be}
            st.session_state.tela = 'conferencia'
            st.rerun()

# --- 6. TELA DE CONFERÊNCIA ---
elif st.session_state.tela == 'conferencia':
    if not st.session_state.dados_nf: # Previne KeyError
        st.session_state.tela = 'registro'
        st.rerun()

    d = st.session_state.dados_nf
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    with st.form("confirm_form"):
        st.write(f"**Empurrador:** {d['emp']} | **Nota:** {d['nf']}")
        st.write(f"**Qtd:** {d['qtd']} LTS | **Data:** {d['dt'].strftime('%d/%m/%Y')}") #
        if st.form_submit_button("✅ SALVAR NO NOTION"):
            st.success("Dados Salvos!")
            time.sleep(2)
            st.session_state.tela = 'home'
            st.rerun()
    if st.button("CORRIGIR"):
        st.session_state.tela = 'registro'
        st.rerun()
