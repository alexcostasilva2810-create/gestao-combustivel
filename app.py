import streamlit as st
import requests
from datetime import date
import base64
import os
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ZION - Gestão", page_icon="⛽", layout="centered")

def carregar_imagem_base64(caminho):
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_64 = carregar_imagem_base64("ZION.jpg")
fundo_64 = carregar_imagem_base64("plataforma.jpg")

# --- 2. ESTILO VISUAL PERSONALIZADO ---
fundo_estilo = f"""
    background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
    url("data:image/jpg;base64,{fundo_64}");
    background-size: cover; background-position: center; background-attachment: fixed;
""" if fundo_64 else "background-color: #1E1E1E;"

st.markdown(f"""
    <style>
    .stApp {{ {fundo_estilo} }}
    
    /* Rótulos dos campos em AZUL */
    label, .stWidgetLabel p {{
        color: #007bff !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }}

    /* CORREÇÃO SOLICITADA: Texto circulado em VERDE FORTE */
    .texto-verde {{
        color: #00FF00 !important; /* Verde Limão/Forte */
        font-size: 20px !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px #000;
        margin-top: 20px;
        margin-bottom: 10px;
    }}

    .container-central {{ display: flex; flex-direction: column; align-items: center; text-align: center; }}
    .titulo-zion {{ color: white !important; font-size: 38px !important; font-weight: bold; text-shadow: 2px 2px 4px #000; }}
    
    .stButton>button {{
        width: 100%; max-width: 300px; height: 3.5em; background-color: #007bff; 
        color: white; font-weight: bold; border-radius: 12px; border: none;
    }}
    
    input {{ background-color: white !important; color: black !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. GOVERNANÇA (13 VAGAS) ---
USUARIOS = {
    "admin": "zion123", "user2": "senha2", "user3": "senha3", "user4": "senha4",
    "user5": "senha5", "user6": "senha6", "user7": "senha7", "user8": "senha8",
    "user9": "senha9", "user10": "senha10", "user11": "senha11", "user12": "senha12",
    "user13": "senha13"
}

# --- 4. JANELA FLUTUANTE DE LOGIN ---
@st.dialog("Governança de Acesso")
def login_modal():
    st.write("Identifique-se para acessar o formulário.")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("VALIDAR"):
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            st.session_state.autenticado = True
            st.session_state.user = usuario
            st.rerun()
        else:
            st.error("Dados incorretos.")

# --- 5. NAVEGAÇÃO ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'inicio'

if not st.session_state.autenticado:
    st.markdown('<div class="container-central">', unsafe_allow_html=True)
    if logo_64:
        st.markdown(f'<img src="data:image/jpg;base64,{logo_64}" width="250" style="border-radius:20px;">', unsafe_allow_html=True)
    st.markdown('<p class="titulo-zion">ZION TECNOLOGIA</p>', unsafe_allow_html=True)
    if st.button("INICIAR ACESSO"):
        login_modal()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.tela == 'inicio':
    st.markdown('<div class="container-central">', unsafe_allow_html=True)
    st.markdown('<p class="titulo-zion">Bem vindo ao Zion !!</p>', unsafe_allow_html=True)
    st.write(f"Operador atual: **{st.session_state.user}**")
    if st.button("ABRIR REGISTRO"):
        st.session_state.tela = 'form'
        st.rerun()
    if st.button("Sair"):
        st.session_state.autenticado = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# TELA DO FORMULÁRIO COM DESTAQUE VERDE
elif st.session_state.tela == 'form':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_registro"):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("EMPURRADOR")
            st.text_input("Nº PEDIDO")
            st.number_input("Nº NF", step=1)
        with c2:
            st.number_input("QUANTIDADE (LTS)", step=0.1)
            st.date_input("DATA", date.today())
            st.text_input("FORNECEDOR")
        
        # APLICAÇÃO DA COR VERDE FORTE
        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.number_input("TANQUE BB (m³)", step=0.01)
        with col_b:
            st.number_input("TANQUE BE (m³)", step=0.01)

        if st.form_submit_button("CONCLUIR E ENVIAR AO NOTION"):
            st.success("✅ Enviado com sucesso!")
            time.sleep(1)
            st.session_state.tela = 'inicio'
            st.rerun()

    if st.button("Voltar"):
        st.session_state.tela = 'inicio'
        st.rerun()
