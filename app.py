import streamlit as st
import base64
import os
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ZION - Governança", page_icon="🔐", layout="centered")

def carregar_imagem_base64(caminho):
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_64 = carregar_imagem_base64("ZION.jpg")
fundo_64 = carregar_imagem_base64("plataforma.jpg")

# --- 2. ESTILO VISUAL ---
fundo_estilo = f"""
    background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
    url("data:image/jpg;base64,{fundo_64}");
    background-size: cover; background-position: center; background-attachment: fixed;
""" if fundo_64 else "background-color: #1E1E1E;"

st.markdown(f"""
    <style>
    .stApp {{ {fundo_estilo} }}
    .container-central {{ display: flex; flex-direction: column; align-items: center; text-align: center; }}
    .titulo-zion {{ color: white !important; font-size: 38px !important; font-weight: bold; text-shadow: 2px 2px 4px #000; margin-top: 15px; }}
    .stButton {{ display: flex; justify-content: center; }}
    .stButton>button {{ width: 100%; max-width: 300px; height: 3.5em; background-color: #007bff; color: white; font-weight: bold; border-radius: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. BANCO DE DADOS DE ACESSO (13 VAGAS) ---
USUARIOS = {
    "admin": "zion123", "user2": "senha2", "user3": "senha3", "user4": "senha4",
    "user5": "senha5", "user6": "senha6", "user7": "senha7", "user8": "senha8",
    "user9": "senha9", "user10": "senha10", "user11": "senha11", "user12": "senha12",
    "user13": "senha13"
}

# --- 4. JANELA FLUTUANTE DE LOGIN ---
@st.dialog("Governança de Acesso")
def login_modal():
    st.write("Insira suas credenciais para acessar o sistema.")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    
    if st.button("VALIDAR ACESSO"):
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            st.session_state.autenticado = True
            st.session_state.user = usuario
            st.rerun()
        else:
            st.error("Credenciais incorretas!")

# --- 5. LÓGICA DE NAVEGAÇÃO ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# TELA INICIAL COM BOTÃO DE ACESSO
if not st.session_state.autenticado:
    st.markdown('<div class="container-central">', unsafe_allow_html=True)
    if logo_64:
        st.markdown(f'<img src="data:image/jpg;base64,{logo_64}" width="250" style="border-radius:20px;">', unsafe_allow_html=True)
    
    st.markdown('<p class="titulo-zion">ZION TECNOLOGIA</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:white; font-size:18px;">Clique abaixo para entrar no sistema</p>', unsafe_allow_html=True)
    
    # Botão que abre a janela flutuante
    if st.button("INICIAR ACESSO"):
        login_modal()
    st.markdown('</div>', unsafe_allow_html=True)

# TELA APÓS LOGIN (BEM-VINDO)
else:
    st.markdown('<div class="container-central">', unsafe_allow_html=True)
    if logo_64:
        st.markdown(f'<img src="data:image/jpg;base64,{logo_64}" width="200" style="border-radius:20px;">', unsafe_allow_html=True)
    
    st.markdown('<p class="titulo-zion">Bem vindo ao Zion !!</p>', unsafe_allow_html=True)
    st.success(f"Logado como: {st.session_state.user}")
    
    if st.button("ABRIR REGISTRO"):
        st.info("Formulário em construção...")
        
    if st.button("Sair"):
        st.session_state.autenticado = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
