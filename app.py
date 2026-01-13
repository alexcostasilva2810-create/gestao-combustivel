import streamlit as st
import requests
from datetime import date
import base64
import os
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ZION - Sistema de Gestão", page_icon="⛽", layout="centered")

def carregar_imagem_base64(caminho):
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Carregando arquivos do GitHub
logo_64 = carregar_imagem_base64("ZION.jpg")
fundo_64 = carregar_imagem_base64("plataforma.jpg")

# --- 2. ESTILO VISUAL ---
fundo_estilo = f"""
    background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
    url("data:image/jpg;base64,{fundo_64}");
    background-size: cover; background-position: center; background-attachment: fixed;
""" if fundo_64 else "background-color: #1E1E1E;"

st.markdown(f"""
    <style>
    .stApp {{ {fundo_estilo} }}
    .container-central {{ display: flex; flex-direction: column; align-items: center; text-align: center; }}
    .titulo-zion {{ color: white !important; font-size: 38px !important; font-weight: bold; text-shadow: 2px 2px 4px #000; }}
    .stButton>button {{ width: 100%; max-width: 300px; height: 3.5em; background-color: #007bff; color: white; font-weight: bold; border-radius: 12px; }}
    /* Ajuste para inputs no formulário */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {{ background-color: white !important; color: black !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. GOVERNANÇA (13 VAGAS) ---
USUARIOS = {
    "admin": "zion123", "user2": "senha2", "user3": "senha3", "user4": "senha4",
    "user5": "senha5", "user6": "senha6", "user7": "senha7", "user8": "senha8",
    "user9": "senha9", "user10": "senha10", "user11": "senha11", "user12": "senha12",
    "user13": "senha13"
}

# --- 4. FUNÇÃO SALVAR NO NOTION ---
def salvar_notion(dados):
    try:
        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {st.secrets['NOTION_TOKEN']}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        payload = {
            "parent": {"database_id": st.secrets["DATABASE_ID"]},
            "properties": {
                "EMPURRADOR": {"title": [{"text": {"content": dados['emp']}}]},
                "PEDIDO": {"rich_text": [{"text": {"content": dados['ped']}}]},
                "Nº NF": {"number": dados['nf']},
                "QTOS LTS": {"number": dados['lts']},
                "REALIZADO": {"date": {"start": dados['data']}},
                "FORNECEDOR": {"rich_text": [{"text": {"content": dados['forn']}}]},
                "TANQUE BB": {"number": dados['t_bb']},
                "TANQUE BE": {"number": dados['t_be']}
            }
        }
        res = requests.post(url, headers=headers, json=payload)
        return res.status_code == 200
    except:
        return False

# --- 5. JANELA FLUTUANTE DE LOGIN ---
@st.dialog("Acesso ao Sistema")
def login_modal():
    st.write("Identifique-se para registrar abastecimentos.")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("ENTRAR"):
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            st.session_state.autenticado = True
            st.session_state.user = usuario
            st.rerun()
        else:
            st.error("Usuário ou Senha inválidos.")

# --- 6. LÓGICA DE TELAS ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'inicio'

# TELA 01: LOGIN
if not st.session_state.autenticado:
    st.markdown('<div class="container-central">', unsafe_allow_html=True)
    if logo_64:
        st.markdown(f'<img src="data:image/jpg;base64,{logo_64}" width="250" style="border-radius:20px;">', unsafe_allow_html=True)
    st.markdown('<p class="titulo-zion">ZION TECNOLOGIA</p>', unsafe_allow_html=True)
    if st.button("INICIAR ACESSO"):
        login_modal()
    st.markdown('</div>', unsafe_allow_html=True)

# TELA 02: BEM-VINDO (PÓS-LOGIN)
elif st.session_state.tela == 'inicio':
    st.markdown('<div class="container-central">', unsafe_allow_html=True)
    if logo_64:
        st.markdown(f'<img src="data:image/jpg;base64,{logo_64}" width="200" style="border-radius:20px;">', unsafe_allow_html=True)
    st.markdown('<p class="titulo-zion">Bem vindo ao Zion !!</p>', unsafe_allow_html=True)
    st.write(f"Operador: **{st.session_state.user}**")
    
    if st.button("ABRIR FORMULÁRIO DE REGISTRO"):
        st.session_state.tela = 'form'
        st.rerun()
    
    if st.button("Sair"):
        st.session_state.autenticado = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# TELA 03: FORMULÁRIO COMPLETO
elif st.session_state.tela == 'form':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_completo"):
        c1, c2 = st.columns(2)
        with c1:
            emp = st.text_input("EMPURRADOR")
            ped = st.text_input("Nº PEDIDO")
            nf = st.number_input("Nº NF", step=1)
        with c2:
            lts = st.number_input("QUANTIDADE (LTS)", step=0.1)
            dt = st.date_input("DATA", date.today())
            forn = st.text_input("FORNECEDOR")
        
        st.markdown("---")
        st.write("📊 **Níveis de Tanque**")
        col_a, col_b = st.columns(2)
        with col_a:
            t_bb = st.number_input("TANQUE BB (m³)", step=0.01)
        with col_b:
            t_be = st.number_input("TANQUE BE (m³)", step=0.01)

        if st.form_submit_button("CONCLUIR E ENVIAR AO NOTION"):
            dados = {'emp': emp, 'ped': ped, 'nf': nf, 'lts': lts, 'data': str(dt), 'forn': forn, 't_bb': t_bb, 't_be': t_be}
            if salvar_notion(dados):
                st.success("✅ Dados gravados com sucesso!")
                time.sleep(2)
                st.session_state.tela = 'inicio'
                st.rerun()
            else:
                st.error("❌ Erro ao enviar para o Notion. Verifique seus Secrets.")

    if st.button("Voltar"):
        st.session_state.tela = 'inicio'
        st.rerun()
