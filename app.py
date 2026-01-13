import streamlit as st
from datetime import date
import pandas as pd
import time

# --- BLOCO 1: CONFIGURAÇÕES GERAIS E ESTILO ---
# Define o tema visual, o ícone para celular e o fundo azul marinho.
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

# --- BLOCO 2: GOVERNANÇA E CONTROLE DE ACESSO ---
# Gerencia os 13 usuários e mantém a sessão ativa ou encerrada.
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

# --- BLOCO 3: TELA DE REGISTRO INICIAL ---
# Captura os dados principais e a chave da NF. Formato de data ajustado.
if st.session_state.tela == 'registro':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_registro"):
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"])
            pedido = st.text_input("Nº PEDIDO")
            nf = st.number_input("Nº NF", step=1, format="%d")
        with col2:
            qtd = st.number_input("QUANTIDADE (LTS)", step=1)
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY") # Ajuste de data
            forn = st.text_input("FORNECEDOR")

        st.write("---")
        chave_input = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        
        if st.form_submit_button("CONFERIR E EDITAR DADOS"):
            st.session_state.dados_nf = {
                "emp": emp, "pedido": pedido, "nf": nf, 
                "qtd": qtd, "dt": dt, "forn": forn, "chave": chave_input
            }
            st.session_state.tela = 'edicao'
            st.rerun()

# --- BLOCO 4: TELA DE CONFERÊNCIA E MAPA ---
# Permite edição final e mostra a geolocalização abaixo do formulário.
elif st.session_state.tela == 'edicao':
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    d = st.session_state.dados_nf

    with st.form("form_edicao"):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Confirmar Nº NF", value=str(d['nf']))
            st.text_input("Confirmar Chave", value=d['chave'])
        with c2:
            st.text_input("Confirmar Fornecedor", value=d['forn'])
            st.text_input("Confirmar Quantidade", value=str(d['qtd']))

        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        t_bb = st.number_input("TANQUE BB (m³)", step=0.01)
        t_be = st.number_input("TANQUE BE (m³)", step=0.01)

        st.write("---")
        st.markdown('<p class="texto-verde">📍 Localização Detectada</p>', unsafe_allow_html=True)
        # Exibição do mapa reduzido conforme solicitado
        st.map(pd.DataFrame({'lat': [-1.4000], 'lon': [-48.3963]}), zoom=14)

        if st.form_submit_button("✅ SALVAR NO NOTION"):
            st.session_state.tela = 'sucesso'
            st.rerun()

    if st.button("🔄 VOLTAR PARA EDIÇÃO"):
        st.session_state.tela = 'registro'
        st.rerun()

# --- BLOCO 5: TELA DE SUCESSO E NAVEGAÇÃO FINAL ---
# Oferece as opções de novo lançamento ou retorno ao login.
elif st.session_state.tela == 'sucesso':
    st.balloons()
    st.markdown('<h2 style="color:white; text-align:center;">✅ Operação Concluída!</h2>', unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        if st.button("➕ NOVO LANÇAMENTO"):
            st.session_state.dados_nf = {}
            st.session_state.tela = 'registro'
            st.rerun()
    with col_f2:
        if st.button("🔐 RETORNAR AO LOGIN"):
            st.session_state.clear()
            st.rerun()

# --- BLOCO 6: FUNÇÕES DE INTEGRAÇÃO (BACKEND) ---
# Espaço reservado para a conexão futura com a API do Notion.
def enviar_ao_notion(dados):
    # Lógica de integração será inserida aqui
    pass
