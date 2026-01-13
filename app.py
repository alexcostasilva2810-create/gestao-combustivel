import streamlit as st
import requests
from datetime import date

# Configuração da Página para ícone no celular
st.set_page_config(page_title="Zion Combustível", page_icon="⛽", layout="centered")

# Função para aplicar o fundo de plataforma e estilo visual
def aplicar_estilo_zion():
    # Links das imagens hospedadas no seu repositório GitHub
    img_fundo = "https://raw.githubusercontent.com/alexcostasilva2810-create/gestao-combustivel/main/plataforma.jpg"
    
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("{img_fundo}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stButton>button {{
            width: 100%;
            height: 3.5em;
            background-color: #007bff;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            border: none;
        }}
        h1, h2, h3, p {{
            color: white !important;
            text-shadow: 2px 2px 8px #000000;
            text-align: center;
        }}
        /* Estilo para os campos de entrada ficarem visíveis sobre o fundo */
        .stTextInput>div>div>input, .stNumberInput>div>div>input {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 8px;
        }}
        </style>
        """, unsafe_allow_html=True)

aplicar_estilo_zion()
