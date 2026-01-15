import streamlit as st
from datetime import date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ZION - ABASTECIMENTO ODM", layout="centered")

# --- ESTILO VISUAL (UI/UX) ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("app/static/plataforma.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 8, 20, 0.85); z-index: -1;
    }
    .main-container { background-color: white; padding: 25px; border-radius: 15px; }
    .alerta-erro { background-color: #ff4b4b; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; margin-bottom: 15px; }
    .alerta-sucesso { background-color: #28a745; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; }
    label { color: #007bff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Capacidades conforme a tabela
CAPACIDADES = {
    "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
    "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
    "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
    "TIMBORANA": 19792, "JATOBA": 84000
}

if 'tela' not in st.session_state: st.session_state.tela = 'input'
