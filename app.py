import streamlit as st
from datetime import date
import pandas as pd
import time
import requests #

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL (FIEL À IMAGEM) ---
st.set_page_config(page_title="ZION TECNOLOGIA", page_icon="⛽", layout="centered")

# CSS para o fundo petrolífero real e estilização dos botões
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
        background-color: rgba(0, 8, 20, 0.7); /* Tom escuro para destacar o robô */
        z-index: -1;
    }
    .main-container {
        text-align: center;
        padding-top: 50px;
    }
    .btn-iniciar {
        background-color: #007bff;
        color: white !important;
        padding: 15px 30px;
        border-radius: 15px;
        font-weight: bold;
        text-decoration: none;
        font-size: 1.2em;
        border: none;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTÃO DE NAVEGAÇÃO ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'home'

# --- 3. TELA INICIAL (RESTORE: ROBÔ + TEXTOS + BOTÃO) ---
if st.session_state.tela == 'home':
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Exibição do Robô (ZION.jpg) centralizado
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("ZION.jpg", use_container_width=True)
    
    # Correção dos textos que apareciam com erro de tag
    st.markdown('<h1 style="color:white; margin-bottom:0;">ZION TECNOLOGIA</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#d1d1d1; margin-top:0;">Sistema de Recebimento de Combustível</h3>', unsafe_allow_html=True)
    
    st.write("") # Espaçamento
    
    # Botão de Ação que inicia o processo
    if st.button("INICIAR REGISTRO", use_container_width=True, type="primary"):
        st.session_state.tela = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. TELA DE LOGIN (MODULAR) ---
elif st.session_state.tela == 'login':
    # Aqui entra o bloco de login que validamos antes, 
    # garantindo a segurança dos 13 usuários.
    st.markdown('<h2 style="color:white; text-align:center;">Acesso ao Sistema</h2>', unsafe_allow_html=True)
    with st.form("login"):
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.form_submit_button("ENTRAR"):
            # Lógica de validação aqui...
            st.session_state.autenticado = True
            st.session_state.tela = 'registro'
            st.rerun()
    if st.button("VOLTAR"):
        st.session_state.tela = 'home'
        st.rerun()
