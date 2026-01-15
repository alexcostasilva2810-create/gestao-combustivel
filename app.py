import streamlit as st
from datetime import date
import time

# --- CONFIGURAÇÃO PARA CELULAR E TABLET ---
st.set_page_config(
    page_title="ZION TECNOLOGIA", 
    page_icon="⛽", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- ESTILO VISUAL CUSTOMIZADO ---
# Define o fundo com a plataforma e o estilo dos alertas
st.markdown("""
    <style>
    .stApp {
        background-image: url("app/static/plataforma.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 8, 20, 0.8); z-index: -1;
    }
    .login-box {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 30px; border-radius: 20px;
        border: 1px solid #007bff; backdrop-filter: blur(10px);
        text-align: center;
    }
    label { color: #007bff !important; font-weight: bold; font-size: 18px !important; }
    .alerta-erro { background-color: #ff4b4b; color: white; padding: 20px; border-radius: 10px; font-weight: bold; text-align: center; font-size: 1.1rem; }
    .alerta-sucesso { background-color: #28a745; color: white; padding: 20px; border-radius: 10px; font-weight: bold; text-align: center; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS DE CAPACIDADES (13 NAVIOS) ---
# Valores extraídos fielmente da tabela técnica
CAPACIDADES = {
    "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
    "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
    "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
    "TIMBORANA": 19792, "JATOBA": 84000
}

# --- CONTROLE DE ACESSO (13 USUÁRIOS) ---
USUARIOS = {
    "admin": "zion01", "gestor": "zion02", "operador1": "123", "operador2": "234",
    "operador3": "345", "operador4": "456", "operador5": "567", "operador6": "678",
    "operador7": "789", "operador8": "890", "operador9": "901", "operador10": "012",
    "operador11": "111"
}

# Gerenciamento de estado das telas
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'login'

# --- TELA DE ACESSO (LOGIN) ---
if not st.session_state.autenticado:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.image("ZION.jpg", width=250) # Imagem do robô
    st.markdown('<h2 style="color:white;">Acesso ao Sistema ODM</h2>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        user = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("ACESSAR SISTEMA", use_container_width=True)
        
        if entrar:
            if user in USUARIOS and USUARIOS[user] == senha:
                st.session_state.autenticado = True
                st.session_state.user_atual = user
                st.rerun()
            else:
                st.error("Credenciais incorretas. Verifique seu usuário e senha.")
    st.markdown('</div>', unsafe_allow_html=True)

# O Bloco 02 entrará aqui para quem estiver autenticado
