import streamlit as st
from datetime import date
import pandas as pd
import time

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="ZION - Gestão", layout="centered")

st.markdown("""
    <style>
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; }
    .texto-verde { color: #00FF00 !important; font-size: 20px !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    .btn-azul>button { background-color: #007bff; color: white; }
    .btn-vermelho>button { background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONTROLE DE ESTADO E NAVEGAÇÃO ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = True # Simulado para teste
if 'tela' not in st.session_state: st.session_state.tela = 'registro'
if 'dados_temp' not in st.session_state: st.session_state.dados_temp = None

# Dados de exemplo para simular o que vem do Notion
if 'banco_notion' not in st.session_state:
    st.session_state.banco_notion = []

# --- 3. LOGICA DE TELAS ---

# TELA 1 & 2: REGISTRO E CONFERÊNCIA
if st.session_state.tela == 'registro':
    st.markdown('<h2 style="text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA"])
            nf_num = st.number_input("Nº NF", step=1, format="%d")
        with col2:
            qtd = st.number_input("QUANTIDADE (LTS)", step=1, format="%d")
            data_sel = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY")

        st.write("📸 **Captura da Chave**")
        chave = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)

    if st.button("PROSSEGUIR PARA CONFERÊNCIA"):
        st.session_state.dados_temp = {"empurrador": emp, "nf": nf_num, "chave": chave, "qtd": qtd, "data": data_sel}

    # BLOCO DE EDIÇÃO (Aparece se dados_temp existir)
    if st.session_state.dados_temp:
        st.markdown('<p class="texto-verde">🔍 EDITAR E VALIDAR DADOS</p>', unsafe_allow_html=True)
        with st.expander("Editar Campos da Nota", expanded=True):
            edit_nf = st.text_input("Confirmar NF", value=str(st.session_state.dados_temp['nf']))
            edit_chave = st.text_input("Confirmar Chave", value=st.session_state.dados_temp['chave'])
        
        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        c_a, c_b = st.columns(2)
        t_bb = c_a.number_input("TANQUE BB (m³)", step=0.01)
        t_be = c_b.number_input("TANQUE BE (m³)", step=0.01)

        st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
        if st.button("✅ TUDO CERTO! SALVAR NO NOTION"):
            # Simula salvamento no banco de dados local
            novo_registro = {
                "Data": data_sel.strftime("%d/%m/%Y"),
                "Empurrador": emp,
                "NF": edit_nf,
                "Qtd": qtd,
                "Tanque BB": t_bb,
                "Tanque BE": t_be
            }
            st.session_state.banco_notion.append(novo_registro)
            st.session_state.dados_temp = None
            st.session_state.tela = 'visualizacao' # LEVA PARA A NOVA TELA
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. TELA 3: NOVA TELA DE LANÇAMENTOS (VISUALIZAÇÃO) ---
elif st.session_state.tela == 'visualizacao':
    st.markdown('<h2 style="text-align:center;">📋 Últimos Lançamentos - Notion</h2>', unsafe_allow_html=True)
    
    if st.session_state.banco_notion:
        df = pd.DataFrame(st.session_state.banco_notion)
        st.table(df) # Mostra a tabela com os dados
    else:
        st.info("Nenhum lançamento encontrado.")

    st.write("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
        if st.button("➕ NOVO LANÇAMENTO"):
            st.session_state.tela = 'registro'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="btn-vermelho">', unsafe_allow_html=True)
        if st.button("🚪 SAIR DO SISTEMA"):
            st.session_state.autenticado = False
            st.session_state.tela = 'registro'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
