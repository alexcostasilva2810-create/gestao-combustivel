import streamlit as st
from datetime import date
import pandas as pd
import time

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="ZION - Gestão", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #001f3f; } /* Fundo Azul Marinho */
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; } /* Rótulos Azuis */
    .texto-verde { color: #00FF00 !important; font-size: 20px !important; font-weight: bold; } /* Verde Forte */
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3em; }
    input { background-color: white !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ESTADO DA SESSÃO ---
if 'tela' not in st.session_state: st.session_state.tela = 'registro'
if 'dados_nf' not in st.session_state: st.session_state.dados_nf = {}

# --- 3. TELA 1: CAPTURA DA CHAVE E DADOS INICIAIS ---
if st.session_state.tela == 'registro':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_registro"):
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"])
            pedido = st.text_input("Nº PEDIDO")
            nf = st.number_input("Nº NF", step=1, format="%d")
        with col2:
            qtd = st.number_input("QUANTIDADE (LTS)", step=1, format="%d")
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY")
            forn = st.text_input("FORNECEDOR")

        st.write("---")
        st.write("📸 **Captura da Chave da Nota**")
        # Local de captura da chave
        chave_capturada = st.text_input("CHAVE DA NF (Escaneie ou Digite)", max_chars=44)
        
        if st.form_submit_button("PROSSEGUIR PARA EDIÇÃO"):
            st.session_state.dados_nf = {
                "emp": emp, "pedido": pedido, "nf": nf, 
                "qtd": qtd, "dt": dt, "forn": forn, "chave": chave_capturada
            }
            st.session_state.tela = 'edicao'
            st.rerun()

# --- TELA 2: CONFERÊNCIA, EDIÇÃO E MAPA ---
elif st.session_state.tela == 'edicao':
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferir e Editar Dados</h2>', unsafe_allow_html=True)
    d = st.session_state.dados_nf

    with st.form("form_edicao"):
        st.markdown('<p class="texto-verde">Confirme as informações da Chave</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            # Local onde o usuário edita os dados da chave
            nova_nf = st.text_input("Confirmar Nº NF", value=str(d['nf']))
            nova_chave = st.text_input("Confirmar Chave de Acesso", value=d['chave'])
        with c2:
            novo_forn = st.text_input("Confirmar Fornecedor", value=d['forn'])
            nova_qtd = st.text_input("Confirmar Qtd (LTS)", value=str(d['qtd']))

        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        ca, cb = st.columns(2)
        t_bb = ca.number_input("TANQUE BB (m³)", step=0.01)
        t_be = cb.number_input("TANQUE BE (m³)", step=0.01)

        # --- MAPA ABAIXO DO FORMULÁRIO DE EDIÇÃO ---
        st.write("---")
        st.markdown('<p class="texto-verde">📍 Localização do Lançamento</p>', unsafe_allow_html=True)
        df_mapa = pd.DataFrame({'lat': [-1.4000], 'lon': [-48.3963]}) #
        st.map(df_mapa, zoom=14)

        if st.form_submit_button("✅ TUDO CERTO! ENVIAR AO NOTION"):
            st.success("Dados enviados com sucesso!")
            time.sleep(1)
            st.session_state.tela = 'registro' # Volta ao início após salvar
            st.rerun()

    if st.button("Voltar para Captura"):
        st.session_state.tela = 'registro'
        st.rerun()
