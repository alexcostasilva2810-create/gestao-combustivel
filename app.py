import streamlit as st
import requests
from datetime import date
import base64
import os

# --- CONFIGURAÇÃO E CARREGAMENTO ---
st.set_page_config(page_title="ZION", page_icon="⛽", layout="centered")

def carregar_imagem(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Carrega as imagens da sua biblioteca
logo_base64 = carregar_imagem("ZION.jpg")
fundo_base64 = carregar_imagem("plataforma.jpg")

# --- ESTILO CSS ---
fundo_css = f'background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("data:image/jpg;base64,{fundo_64}");' if fundo_base64 else "background-color: #1E1E1E;"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("data:image/jpg;base64,{fundo_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* CORREÇÃO DO TEXTO: Força a cor branca e remove sombras estranhas */
    .titulo-principal {{
        color: white !important;
        font-size: 40px !important;
        font-weight: bold;
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
        margin-top: 10px;
    }}
    .subtitulo {{
        color: #f0f0f0 !important;
        font-size: 20px !important;
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

# --- NAVEGAÇÃO ---
if 'tela' not in st.session_state: st.session_state.tela = 'inicio'

if st.session_state.tela == 'inicio':
    # Exibe a logo ZION.jpg
    if logo_base64:
        st.markdown(f'<div style="text-align:center"><img src="data:image/jpg;base64,{logo_base64}" width="250" style="border-radius:20px; box-shadow: 0px 4px 15px rgba(0,0,0,0.5);"></div>', unsafe_allow_html=True)
    
    # --- CORREÇÃO DO ERRO CIRCULADO EM VERMELHO ---
    st.markdown('<p class="titulo-principal">ZION TECNOLOGIA</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitulo">Sistema de Recebimento de Combustível</p>', unsafe_allow_html=True)
    
    if st.button("INICIAR REGISTRO"):
        st.session_state.tela = 'form'
        st.rerun()

elif st.session_state.tela == 'form':
    st.markdown('<p class="titulo-principal">📝 Novo Registro</p>', unsafe_allow_html=True)
    # Restante do seu código do formulário aqui...
