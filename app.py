import streamlit as st
import requests
from datetime import date

# --- BLOCO 1: ESTILO E IMAGEM DE FUNDO ---
st.set_page_config(page_title="Zion Combustível", page_icon="⛽", layout="centered")

# CSS para forçar o plano de fundo usando o arquivo 'plataforma.jpg' que está no seu GitHub
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("https://raw.githubusercontent.com/alexcostasilva2810-create/gestao-combustivel/main/plataforma.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    h1, h2, h3, p, label { color: white !important; text-shadow: 2px 2px 4px #000; text-align: center; }
    .stButton>button { width: 100%; height: 3.5em; background-color: #007bff; color: white; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- BLOCO 2: INTEGRAÇÃO NOTION ---
NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
DATABASE_ID = st.secrets["DATABASE_ID"]

def salvar_no_notion(dados):
    url = "https://api.notion.com/v1/pages"
    headers = {"Authorization": f"Bearer {NOTION_TOKEN}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
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

# --- BLOCO 3: TELAS (INICIAL E FORMULÁRIO) ---
if 'tela' not in st.session_state: st.session_state.tela = 'inicial'

if st.session_state.tela == 'inicial':
    # Caminho direto para sua logo ZION.JPG no GitHub
    st.image("https://raw.githubusercontent.com/alexcostasilva2810-create/gestao-combustivel/main/ZION.JPG", width=300)
    st.markdown("<h1>SISTEMA ZION</h1>")
    if st.button("INICIAR"):
        st.session_state.tela = 'form'
        st.rerun()

elif st.session_state.tela == 'form':
    st.markdown("<h2>📝 Dados do Abastecimento</h2>")
    with st.form("zion_form", clear_on_submit=True):
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
            info = {"emp": emp, "ped": ped, "nf": nf, "lts": lts, "chave": chave, "data": str(dt), "forn": forn, "cnpj": cnpj, "t_bb": t_bb, "t_be": t_be, "antes": 0, "depois": 0}
            res = salvar_no_notion(info)
            if res.status_code == 200:
                st.balloons()
                st.success("Enviado!")
                st.session_state.tela = 'inicial'
                st.rerun()
