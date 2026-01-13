import streamlit as st
from datetime import date
import pandas as pd
import time
import requests

# --- BLOCO 1: CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="ZION - Gestão PRO", page_icon="⛽", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #001f3f; } 
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; } 
    .texto-verde { color: #00FF00 !important; font-size: 20px !important; font-weight: bold; } 
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }
    input { background-color: white !important; color: black !important; }
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

if not st.session_state.autenticado:
    st.markdown('<h2 style="color:white; text-align:center;">🔐 ZION - Login</h2>', unsafe_allow_html=True)
    with st.form("login_zion"):
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.form_submit_button("ENTRAR"):
            if u in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[u] == s:
                st.session_state.autenticado = True
                st.session_state.user_logado = u
                st.rerun()
            else:
                st.error("Credenciais Inválidas")
    st.stop()

# --- BLOCO 6: INTEGRAÇÃO NOTION (CONFIGURADO) ---
def enviar_ao_notion(dados):
    # Credenciais fornecidas pelo usuário
    NOTION_TOKEN = "ntn_ak6353375936jhpmATGSJqAEi11rjRSqPQFu1XMPuda4xN"
    DATABASE_ID = "2e6025de7b7980cdb7f8ef8a39d424e5"

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Estrutura de dados para o Notion conforme as colunas solicitadas
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

# --- BLOCO 3: REGISTRO AVANÇADO ---
if st.session_state.tela == 'registro':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    if st.button("⬅️ LOGOUT"):
        st.session_state.clear()
        st.rerun()

    with st.form("form_registro"):
        st.markdown('<p class="texto-verde">📸 Scanner de Nota Fiscal</p>', unsafe_allow_html=True)
        st.camera_input("Scanner")
        chave_input = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"])
            forn = st.text_input("FORNECEDOR")
            cnpj_forn = st.text_input("CNPJ FORNECEDOR")
            localidade = st.text_input("CIDADE / ESTADO (NF)")
        with col2:
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY")
            valor_nf = st.number_input("VALOR TOTAL NF (R$)", step=0.01)
            nf_num = st.text_input("Nº DA NOTA")
            pedido = st.text_input("Nº PEDIDO")

        st.markdown('<p class="texto-verde">⛽ Abastecimento e Tanques</p>', unsafe_allow_html=True)
        c_real, c_bb, c_be = st.columns(3)
        qtd_realizada = c_real.number_input("REALIZADO (LTS)", step=1)
        t_bb = c_bb.number_input("TANQUE BB (m³)", step=0.01)
        t_be = c_be.number_input("TANQUE BE (m³)", step=0.01)

        if st.form_submit_button("CONFERIR E EDITAR DADOS"):
            st.session_state.dados_nf = {
                "emp": emp, "pedido": pedido, "nf": nf_num, "qtd": qtd_realizada,
                "dt": dt, "forn": forn, "cnpj": cnpj_forn, "valor": valor_nf,
                "local": localidade, "chave": chave_input, "t_bb": t_bb, "t_be": t_be
            }
            st.session_state.tela = 'edicao'
            st.rerun()

# --- BLOCO 4: CONFERÊNCIA E ENVIO ---
elif st.session_state.tela == 'edicao':
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    d = st.session_state.dados_nf
    with st.form("form_edicao"):
        st.markdown('<p class="texto-verde">Confirme as informações:</p>', unsafe_allow_html=True)
        st.write(f"**Empurrador:** {d['emp']} | **NF:** {d['nf']}")
        st.write(f"**Realizado:** {d['qtd']} LTS | **Data:** {d['dt'].strftime('%d/%m/%Y')}")
        
        st.write("---")
        st.markdown('<p class="texto-verde">📍 Mapa de Localização</p>', unsafe_allow_html=True)
        st.map(pd.DataFrame({'lat': [-1.4000], 'lon': [-48.3963]}), zoom=14)

        if st.form_submit_button("✅ SALVAR NO NOTION"):
            if enviar_ao_notion(d):
                st.success("DADOS SALVOS COM SUCESSO!")
                time.sleep(2)
                st.session_state.tela = 'sucesso'
                st.rerun()
            else:
                st.error("Erro ao enviar para o Notion. Verifique o Token/ID.")

    if st.button("🔄 VOLTAR"):
        st.session_state.tela = 'registro'
        st.rerun()

# --- BLOCO 5: SUCESSO ---
elif st.session_state.tela == 'sucesso':
    st.balloons()
    st.markdown('<h2 style="color:white; text-align:center;">✅ Operação Concluída!</h2>', unsafe_allow_html=True)
    if st.button("🏠 NOVO LANÇAMENTO"):
        st.session_state.dados_nf = {}
        st.session_state.tela = 'registro'
        st.rerun()
    if st.button("🔐 LOGOUT"):
        st.session_state.clear()
        st.rerun()
