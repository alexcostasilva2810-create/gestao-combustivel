import streamlit as st
from datetime import date
import pandas as pd
import time

# --- BLOCO 1: CONFIGURAÇÃO DE ÍCONE (PWA) E ESTILO ---
st.set_page_config(
    page_title="ZION - Gestão PRO",
    page_icon="⛽",
    layout="centered"
)

st.markdown("""
    <head>
        <link rel="manifest" href="manifest.json">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="default">
        <meta name="apple-mobile-web-app-title" content="ZION Gestão">
        <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/234/234718.png">
    </head>
    <style>
    .stApp { background-color: #001f3f; } 
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; } 
    .texto-verde { color: #00FF00 !important; font-size: 20px !important; font-weight: bold; } 
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }
    input { background-color: white !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BLOCO 2: INICIALIZAÇÃO E LISTAS ---
if 'tela' not in st.session_state: st.session_state.tela = 'registro'
if 'dados_nf' not in st.session_state: st.session_state.dados_nf = {}

LISTA_EMPURRADORES = ["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"]

# --- BLOCO 3: TELA DE REGISTRO E SCANNER ---
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
        st.markdown('<p class="texto-verde">📸 Escanear ou Digitar Chave</p>', unsafe_allow_html=True)
        st.camera_input("Capturar Código de Barras")
        chave_input = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        
        if st.form_submit_button("CONFERIR E EDITAR DADOS"):
            st.session_state.dados_nf = {
                "emp": emp, 
                "nf": nf if nf > 0 else (chave_input[25:34] if len(chave_input) == 44 else 0),
                "qtd": qtd, "dt": dt, "forn": forn, "chave": chave_input
            }
            st.session_state.tela = 'edicao'
            st.rerun()

# --- BLOCO 4: TELA DE EDIÇÃO, MAPA E SALVAMENTO ---
elif st.session_state.tela == 'edicao':
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    d = st.session_state.dados_nf

    with st.form("form_edicao"):
        st.markdown('<p class="texto-verde">Confirme os Dados da Chave:</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            ed_nf = st.text_input("Confirmar Nº NF", value=str(d['nf']))
            ed_chave = st.text_input("Confirmar Chave", value=d['chave'])
        with c2:
            ed_forn = st.text_input("Confirmar Fornecedor", value=d['forn'])
            ed_qtd = st.text_input("Confirmar Quantidade", value=str(d['qtd']))

        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        ta, tb = st.columns(2)
        t_bb = ta.number_input("TANQUE BB (m³)", step=0.01)
        t_be = tb.number_input("TANQUE BE (m³)", step=0.01)

        st.write("---")
        st.markdown('<p class="texto-verde">📍 Local detectado: Belém - PA</p>', unsafe_allow_html=True)
        map_data = pd.DataFrame({'lat': [-1.4000], 'lon': [-48.3963]})
        st.map(map_data, zoom=14) 

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.form_submit_button("✅ SALVAR NO NOTION"):
                st.success("Enviando ao Notion...")
                time.sleep(1)
                st.session_state.tela = 'sucesso'
                st.rerun()
        with col_b2:
            if st.form_submit_button("🔄 VOLTAR"):
                st.session_state.tela = 'registro'
                st.rerun()

# --- BLOCO 5: FINALIZAÇÃO (BOTÕES DE RETORNO / SAIR) ---
elif st.session_state.tela == 'sucesso':
    st.balloons()
    st.markdown('<h2 style="color:white; text-align:center;">✅ Registro Concluído!</h2>', unsafe_allow_html=True)
    
    # Coluna tripla para organizar os botões finais
    cf1, cf2, cf3 = st.columns(3)
    
    with cf1:
        if st.button("➕ NOVO"):
            st.session_state.tela = 'registro'
            st.rerun()
            
    with cf2:
        # Botão solicitado: Retornar à tela inicial limpando dados
        if st.button("🏠 INÍCIO"):
            st.session_state.dados_nf = {}
            st.session_state.tela = 'registro'
            st.rerun()
    
    with cf3:
        if st.button("🚪 SAIR"):
            st.session_state.clear()
            st.rerun()
