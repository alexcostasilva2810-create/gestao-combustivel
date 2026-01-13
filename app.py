import streamlit as st
import requests
from datetime import date
import base64
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ZION Combustível", page_icon="⛽", layout="centered")

# --- FUNÇÃO PARA CARREGAR IMAGENS LOCAIS ---
def carregar_imagem_local(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# Carregando as imagens do seu repositório
fundo_base64 = carregar_imagem_local("plataforma.jpg")
logo_base64 = carregar_imagem_local("ZION.JPG")

# --- APLICANDO O DESIGN APROVADO ---
estilo_fundo = ""
if fundo_base64:
    estilo_fundo = f"""
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("data:image/jpg;base64,{fundo_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    """

st.markdown(f"""
    <style>
    .stApp {{
        {estilo_fundo}
        color: white;
    }}
    h1, h2, h3, p, label {{
        color: white !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        text-align: center;
    }}
    .stButton>button {{
        width: 100%;
        max-width: 300px;
        height: 4em;
        background-color: #007bff;
        color: white;
        font-size: 1.2em;
        font-weight: bold;
        border-radius: 15px;
        border: none;
        margin: auto;
        display: block;
    }}
    .logo-img {{
        display: block;
        margin: auto;
        width: 250px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}
    /* Inputs visíveis */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: black !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- INTEGRAÇÃO NOTION ---
NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
DATABASE_ID = st.secrets["DATABASE_ID"]

def enviar_notion(dados):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "EMPURRADOR": {"title": [{"text": {"content": dados['emp']}}]},
            "PEDIDO": {"rich_text": [{"text": {"content": dados['ped']}}]},
            "Nº NF": {"number": dados['nf']},
            "QTOS LTS": {"number": dados['lts']},
            "CHAVE DA NF": {"rich_text": [{"text": {"content": dados['chave']}}]},
            "REALIZADO": {"date": {"start": dados['data']}},
            "FORNECEDOR": {"rich_text": [{"text": {"content": dados['forn']}}]},
            "CNPJ": {"rich_text": [{"text": {"content": dados['cnpj']}}]},
            "TANQUE BB": {"number": dados['t_bb']},
            "TANQUE BE": {"number": dados['t_be']},
            "ANTES": {"number": dados['antes']},
            "DEPOIS": {"number": dados['depois']}
        }
    }
    return requests.post(url, headers=headers, json=payload)

# --- NAVEGAÇÃO ---
if 'pg' not in st.session_state: st.session_state.pg = 'inicial'

if st.session_state.pg == 'inicial':
    if logo_base64:
        st.markdown(f'<img src="data:image/jpg;base64,{logo_base64}" class="logo-img">', unsafe_allow_html=True)
    
    st.markdown("<h1>ZION Combustível</h1>")
    st.markdown("<h3>Sistema de Registro</h3>")
    
    if st.button("INICIAR"):
        st.session_state.pg = 'form'
        st.rerun()

elif st.session_state.pg == 'form':
    st.title("⛽ Registro")
    with st.form("form_zion"):
        emp = st.text_input("EMPURRADOR")
        c1, c2 = st.columns(2)
        with c1:
            ped = st.text_input("PEDIDO")
            nf = st.number_input("Nº NF", step=1)
            lts = st.number_input("QTOS LTS", step=0.01)
        with c2:
            chave = st.text_input("CHAVE DA NF")
            dt = st.date_input("DATA", date.today())
            forn = st.text_input("FORNECEDOR")
        
        cnpj = st.text_input("CNPJ")
        t_bb = st.number_input("TANQUE BB", step=0.01)
        t_be = st.number_input("TANQUE BE", step=0.01)

        if st.form_submit_button("SALVAR"):
            dados = {"emp": emp, "ped": ped, "nf": nf, "lts": lts, "chave": chave, "data": str(dt), "forn": forn, "cnpj": cnpj, "t_bb": t_bb, "t_be": t_be, "antes": 0, "depois": 0}
            res = enviar_notion(dados)
            if res.status_code == 200:
                st.balloons()
                st.success("Enviado!")
                st.session_state.pg = 'inicial'
                st.rerun()
