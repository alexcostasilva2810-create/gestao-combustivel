import streamlit as st
from datetime import date
import pandas as pd
import time
import requests #

# --- BLOCO 1: CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="ZION - Gestão PRO", page_icon="⛽", layout="centered")

# CSS para carregar suas imagens locais: plataforma.jpg como fundo
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("app/static/plataforma.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 31, 63, 0.85);
        z-index: -1;
    }}
    .login-box {{
        background-color: rgba(255, 255, 255, 0.1);
        padding: 40px;
        border-radius: 20px;
        border: 2px solid #007bff;
        backdrop-filter: blur(15px);
        text-align: center;
    }}
    label, .stWidgetLabel p {{ color: #007bff !important; font-weight: bold; }}
    .texto-verde {{ color: #00FF00 !important; font-weight: bold; }}
    .stButton>button {{ width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }}
    </style>
    """, unsafe_allow_html=True)

# --- BLOCO 2: GOVERNANÇA (13 USUÁRIOS) ---
USUARIOS_AUTORIZADOS = {
    "admin": "zion01", "gestor": "zion02", "usuario1": "123", "usuario2": "234",
    "usuario3": "345", "usuario4": "456", "usuario5": "567", "usuario6": "678",
    "usuario7": "789", "usuario8": "890", "usuario9": "901", "usuario10": "012",
    "usuario11": "124"
}

if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'registro'
if 'dados_nf' not in st.session_state: st.session_state.dados_nf = {}

# --- BLOCO 3: LOGIN COM LOGO ZION.jpg ---
if not st.session_state.autenticado:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    # Carregando sua logo da biblioteca
    st.image("ZION.jpg", width=200) 
    st.markdown('<h1 style="color:white;">ZION GESTÃO PRO</h1>', unsafe_allow_html=True)
    
    with st.form("login_zion"):
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.form_submit_button("ENTRAR NO SISTEMA"): #
            if u in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[u] == s:
                st.session_state.autenticado = True
                st.session_state.user_logado = u
                st.rerun()
            else:
                st.error("Credenciais Inválidas")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- INTEGRAÇÃO NOTION ---
def enviar_ao_notion(dados):
    NOTION_TOKEN = "ntn_ak6353375936jhpmATGSJqAEi11rjRSqPQFu1XMPuda4xN"
    DATABASE_ID = "2e6025de7b7980cdb7f8ef8a39d424e5"
    url = "https://api.notion.com/v1/pages"
    headers = {"Authorization": f"Bearer {NOTION_TOKEN}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Empurrador": {"title": [{"text": {"content": dados['emp']}}]},
            "NF": {"rich_text": [{"text": {"content": str(dados['nf'])}}]},
            "Fornecedor": {"rich_text": [{"text": {"content": dados['forn']}}]},
            "CNPJ": {"rich_text": [{"text": {"content": dados['cnpj']}}]},
            "Valor NF": {"number": float(dados['valor'])},
            "Localidade": {"rich_text": [{"text": {"content": dados['local']}}]},
            "Realizado": {"number": float(dados['qtd'])},
            "Tanque BB": {"number": float(dados['t_bb'])},
            "Tanque BE": {"number": float(dados['t_be'])},
            "Data": {"date": {"start": dados['dt'].isoformat()}},
            "Chave": {"rich_text": [{"text": {"content": dados['chave']}}]}
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code == 200

# --- BLOCO 4: REGISTRO ---
if st.session_state.tela == 'registro':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_reg"):
        st.markdown('<p class="texto-verde">📸 Scanner de Nota Fiscal</p>', unsafe_allow_html=True)
        st.camera_input("Scanner")
        chave = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"])
            forn = st.text_input("FORNECEDOR")
            cnpj = st.text_input("CNPJ FORNECEDOR")
            local = st.text_input("CIDADE / ESTADO (NF)")
        with col2:
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY") #
            val = st.number_input("VALOR TOTAL NF (R$)", step=0.01)
            n_nf = st.text_input("Nº DA NOTA")
            ped = st.text_input("Nº PEDIDO")

        st.markdown('<p class="texto-verde">⛽ Realizado e Tanques</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        q_real = c1.number_input("REALIZADO (LTS)", step=1)
        v_bb = c2.number_input("TANQUE BB (m³)", step=0.01)
        v_be = c3.number_input("TANQUE BE (m³)", step=0.01)

        if st.form_submit_button("CONFERIR DADOS"): #
            st.session_state.dados_nf = {"emp":emp,"pedido":ped,"nf":n_nf,"qtd":q_real,"dt":dt,"forn":forn,"cnpj":cnpj,"valor":val,"local":local,"chave":chave,"t_bb":v_bb,"t_be":v_be}
            st.session_state.tela = 'edicao'
            st.rerun()

# --- BLOCO 5: CONFERÊNCIA ---
elif st.session_state.tela == 'edicao':
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    d = st.session_state.dados_nf
    with st.form("form_ed"):
        st.write(f"**Empurrador:** {d['emp']} | **Nota:** {d['nf']}")
        st.write(f"**Realizado:** {d['qtd']} LTS | **Data:** {d['dt'].strftime('%d/%m/%Y')}")
        if st.form_submit_button("✅ SALVAR NO NOTION"): #
            if enviar_ao_notion(d):
                st.session_state.tela = 'sucesso'
                st.rerun()
            else: st.error("Erro na integração.")
    if st.button("🔄 VOLTAR"):
        st.session_state.tela = 'registro'
        st.rerun()

# --- BLOCO 6: SUCESSO ---
elif st.session_state.tela == 'sucesso':
    st.balloons()
    st.markdown('<h2 style="color:white; text-align:center;">✅ Registro Concluído!</h2>', unsafe_allow_html=True)
    if st.button("🏠 NOVO LANÇAMENTO"):
        st.session_state.tela = 'registro'
        st.rerun()
