import streamlit as st
from datetime import date
import pandas as pd
import time
import requests #

# --- BLOCO 1: CONFIGURAÇÃO E ESTILO ---
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
    .texto-sucesso { color: #00FF00 !important; font-weight: bold; }
    .alerta-capacidade { background-color: rgba(255, 0, 0, 0.2); padding: 10px; border-radius: 10px; color: white; font-weight: bold; border: 1px solid red; }
    </style>
    """, unsafe_allow_html=True)

# --- BLOCO 2: DADOS DE CAPACIDADE (TABELA RESTAURADA) ---
#
CAPACIDADES = {
    "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
    "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
    "JACARANDA": 19792, "LUIZ FELLIPE": 25000, "QUARUBA": 19792,
    "TIMBORANA": 19792, "JATOBA": 84000
}

USUARIOS_AUTORIZADOS = {
    "admin": "zion01", "gestor": "zion02", "usuario1": "123", "usuario2": "234",
    "usuario3": "345", "usuario4": "456", "usuario5": "567", "usuario6": "678",
    "usuario7": "789", "usuario8": "890", "usuario9": "901", "usuario10": "012",
    "usuario11": "124"
}

if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'home'
if 'dados_nf' not in st.session_state: st.session_state.dados_nf = {}

# --- BLOCO 3: TELA INICIAL ---
if st.session_state.tela == 'home':
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("ZION.jpg", use_container_width=True) #
    st.markdown('<h1 style="color:white; margin-bottom:0;">ZION TECNOLOGIA</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#d1d1d1; margin-top:0;">Sistema de Recebimento de Combustível</h3>', unsafe_allow_html=True)
    if st.button("INICIAR REGISTRO", use_container_width=True, type="primary"):
        st.session_state.tela = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- BLOCO 4: LOGIN ---
elif st.session_state.tela == 'login':
    st.markdown('<div class="main-container"><div class="login-box">', unsafe_allow_html=True)
    st.image("ZION.jpg", width=150)
    with st.form("login_form"):
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.form_submit_button("ACESSAR SISTEMA"):
            if u in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[u] == s:
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

# --- BLOCO 5: REGISTRO COM VALIDAÇÃO DE CAPACIDADE ---
elif st.session_state.tela == 'registro' and st.session_state.autenticado:
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_registro"):
        c1, c2 = st.columns(2)
        with c1:
            emp = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys()))
            cap_max = CAPACIDADES[emp]
            st.info(f"Atenção: este empurrador só pode receber {cap_max:,} lts conforme a tabela.") #
            nf = st.text_input("Nº NOTA FISCAL")
        with c2:
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY") #
            qtd_nf = st.number_input("QUANTIDADE (LTS) NA NOTA", step=1)
            remanescente = st.number_input("VOLUME REMANESCENTE NO TANQUE (LTS)", step=1)

        total_previsto = qtd_nf + remanescente
        
        st.write("---")
        st.markdown('<p class="texto-sucesso">⛽ Volume atual nos Tanques (m³)</p>', unsafe_allow_html=True)
        t1, t2 = st.columns(2)
        v_bb = t1.number_input("TANQUE BB", step=0.01)
        v_be = t2.number_input("TANQUE BE", step=0.01)
        
        # Lógica de Alerta
        if total_previsto <= cap_max:
            st.success("✅ EMPURRADOR COM CAPACIDADE PARA RECEBER COMBUSTÍVEL")
        else:
            st.markdown(f'<div class="alerta-capacidade">⚠️ PROCURE SEU GESTOR PARA REPORTAR QUE NÃO DÁ PARA RECEBER. (Total: {total_previsto:,} lts excede {cap_max:,} lts)</div>', unsafe_allow_html=True)

        if st.form_submit_button("CONFERIR REGISTRO"):
            st.session_state.dados_nf = {
                "emp": emp, "nf": nf, "dt": dt, "qtd": qtd_nf, 
                "t_bb": v_bb, "t_be": v_be, "cap_max": cap_max, "total": total_previsto
            }
            st.session_state.tela = 'conferencia'
            st.rerun()

# --- BLOCO 6: CONFERÊNCIA ---
elif st.session_state.tela == 'conferencia':
    d = st.session_state.dados_nf
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    with st.form("final"):
        st.write(f"**Empurrador:** {d['emp']} (Limite: {d['cap_max']:,} lts)")
        st.write(f"**NF:** {d['nf']} | **Qtd:** {d['qtd']} LTS | **Total Previsto:** {d['total']} lts")
        if st.form_submit_button("🚀 SALVAR NO NOTION"):
            st.success("Enviado!")
            time.sleep(1); st.session_state.tela = 'home'; st.rerun()
    if st.button("CORRIGIR"):
        st.session_state.tela = 'registro'; st.rerun()
