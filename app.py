import streamlit as st
from datetime import date
import base64
import os
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ZION - Gestão", page_icon="⛽", layout="centered")

# Função para carregar imagens locais
def carregar_imagem_base64(caminho):
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_64 = carregar_imagem_base64("ZION.jpg")
fundo_64 = carregar_imagem_base64("plataforma.jpg")

# --- 2. ESTILO VISUAL (Rótulos Azuis e Título Verde) ---
fundo_estilo = f"""
    background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
    url("data:image/jpg;base64,{fundo_64}");
    background-size: cover; background-position: center; background-attachment: fixed;
""" if fundo_64 else "background-color: #1E1E1E;"

st.markdown(f"""
    <style>
    .stApp {{ {fundo_estilo} }}
    
    /* Letras acima dos campos em AZUL */
    label, .stWidgetLabel p {{
        color: #007bff !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }}

    /* Título dos Tanques em VERDE FORTE */
    .texto-verde {{
        color: #00FF00 !important;
        font-size: 20px !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px #000;
        margin-top: 20px;
        margin-bottom: 10px;
    }}

    .stButton>button {{
        width: 100%; max-width: 300px; height: 3.5em; background-color: #007bff; 
        color: white; font-weight: bold; border-radius: 12px;
    }}
    
    input, div[data-baseweb="select"] > div {{ 
        background-color: white !important; 
        color: black !important; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DADOS ---
LISTA_EMPURRADORES = ["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"]
USUARIOS = {"admin": "zion123"}

# --- 4. CONTROLE DE ESTADO ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'inicio'

# --- 5. LOGICA DE TELAS ---

# TELA DE LOGIN
if not st.session_state.autenticado:
    st.markdown('<h1 style="color:white; text-align:center;">GOVERNANÇA DE ACESSO</h1>', unsafe_allow_html=True)
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("INICIAR"):
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

# TELA INICIAL
elif st.session_state.tela == 'inicio':
    st.markdown('<h1 style="color:white; text-align:center;">Bem vindo ao Zion !!</h1>', unsafe_allow_html=True)
    if st.button("ABRIR REGISTRO"):
        st.session_state.tela = 'form'
        st.rerun()

# TELA DO FORMULÁRIO (ONDE ESTAVA O ERRO)
elif st.session_state.tela == 'form':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_registro"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("EMPURRADOR", options=LISTA_EMPURRADORES)
            st.text_input("Nº PEDIDO")
            st.number_input("Nº NF", step=1, format="%d")
            
            # Campo para a Chave da NF (individual)
            chave_nf = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
            
            # Link para o site Consulta Danfe
            if len(chave_nf) == 44:
                st.link_button("📄 ABRIR NO CONSULTA DANFE", f"https://www.consultadanfe.com/?chave={chave_nf}")

        with col2:
            st.number_input("QUANTIDADE (LTS)", step=1, format="%d")
            st.date_input("DATA", value=date.today(), format="DD/MM/YYYY")
            st.text_input("FORNECEDOR")
            
            # Câmera para escanear
            st.write("📸 **Escanear Nota**")
            st.camera_input("Tirar foto do código")

        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        c_a, c_b = st.columns(2)
        with c_a: st.number_input("TANQUE BB (m³)", step=0.01)
        with c_b: st.number_input("TANQUE BE (m³)", step=0.01)

        if st.form_submit_button("CONCLUIR E ENVIAR AO NOTION"):
            st.success("✅ Dados enviados com sucesso!")
            time.sleep(1)
            st.session_state.tela = 'inicio'
            st.rerun()

    if st.button("Voltar"):
        st.session_state.tela = 'inicio'
        st.rerun()
