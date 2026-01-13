import streamlit as st
import requests
from datetime import date

# --- BLOCO 1: CONFIGURAÇÃO ---
st.set_page_config(page_title="Zion Combustível", page_icon="⛽", layout="centered")

def aplicar_estilo():
    # Usando links diretos do seu repositório
    img_fundo = "https://raw.githubusercontent.com/alexcostasilva2810-create/gestao-combustivel/main/plataforma.jpg"
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("{img_fundo}");
            background-size: cover;
            background-position: center;
        }}
        .stButton>button {{ width: 100%; height: 3em; background-color: #007bff; color: white; font-weight: bold; border-radius: 10px; }}
        h1, h2, h3, p {{ color: white !important; text-shadow: 2px 2px 4px #000; text-align: center; }}
        </style>
        """, unsafe_allow_html=True)

aplicar_estilo()

# --- BLOCO 2: SEGURANÇA ---
try:
    NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
    DATABASE_ID = st.secrets["DATABASE_ID"]
except Exception:
    st.error("Erro nos Secrets! Verifique se NOTION_TOKEN e DATABASE_ID estão preenchidos.")
    st.stop()

def enviar_ao_notion(dados):
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

# --- BLOCO 3: NAVEGAÇÃO ---
if 'tela' not in st.session_state:
    st.session_state.tela = 'inicial'

if st.session_state.tela == 'inicial':
    logo_url = "https://raw.githubusercontent.com/alexcostasilva2810-create/gestao-combustivel/main/ZION.JPG"
    # Se a logo não existir, ele mostra apenas o título
    try:
        st.image(logo_url, width=280)
    except:
        st.write("### LOGO ZION")
    
    st.markdown("<h1>SISTEMA DE RECEBIMENTO</h1>")
    if st.button("INICIAR REGISTRO"):
        st.session_state.tela = 'formulario'
        st.rerun()

elif st.session_state.tela == 'formulario':
    st.markdown("<h2>📝 Dados do Abastecimento</h2>")
    with st.form("form_comb", clear_on_submit=True):
        emp = st.text_input("EMPURRADOR")
        col1, col2 = st.columns(2)
        with col1:
            ped = st.text_input("PEDIDO")
            nf = st.number_input("Nº NF", step=1)
            lts = st.number_input("QTOS LTS", step=0.01)
        with col2:
            chave = st.text_input("CHAVE DA NF")
            dt = st.date_input("REALIZADO", date.today())
            forn = st.text_input("FORNECEDOR")
        
        cnpj = st.text_input("CNPJ")
        t_bb = st.number_input("TANQUE BB", step=0.01)
        t_be = st.number_input("TANQUE BE", step=0.01)

        if st.form_submit_button("CONCLUIR E SALVAR"):
            info = {"emp": emp, "ped": ped, "nf": nf, "lts": lts, "chave": chave, "data": str(dt), "forn": forn, "cnpj": cnpj, "t_bb": t_bb, "t_be": t_be, "antes": 0, "depois": 0}
            res = enviar_ao_notion(info)
            if res.status_code == 200:
                st.success("✅ Enviado!")
                st.session_state.tela = 'inicial'
                st.rerun()
            else:
                st.error("Erro ao enviar. Verifique a conexão com Notion.")
