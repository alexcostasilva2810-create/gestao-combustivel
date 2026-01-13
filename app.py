import streamlit as st
from datetime import date
import time

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="ZION - Gestão", layout="centered")

st.markdown("""
    <style>
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; }
    .texto-verde { color: #00FF00 !important; font-size: 20px !important; font-weight: bold; }
    .stButton>button { width: 100%; background-color: #007bff; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DADOS E ESTADO ---
EMPURRADORES = ["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"]

if 'dados_temp' not in st.session_state:
    st.session_state.dados_temp = None

# --- 3. TELA 1: FORMULÁRIO DE CAPTURA ---
st.markdown('<h2 style="text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        empurrador = st.selectbox("EMPURRADOR", options=EMPURRADORES)
        pedido = st.text_input("Nº PEDIDO")
        nf_num = st.number_input("Nº NF", step=1, format="%d")
    with col2:
        qtd = st.number_input("QUANTIDADE (LTS)", step=1, format="%d")
        data_sel = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY")
        fornecedor = st.text_input("FORNECEDOR")

    st.write("---")
    st.write("📸 **Captura da Chave da Nota**")
    foto = st.camera_input("Escanear Código de Barras")
    chave_manual = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)

    # BOTÃO PARA EDITAR/CONFERIR
    if st.button("PROSSEGUIR PARA CONFERÊNCIA"):
        # Aqui simulamos a extração automática da chave para edição
        st.session_state.dados_temp = {
            "empurrador": empurrador,
            "nf": nf_num,
            "chave": chave_manual if chave_manual else "CHAVE_EXTRAIDA_PELA_FOTO",
            "qtd": qtd,
            "fornecedor": fornecedor,
            "data": data_sel
        }

# --- 4. TELA 2: BLOCO DE EDIÇÃO E VALIDAÇÃO (A "Outra Tela") ---
if st.session_state.dados_temp:
    st.write("---")
    st.markdown('<p class="texto-verde">🔍 CONFERIR E EDITAR DADOS DA NOTA</p>', unsafe_allow_html=True)
    
    with st.expander("Clique para Editar Dados Extraídos da Chave", expanded=True):
        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            # Campos preenchidos automaticamente, mas que permitem edição
            nova_nf = st.text_input("Confirmar Nº NF", value=str(st.session_state.dados_temp['nf']))
            nova_chave = st.text_input("Confirmar Chave", value=st.session_state.dados_temp['chave'])
        with col_ed2:
            novo_fornecedor = st.text_input("Confirmar Fornecedor", value=st.session_state.dados_temp['fornecedor'])
            nova_qtd = st.text_input("Confirmar Quantidade", value=str(st.session_state.dados_temp['qtd']))

    # BLOCO DE TANQUES (Sempre visível antes do envio final)
    st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
    c_a, c_b = st.columns(2)
    t_bb = c_a.number_input("TANQUE BB (m³)", step=0.01)
    t_be = c_b.number_input("TANQUE BE (m³)", step=0.01)

    # BOTÃO FINAL DE SALVAMENTO NO NOTION
    if st.button("✅ TUDO CERTO! SALVAR NO NOTION"):
        with st.spinner("Enviando dados..."):
            time.sleep(1) # Simulação de envio
            st.success("Registro concluído com sucesso!")
            st.session_state.dados_temp = None # Limpa para o próximo registro
            time.sleep(1)
            st.rerun()
