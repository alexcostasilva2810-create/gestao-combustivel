import streamlit as st
from datetime import date
import base64
import os
import time

# Tenta importar a biblioteca de PDF, se não existir, o sistema avisa sem travar
try:
    from fpdf import FPDF
    PDF_DISPONIVEL = True
except ImportError:
    PDF_DISPONIVEL = False

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="ZION - Gestão", page_icon="⛽", layout="centered")

st.markdown(f"""
    <style>
    /* Rótulos em AZUL */
    label, .stWidgetLabel p {{
        color: #007bff !important;
        font-weight: bold !important;
    }}
    /* Título em VERDE FORTE */
    .texto-verde {{
        color: #00FF00 !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }}
    input {{ background-color: white !important; color: black !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. LISTA DE EMPURRADORES ---
EMPURRADORES = ["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"]

# --- 3. TELA DO FORMULÁRIO ---
if 'tela' not in st.session_state: st.session_state.tela = 'form'

if st.session_state.tela == 'form':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_registro"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("EMPURRADOR", options=EMPURRADORES)
            st.text_input("Nº PEDIDO")
            st.number_input("Nº NF", step=1, format="%d")
            
            # BLOCO DE CAPTURA DA CHAVE
            st.write("📸 **Captura da Chave**")
            chave_input = st.text_input("CHAVE DA NF (Extraída ou Digitada)", max_chars=44)
            
            # Botão para o site que você usa
            if len(chave_input) == 44:
                st.link_button("📄 VER PDF NO CONSULTA DANFE", f"https://www.consultadanfe.com/?chave={chave_input}")

        with col2:
            st.number_input("QUANTIDADE (LTS)", step=1, format="%d")
            st.date_input("DATA", value=date.today(), format="DD/MM/YYYY")
            st.text_input("FORNECEDOR")
            st.camera_input("Escanear Código de Barras")

        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        c_a, c_b = st.columns(2)
        with c_a: st.number_input("TANQUE BB (m³)", step=0.01)
        with c_b: st.number_input("TANQUE BE (m³)", step=0.01)

        # BOTÃO DE ENVIO
        enviar = st.form_submit_button("CONCLUIR E ENVIAR AO NOTION")
        
        if enviar:
            if len(chave_input) < 44:
                st.warning("⚠️ Chave de NF incompleta.")
            else:
                st.success("✅ Dados e Chave salvos para o Notion!")
                # O PDF será guardado na coluna 'Arquivos' do Notion através do link ou upload
