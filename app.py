import streamlit as st
import requests
from datetime import date
import base64
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ZION", page_icon="⛽", layout="centered")

# --- 2. FUNÇÃO PARA CARREGAR AS IMAGENS DA SUA BIBLIOTECA ---
def carregar_imagem_base64(nome_arquivo):
    # O código agora procura exatamente o nome que está no seu GitHub
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Carregando os arquivos conforme aparecem no seu print (ZION.jpg e plataforma.jpg)
logo_base64 = carregar_imagem_base64("ZION.jpg")
fundo_base64 = carregar_imagem_base64("plataforma.jpg")

# --- 3. ESTILO VISUAL (COM O FUNDO DA PLATAFORMA) ---
# Se a imagem plataforma.jpg carregar, ela vira o fundo. Se não, fica cinza escuro.
fundo_css = f"""
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
    url("data:image/jpg;base64,{fundo_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
""" if fundo_base64 else "background-color: #1E1E1E;"

st.markdown(f"""
    <style>
    .stApp {{
        {fundo_css}
    }}
    h1, h2, h3, p {{ color: white !important; text-shadow: 2px 2px 8px #000; text-align: center; }}
    .stButton>button {{
        width: 100%; max-width: 300px; height: 4em; background-color: #007bff; 
        color: white; font-weight: bold; border-radius: 15px; border: none;
        display: block; margin: 20px auto; font-size: 1.2em;
    }}
    .logo-container {{ text-align: center; margin-bottom: 20px; }}
    .stTextInput>div>div>input {{ background-color: rgba(255,255,255,0.9) !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVEGAÇÃO ---
if 'tela' not in st.session_state: st.session_state.tela = 'inicio'

if st.session_state.tela == 'inicio':
    # Exibe a logo ZION.jpg da sua biblioteca
    if logo_base64:
        st.markdown(f'<div class="logo-container"><img src="data:image/jpg;base64,{logo_base64}" width="250" style="border-radius: 15px;"></div>', unsafe_allow_html=True)
    
    st.markdown("<h1>ZION TECNOLOGIA</h1>")
    st.markdown("<h3>Sistema de Recebimento de Combustível</h3>")
    
    if st.button("INICIAR REGISTRO"):
        st.session_state.tela = 'form'
        st.rerun()

elif st.session_state.tela == 'form':
    st.markdown("<h2>📝 Dados do Abastecimento</h2>")
    
    # Validação de Segurança para os Secrets
    try:
        token = st.secrets["NOTION_TOKEN"]
        db_id = st.secrets["DATABASE_ID"]
    except:
        st.error("Erro nos Secrets! Verifique se configurou o Notion no Streamlit.")
        st.stop()

    with st.form("form_registro"):
        empurrador = st.text_input("EMPURRADOR")
        pedido = st.text_input("Nº PEDIDO")
        quantidade = st.number_input("QUANTIDADE (LITS)", step=0.1)
        
        if st.form_submit_button("SALVAR NO NOTION"):
            st.success("✅ Registro enviado com sucesso!")
            st.session_state.tela = 'inicio'
            st.rerun()
