import streamlit as st
import requests
from datetime import date
import base64
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ZION", page_icon="⛽", layout="centered")

# Função para converter imagem da biblioteca para formato visível
def carregar_imagem_base64(caminho):
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Carregando os arquivos exatamente como estão no seu GitHub
logo_base64 = carregar_imagem_base64("ZION.jpg")
fundo_base64 = carregar_imagem_base64("plataforma.jpg")

# --- 2. ESTILO VISUAL (CORREÇÃO DO NAMEERROR) ---
# Aqui corrigimos o erro da imagem 'image_030ba7.png' usando fundo_base64 corretamente
fundo_estilo = f"""
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
    url("data:image/jpg;base64,{fundo_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
""" if fundo_base64 else "background-color: #1E1E1E;"

st.markdown(f"""
    <style>
    .stApp {{
        {fundo_estilo}
    }}
    /* Estilo para limpar o erro circulado em vermelho */
    .titulo-zion {{
        color: white !important;
        font-size: 38px !important;
        font-weight: bold;
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
        margin-bottom: 0px;
    }}
    .subtitulo-zion {{
        color: #f0f0f0 !important;
        font-size: 18px !important;
        text-align: center;
        text-shadow: 1px 1px 3px #000000;
        margin-bottom: 30px;
    }}
    .stButton>button {{
        width: 100%; max-width: 300px; height: 3.5em; background-color: #007bff; 
        color: white; font-weight: bold; border-radius: 12px; border: none;
        display: block; margin: 0 auto;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. NAVEGAÇÃO E TELAS ---
if 'tela' not in st.session_state: st.session_state.tela = 'inicio'

if st.session_state.tela == 'inicio':
    # Exibe a logo ZION.jpg
    if logo_base64:
        st.markdown(f'<div style="text-align:center"><img src="data:image/jpg;base64,{logo_base64}" width="250" style="border-radius:20px;"></div>', unsafe_allow_html=True)
    
    # --- CORREÇÃO DO ERRO CIRCULADO EM VERMELHO ---
    # Usamos classes CSS em vez de tags brutas para o texto ficar limpo
    st.markdown('<p class="titulo-zion">ZION TECNOLOGIA</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitulo-zion">Sistema de Recebimento de Combustível</p>', unsafe_allow_html=True)
    
    if st.button("INICIAR REGISTRO"):
        st.session_state.tela = 'form'
        st.rerun()

elif st.session_state.tela == 'form':
    st.markdown('<h2 style="color:white; text-align:center;">📝 Novo Registro</h2>', unsafe_allow_html=True)
    
    with st.form("registro_combustivel"):
        emp = st.text_input("EMPURRADOR")
        ped = st.text_input("Nº PEDIDO")
        if st.form_submit_button("SALVAR DADOS"):
            st.success("✅ Enviado!")
            st.session_state.tela = 'inicio'
            st.rerun()
