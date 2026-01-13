import streamlit as st
import requests
from datetime import date
import base64

# --- BLOCO 1: CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Zion Combustível", page_icon="⛽", layout="centered")

# Função para converter imagem local para Base64 (mais garantido que link)
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

def aplicar_design():
    # Tenta carregar a imagem de fundo do seu GitHub
    fundo_base64 = get_base64_of_bin_file("plataforma.jpg")
    
    if fundo_base64:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{fundo_base64}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        .stButton>button { width: 100%; height: 3.5em; background-color: #007bff; color: white; font-weight: bold; border-radius: 12px; border: none; }
        h1, h2, h3, p { color: white !important; text-shadow: 2px 2px 8px #000000; text-align: center; }
        .stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: rgba(255, 255, 255, 0.9) !important; color: black !important; }
        </style>
        """, unsafe_allow_html=True)

aplicar_design()

# --- BLOCO 2: INTEGRAÇÃO NOTION ---
try:
    NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
    DATABASE_ID = st.secrets["DATABASE_ID"]
except:
    st.error("Erro: Verifique os Secrets no Streamlit Cloud.")
    st.stop()

def salvar_no_notion(dados):
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

# --- BLOCO 3: INTERFACE ---
if 'pg' not in st.session_state: st.session_state.pg = 'inicio'

if st.session_state.pg == 'inicio':
    # Exibe a logo ZION.JPG
    try:
        st.image("ZION.JPG", width=250)
    except:
        st.write("### ZION TECNOLOGIA")
    
    st.markdown("<h1>SISTEMA DE RECEBIMENTO</h1>")
    if st.button("INICIAR NOVO REGISTRO"):
        st.session_state.pg = 'form'
        st.rerun()

elif st.session_state.pg == 'form':
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

        if st.form_submit_button("CONCLUIR"):
            info = {"emp": emp, "ped": ped, "nf": nf, "lts": lts, "chave": chave, "data": str(dt), "forn": forn, "cnpj": cnpj, "t_bb": t_bb, "t_be": t_be, "antes": 0, "depois": 0}
            res = salvar_no_notion(info)
            if res.status_code == 200:
                st.balloons()
                st.success("Registrado!")
                st.session_state.pg = 'inicio'
                st.rerun()
