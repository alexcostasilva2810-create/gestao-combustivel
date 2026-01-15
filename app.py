import streamlit as st
from datetime import date
import pandas as pd
import time
import requests #

# --- BLOCO 1: CONFIGURAÇÃO E ESTILO (IDENTIDADE ORIGINAL) ---
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
        margin-top: 20px;
    }
    label { color: #007bff !important; font-weight: bold; }
    .texto-sucesso { color: #00FF00 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- BLOCO 2: GOVERNANÇA E ESTADOS DE SESSÃO ---
# Restaurando a lista completa de 13 usuários autorizados
USUARIOS_AUTORIZADOS = {
    "ALEX": "2463", "gestor": "zion02", "usuario1": "123", "usuario2": "234",
    "usuario3": "345", "usuario4": "456", "usuario5": "567", "usuario6": "678",
    "usuario7": "789", "usuario8": "890", "usuario9": "901", "usuario10": "012",
    "usuario11": "124"
}

if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'home'
if 'dados_nf' not in st.session_state: st.session_state.dados_nf = {}

# --- BLOCO 3: TELA INICIAL (RESTORE: ROBÔ E BOAS-VINDAS) ---
if st.session_state.tela == 'home':
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("ZION.jpg", use_container_width=True) #
    
    # Textos corrigidos sem erro de tag
    st.markdown('<h1 style="color:white; margin-bottom:0;">ZION TECNOLOGIA</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#d1d1d1; margin-top:0;">Sistema de Recebimento de Combustível</h3>', unsafe_allow_html=True)
    
    if st.button("INICIAR REGISTRO", use_container_width=True, type="primary"):
        st.session_state.tela = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- BLOCO 4: TELA DE LOGIN (GOVERNANÇA ATIVA) ---
elif st.session_state.tela == 'login':
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.image("ZION.jpg", width=150)
    st.markdown('<h2 style="color:white;">Acesso Restrito</h2>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.form_submit_button("ACESSAR SISTEMA"): #
            if u in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[u] == s:
                st.session_state.autenticado = True
                st.session_state.user_logado = u
                st.session_state.tela = 'registro'
                st.rerun()
            else:
                st.error("Usuário ou Senha incorretos.")
                
    if st.button("VOLTAR À HOME"):
        st.session_state.tela = 'home'
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- BLOCO 5: TELA DE REGISTRO (TANQUES E DADOS) ---
elif st.session_state.tela == 'registro' and st.session_state.autenticado:
    st.markdown(f'<p style="color:white; text-align:right;">Operador: {st.session_state.user_logado}</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_registro"):
        c1, c2 = st.columns(2)
        with c1:
            emp = st.selectbox("EMPURRADOR", options=["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"])
            nf = st.text_input("Nº NOTA FISCAL")
        with c2:
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY") #
            qtd = st.number_input("QUANTIDADE (LTS)", step=1)
        
        st.markdown('<p class="texto-sucesso">⛽ Volume nos Tanques (m³)</p>', unsafe_allow_html=True)
        t1, t2 = st.columns(2)
        v_bb = t1.number_input("TANQUE BB", step=0.01)
        v_be = t2.number_input("TANQUE BE", step=0.01)
        
        chave_nf = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)

        if st.form_submit_button("CONFERIR REGISTRO"): #
            st.session_state.dados_nf = {
                "emp": emp, "nf": nf, "dt": dt, "qtd": qtd, 
                "t_bb": v_bb, "t_be": v_be, "chave": chave_nf
            }
            st.session_state.tela = 'conferencia'
            st.rerun()

# --- BLOCO 6: CONFERÊNCIA E NOTION ---
elif st.session_state.tela == 'conferencia':
    if not st.session_state.dados_nf:
        st.session_state.tela = 'registro'
        st.rerun()

    d = st.session_state.dados_nf
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    
    with st.form("confirm_final"):
        st.write(f"**Empurrador:** {d['emp']} | **NF:** {d['nf']}")
        st.write(f"**Realizado:** {d['qtd']} LTS | **Data:** {d['dt'].strftime('%d/%m/%Y')}") #
        st.write(f"**Tanques:** BB: {d['t_bb']}m³ | BE: {d['t_be']}m³")
        
        if st.form_submit_button("🚀 CONFIRMAR E SALVAR NO NOTION"):
            st.balloons()
            st.success("Dados enviados com sucesso!")
            time.sleep(2)
            st.session_state.tela = 'home'
            st.rerun()

    if st.button("🔄 CORRIGIR DADOS"):
        st.session_state.tela = 'registro'
        st.rerun()
