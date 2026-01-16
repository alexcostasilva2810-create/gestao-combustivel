import streamlit as st
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
import time

# #-------------------------------------------------------------------------#
#                             CONFIGURAÇÕES VISUAIS
# #-------------------------------------------------------------------------#

st.set_page_config(page_title="ZION - ABASTECIMENTO NAVAL", layout="centered")

st.markdown("""
    <style>
    /* Fundo Naval que você aprovou */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1524522173746-f628baad3644?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Overlay escuro para dar contraste */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.75); 
        z-index: -1;
    }

    /* Estilo das letras em cima dos blocos (Rótulos) - Agora em Branco */
    label, .stMarkdown p { 
        font-size: 19px !important; /* Tamanho 14pt solicitado */
        color: #FFFFFF !important;  /* Mudança para Branco conforme pedido */
        font-weight: bold !important;
        text-shadow: 1px 1px 2px #000; /* Sombra para garantir leitura */
    }

    /* Caixa onde os dados são digitados (Branca para destacar o texto interno) */
    .stSelectbox div, .stNumberInput input, .stDateInput input {
        background-color: white !important;
        color: black !important;
        font-size: 19px !important;
        border-radius: 8px !important;
    }

    .banner-interno-verde {
        color: #28a745;
        text-align: center;
        font-weight: 900;
        font-size: 28px;
        margin-bottom: 25px;
        text-transform: uppercase;
        background: rgba(255, 255, 255, 0.9);
        padding: 10px;
        border-radius: 10px;
    }

    .timer-display { 
        font-size: 36px; 
        font-weight: bold; 
        color: #d32f2f; 
        text-align: center; 
        padding: 10px; 
        background: white; 
        border-radius: 10px; 
        border: 3px solid #007bff; 
    }
    </style>
    """, unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#                             TELA DE ENTRADA
# #-------------------------------------------------------------------------#

if 'passo' not in st.session_state: st.session_state.passo = 'INPUT'

if st.session_state.passo == 'INPUT':
    st.markdown('<h1 style="color:white; text-align:center; font-size: 45px;">ZION</h1>', unsafe_allow_html=True)
    
    # Título verde centralizado sem campo vazio no topo
    st.markdown('<div class="banner-interno-verde">ACOMPANHAMENTO DE ABASTECIMENTO</div>', unsafe_allow_html=True)
    
    # Campo Empurrador
    empurrador = st.selectbox("EMPURRADOR", options=["ANGELO", "ANGICO", "AROEIRA", "CANJERANA", "JATOBA"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("DATA", format="DD/MM/YYYY")
        st.number_input("SALDO BB (LTS)", min_value=0)
        st.number_input("SALDO BE (LTS)", min_value=0)
        st.number_input("REMANESCENTE (LTS)", min_value=0)
        # Campo de foto ANTES
        st.file_uploader("📷 FOTO ANTES DO ABASTECIMENTO", type=['jpg', 'png', 'jpeg'])
        
    with col2:
        st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0)
        st.markdown("<p style='margin-bottom: 0px;'>CONTROLE DE TEMPO</p>", unsafe_allow_html=True)
        st.markdown('<div class="timer-display">00:00:00</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        c1.button("▶️ INICIAR", use_container_width=True)
        c2.button("🛑 PARAR", use_container_width=True)
        
        # Campo de foto DEPOIS
        st.file_uploader("📷 FOTO DEPOIS DO ABASTECIMENTO", type=['jpg', 'png', 'jpeg'])

    st.markdown("---")
    st.markdown("<p>ASSINATURA DIGITAL</p>", unsafe_allow_html=True)
    st_canvas(stroke_width=3, stroke_color="#000", background_color="#FFFFFF", height=150, key="canvas_zion_final")

    if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
         st.success("Relatório gerado!")
