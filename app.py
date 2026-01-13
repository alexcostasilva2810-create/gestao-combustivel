import streamlit as st
from datetime import date
import pandas as pd
import time

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="ZION - Gestão", layout="centered")

# Estilo para garantir rótulos azuis e títulos verdes
st.markdown("""
    <style>
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; }
    .texto-verde { color: #00FF00 !important; font-size: 20px !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3em; }
    .btn-azul>button { background-color: #007bff; color: white; }
    .btn-vermelho>button { background-color: #ff4b4b; color: white; }
    input { background-color: white !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DO ESTADO (Prevenir tela em branco) ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = True # Mantenha True para testes
if 'tela' not in st.session_state: st.session_state.tela = 'registro'
if 'banco_dados' not in st.session_state: st.session_state.banco_dados = []
if 'chave_temp' not in st.session_state: st.session_state.chave_temp = ""

# Lista de Empuradores
EMPURRADORES = ["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"]

# --- 3. LOGICA DE NAVEGAÇÃO ---

# TELA 1: REGISTRO DE DADOS
if st.session_state.tela == 'registro':
    st.markdown('<h2 style="text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_captura"):
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=EMPURRADORES)
            pedido = st.text_input("Nº PEDIDO")
            nf = st.number_input("Nº NF", step=1, format="%d")
        with col2:
            qtd = st.number_input("QUANTIDADE (LTS)", step=1, format="%d")
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY")
            forn = st.text_input("FORNECEDOR")
        
        st.write("---")
        st.write("📸 **Captura da Chave**")
        chave = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        
        # Botão para processar e ir para edição
        if st.form_submit_button("CONFERIR E EDITAR DADOS"):
            st.session_state.dados_conferencia = {
                "empurrador": emp, "pedido": pedido, "nf": nf, 
                "qtd": qtd, "data": dt, "fornecedor": forn, "chave": chave
            }
            st.session_state.tela = 'conferencia'
            st.rerun()

# TELA 2: CONFERÊNCIA E EDIÇÃO (A "Outra Tela")
elif st.session_state.tela == 'conferencia':
    st.markdown('<h2 style="text-align:center;">🔍 Conferência de Dados</h2>', unsafe_allow_html=True)
    d = st.session_state.dados_conferencia
    
    with st.form("form_edicao"):
        st.markdown('<p class="texto-verde">Edite as informações se necessário</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            edit_nf = st.text_input("Confirmar Nº NF", value=str(d['nf']))
            edit_chave = st.text_input("Confirmar Chave", value=d['chave'])
        with c2:
            edit_forn = st.text_input("Confirmar Fornecedor", value=d['fornecedor'])
            edit_qtd = st.text_input("Confirmar Quantidade (LTS)", value=str(d['qtd']))

        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        ca, cb = st.columns(2)
        t_bb = ca.number_input("TANQUE BB (m³)", step=0.01)
        t_be = cb.number_input("TANQUE BE (m³)", step=0.01)

        if st.form_submit_button("✅ TUDO CERTO! SALVAR NO NOTION"):
            # Salva no "banco" e muda de tela
            novo = {
                "Data": d['data'].strftime("%d/%m/%Y"),
                "Empurrador": d['empurrador'],
                "NF": edit_nf,
                "Qtd": edit_qtd,
                "Chave": edit_chave,
                "BB": t_bb, "BE": t_be
            }
            st.session_state.banco_dados.append(novo)
            st.session_state.tela = 'visualizacao'
            st.rerun()
    
    if st.button("Voltar para Registro"):
        st.session_state.tela = 'registro'
        st.rerun()

# TELA 3: ÚLTIMOS LANÇAMENTOS
elif st.session_state.tela == 'visualizacao':
    st.markdown('<h2 style="text-align:center;">📋 Lançamentos Realizados</h2>', unsafe_allow_html=True)
    
    if st.session_state.banco_dados:
        df = pd.DataFrame(st.session_state.banco_dados)
        st.dataframe(df, use_container_width=True) # Exibe a tabela do Notion
    else:
        st.warning("Nenhum dado encontrado.")

    st.write("---")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
        if st.button("➕ NOVO LANÇAMENTO"):
            st.session_state.tela = 'registro'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_v2:
        st.markdown('<div class="btn-vermelho">', unsafe_allow_html=True)
        if st.button("🚪 SAIR DO SISTEMA"):
            st.session_state.autenticado = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
