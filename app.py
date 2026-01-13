import streamlit as st
import requests
from datetime import date
import base64
import os

# --- BLOCO 1: CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="ZION Combustível", page_icon="⛽", layout="centered")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Carregamento seguro das imagens
fundo_64 = get_base64("plataforma.jpg")
logo_64 = get_base64("ZION.JPG")

# Aplicação do CSS
estilo_fundo = f'background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("data:image/jpg;base64,{fundo_64}");' if fundo_64 else "background-color: #262730;"

st.markdown(f"""
    <style>
    .stApp {{
        {estilo_fundo}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    h1, h2, h3, p, label {{ color: white !important; text-shadow: 2px 2px 8px #000; text-align: center; }}
    .stButton>button {{
        width: 100%; height: 4em; background-color: #007bff; color: white;
        font-weight: bold; border-radius: 15px; border: none; margin-top: 20px;
    }}
    .logo-img {{ display: block; margin: auto; width: 220px; border-radius: 10px; margin-bottom: 20px; }}
    .stTextInput>div>div>input {{ background-color: white !important; color: black !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- BLOCO 2: CONEXÃO NOTION ---
try:
    NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
    DATABASE_ID = st.secrets["DATABASE_ID"]
except Exception as e:
    st.error(f"Erro nos Secrets: {e}")
    st.stop()

def salvar_notion(dados):
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

# --- BLOCO 3: TELAS ---
if 'pg' not in st.session_state: st.session_state.pg = 'inicio'

if st.session_state.pg == 'inicio':
    if logo_64:
        st.markdown(f'<img src="data:image/jpg;base64,{logo_64}" class="logo-img">', unsafe_allow_html=True)
    else:
        st.write("### ZION TECNOLOGIA")
    
    st.markdown("<h1>ZION Combustível</h1>")
    if st.button("INICIAR REGISTRO"):
        st.session_state.pg = 'form'
        st.rerun()

elif st.session_state.pg == 'form':
    st.markdown("<h2>📝 Dados</h2>")
    with st.form("zion_form"):
        emp = st.text_input("EMPURRADOR")
        c1, c2 = st.columns(2)
        with c1:
            ped = st.text_input("PEDIDO")
            nf = st.number_input("Nº NF", step=1)
        with c2:
            lts = st.number_input("QTOS LTS", step=0.01)
            dt = st.date_input("DATA", date.today())
        
        forn = st.text_input("FORNECEDOR")
        cnpj = st.text_input("CNPJ")
        t_bb = st.number_input("TANQUE BB", step=0.01)
        t_be = st.number_input("TANQUE BE", step=0.01)

        if st.form_submit_button("CONCLUIR"):
            info = {"emp": emp, "ped": ped, "nf": nf, "lts": lts, "chave": "", "data": str(dt), "forn": forn, "cnpj": cnpj, "t_bb": t_bb, "t_be": t_be, "antes": 0, "depois": 0}
            res = salvar_notion(info)
            if res.status_code == 200:
                st.success("✅ Sucesso!")
                st.session_state.pg = 'inicio'
                st.rerun()
            else:
                st.error(f"Erro: {res.text}")
