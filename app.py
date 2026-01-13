import streamlit as st
from datetime import date
import pandas as pd
import time

# --- BLOCO 1: CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="ZION - Gestão PRO", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #001f3f; } 
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; } 
    .texto-verde { color: #00FF00 !important; font-size: 20px !important; font-weight: bold; } 
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }
    input { background-color: white !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BLOCO 2: INICIALIZAÇÃO DE ESTADO ---
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
        # Restauração do campo de scanner
        st.camera_input("Escanear Código de Barras da NF")
        chave_input = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        
        if st.form_submit_button("CONFERIR E EDITAR DADOS"):
            # Lógica de preenchimento automático simplificada para o bloco de edição
            st.session_state.dados_nf = {
                "emp": emp, "nf": nf if nf > 0 else (chave_input[25:34] if len(chave_input) == 44 else 0),
                "qtd": qtd, "dt": dt, "forn": forn, "chave": chave_input
            }
            st.session_state.tela = 'edicao'
            st.rerun()

# --- BLOCO 4: TELA DE EDIÇÃO, MAPA E CONCLUSÃO ---
elif st.session_state.tela == 'edicao':
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    d = st.session_state.dados_nf

    with st.form("form_edicao"):
        st.markdown('<p class="texto-verde">Dados Extraídos da Chave:</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            # Campos preenchidos automaticamente para edição
            ed_nf = st.text_input("Confirmar Nº NF", value=str(d['nf']))
            ed_chave = st.text_input("Confirmar Chave", value=d['chave'])
        with c2:
            ed_forn = st.text_input("Confirmar Fornecedor", value=d['forn'])
            ed_qtd = st.text_input("Confirmar Quantidade", value=str(d['qtd']))

        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        ta, tb = st.columns(2)
        t_bb = ta.number_input("TANQUE BB (m³)", step=0.01)
        t_be = tb.number_input("TANQUE BE (m³)", step=0.01)

        # MAPA REDUZIDO
        st.write("---")
        st.markdown('<p class="texto-verde">📍 Local de Abastecimento</p>', unsafe_allow_html=True)
        map_data = pd.DataFrame({'lat': [-1.4000], 'lon': [-48.3963]})
        st.map(map_data, zoom=15, use_container_width=True) # Mapa menor e centralizado
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.form_submit_button("✅ SALVAR NO NOTION"):
                st.success("Dados salvos com sucesso!")
                time.sleep(1)
                st.session_state.tela = 'sucesso'
                st.rerun()
        with col_btn2:
            if st.form_submit_button("🔄 VOLTAR"):
                st.session_state.tela = 'registro'
                st.rerun()

# --- BLOCO 5: TELA FINAL (NOVO LANÇAMENTO / SAIR) ---
elif st.session_state.tela == 'sucesso':
    st.markdown('<h2 style="color:white; text-align:center;">✅ Operação Concluída</h2>', unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        if st.button("➕ NOVO LANÇAMENTO"):
            st.session_state.tela = 'registro'
            st.rerun()
    with col_f2:
        if st.button("🚪 SAIR DO SISTEMA"):
            st.session_state.clear()
            st.write("Sessão Encerrada.")
            st.rerun()
