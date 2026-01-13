import streamlit as st
from datetime import date
import pandas as pd
import time

# --- BLOCO 1: CONFIGURAÇÃO DE ÍCONE E ESTILO ---
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

# --- BLOCO 2: ESTADO DA SESSÃO ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'registro'
if 'dados_nf' not in st.session_state: st.session_state.dados_nf = {}

LISTA_EMPURRADORES = ["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"]

# --- BLOCO 3: TELA DE LOGIN ---
if not st.session_state.autenticado:
    st.markdown('<h2 style="color:white; text-align:center;">🔐 ZION - Acesso Restrito</h2>', unsafe_allow_html=True)
    with st.form("login"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.form_submit_button("ENTRAR NO SISTEMA"):
            if usuario == "zion" and senha == "123": # Altere aqui suas credenciais
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")
    st.stop()

# --- BLOCO 4: TELA DE REGISTRO ---
if st.session_state.tela == 'registro':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_registro"):
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=LISTA_EMPURRADORES)
            pedido = st.text_input("Nº PEDIDO")
            nf = st.number_input("Nº NF", step=1, format="%d")
        with col2:
            qtd = st.number_input("QUANTIDADE (LTS)", step=1)
            dt = st.date_input("DATA", value=date.today())
            forn = st.text_input("FORNECEDOR")

        st.write("---")
        st.markdown('<p class="texto-verde">📸 Captura da Chave</p>', unsafe_allow_html=True)
        st.camera_input("Scanner de NF")
        chave_input = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        
        if st.form_submit_button("CONFERIR E EDITAR DADOS"):
            st.session_state.dados_nf = {
                "emp": emp, "pedido": pedido, "nf": nf, 
                "qtd": qtd, "dt": dt, "forn": forn, "chave": chave_input
            }
            st.session_state.tela = 'edicao'
            st.rerun()

    if st.button("🚪 LOGOUT (SAIR)"):
        st.session_state.autenticado = False
        st.rerun()

# --- BLOCO 5: TELA DE EDIÇÃO E MAPA ---
elif st.session_state.tela == 'edicao':
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    d = st.session_state.dados_nf

    with st.form("form_edicao"):
        col_a, col_b = st.columns(2)
        with col_a:
            ed_nf = st.text_input("Confirmar Nº NF", value=str(d['nf']))
            ed_chave = st.text_input("Confirmar Chave", value=d['chave'])
        with col_b:
            ed_forn = st.text_input("Confirmar Fornecedor", value=d['forn'])
            ed_qtd = st.text_input("Confirmar Qtd (LTS)", value=str(d['qtd']))

        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        v_bb = st.number_input("TANQUE BB (m³)", step=0.01)
        v_be = st.number_input("TANQUE BE (m³)", step=0.01)

        st.write("---")
        st.markdown('<p class="texto-verde">📍 Localização</p>', unsafe_allow_html=True)
        map_df = pd.DataFrame({'lat': [-1.4000], 'lon': [-48.3963]})
        st.map(map_df, zoom=14)

        if st.form_submit_button("✅ SALVAR NO NOTION"):
            st.session_state.tela = 'sucesso'
            st.rerun()

    if st.button("🔄 VOLTAR"):
        st.session_state.tela = 'registro'
        st.rerun()

# --- BLOCO 6: TELA FINAL (BOTAO RETORNAR AO INÍCIO/LOGIN) ---
elif st.session_state.tela == 'sucesso':
    st.balloons()
    st.markdown('<h2 style="color:white; text-align:center;">✅ Registro Concluído!</h2>', unsafe_allow_html=True)
    
    st.write("---")
    # Botão para voltar à tela de Registro inicial
    if st.button("🏠 NOVO LANÇAMENTO (TELA INICIAL)"):
        st.session_state.dados_nf = {}
        st.session_state.tela = 'registro'
        st.rerun()
        
    # Botão para retornar à tela de Login
    if st.button("🔐 RETORNAR AO LOGIN"):
        st.session_state.clear()
        st.rerun()
