import streamlit as st
import requests
from datetime import date
import base64
import os

# --- BLOCO 1: CONFIGURAÇÕES E CARREGAMENTO DE IMAGENS ---
st.set_page_config(page_title="ZION Combustível", page_icon="⛽", layout="centered")

# Função para converter imagem do GitHub para formato que o navegador entende
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Carrega os arquivos que você subiu no repositório
fundo_64 = get_image_base64("plataforma.jpg")
logo_64 = get_image_base64("ZION.JPG")

# --- BLOCO 2: ESTILO VISUAL (DESIGN APROVADO) ---
estilo_fundo = ""
if fundo_64:
    estilo_fundo = f"""
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("data:image/jpg;base64,{fundo_64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    """

st.markdown(f"""
    <style>
    .stApp {{
        {estilo_fundo}
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
        display: block;
        margin: 20px auto;
    }}
    .logo-img {{
        display: block;
        margin: auto;
        width: 200px;
        border-radius: 10px;
        filter: drop-shadow(0 0 10px rgba(0,0,0,0.5));
    }}
    /* Estilo para inputs ficarem legíveis */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- BLOCO 3: INTEGRAÇÃO NOTION ---
try:
    NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
    DATABASE_ID = st.secrets["DATABASE_ID"]
except:
    st.error("Erro nos Secrets do Streamlit! Verifique se NOTION_TOKEN e DATABASE_ID estão preenchidos.")
    st.stop()

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

# --- BLOCO 4: NAVEGAÇÃO DAS TELAS ---
if 'pg' not in st.session_state: st.session_state.pg = 'inicio'

if st.session_state.pg == 'inicio':
    # Exibe a logo se o arquivo ZION.JPG existir
    if logo_64:
        st.markdown(f'<img src="data:image/jpg;base64,{logo_64}" class="logo-img">', unsafe_allow_html=True)
    
    st.markdown("<h1>ZION Combustível</h1>")
    st.markdown("<h3>Sistema de Registro de Abastecimento</h3>")
    
    if st.button("INICIAR REGISTRO"):
        st.session_state.pg = 'form'
        st.rerun()

elif st.session_state.pg == 'form':
    st.markdown("<h2>📝 Dados do Abastecimento</h2>")
    with st.form("zion_form"):
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

        if st.form_submit_button("CONCLUIR E SALVAR"):
            info = {"emp": emp, "ped": ped, "nf": nf, "lts": lts, "chave": chave, "data": str(dt), "forn": forn, "cnpj": cnpj, "t_bb": t_bb, "t_be": t_be, "antes": 0, "depois": 0}
            res = salvar_no_notion(info)
            if res.status_code == 200:
                st.balloons()
                st.success("✅ Enviado com sucesso!")
                st.session_state.pg = 'inicio'
                st.rerun()
            else:
                st.error("Erro ao enviar. Verifique a conexão com o Notion.")
