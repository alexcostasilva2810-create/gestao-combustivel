import streamlit as st
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import time

# #-------------------------------------------------------------------------#
#                             CONFIGURAÇÕES VISUAIS
# #-------------------------------------------------------------------------#

st.set_page_config(page_title="ZION - ABASTECIMENTO NAVAL", layout="centered")

st.markdown("""
    <style>
    /* Fundo: Pier Naval Escurecido para não atrapalhar a visão */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1524522173746-f628baad3644?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Overlay escuro para tirar a claridade excessiva */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.82); 
        z-index: -1;
    }

    /* Caixa de preenchimento nítida */
    .box-branco { 
        background-color: rgba(255, 255, 255, 0.98); 
        padding: 30px; 
        border-radius: 15px;
        border: 2px solid #007bff;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Acessibilidade: Tamanho 14pt (aprox 19px) conforme solicitado */
    label, .stSelectbox, .stNumberInput, .stDateInput, p, .stButton { 
        font-size: 19px !important; 
        color: #004a99 !important; 
        font-weight: bold !important;
    }
    
    input { font-size: 19px !important; color: black !important; }

    .banner-interno-verde {
        color: #28a745;
        text-align: center;
        font-weight: 900;
        font-size: 28px;
        margin-bottom: 25px;
        text-transform: uppercase;
    }

    .timer-display { 
        font-size: 34px; 
        font-weight: bold; 
        color: #d32f2f; 
        text-align: center; 
        padding: 10px; 
        background: #fdfdfd; 
        border-radius: 10px; 
        border: 2px solid #007bff; 
    }
    </style>
    """, unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#                             TELA DE ENTRADA
# #-------------------------------------------------------------------------#

if 'passo' not in st.session_state: st.session_state.passo = 'INPUT'

if st.session_state.passo == 'INPUT':
    st.markdown('<h1 style="color:white; text-align:center;">ZION</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="box-branco">', unsafe_allow_html=True)
        
        # Cabeçalho verde centralizado
        st.markdown('<div class="banner-interno-verde">ACOMPANHAMENTO DE ABASTECIMENTO</div>', unsafe_allow_html=True)
        
        empurrador = st.selectbox("EMPURRADOR", options=["ANGELO", "ANGICO", "AROEIRA", "CANJERANA", "JATOBA"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("DATA", format="DD/MM/YYYY")
            st.number_input("SALDO BB (LTS)", min_value=0)
            st.number_input("SALDO BE (LTS)", min_value=0)
            st.number_input("REMANESCENTE (LTS)", min_value=0)
            # Reintegração do campo de foto ANTES
            st.file_uploader("📷 FOTO ANTES DO ABASTECIMENTO", type=['jpg', 'png', 'jpeg'])
            
        with col2:
            st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0)
            st.markdown("<label>CONTROLE DE TEMPO</label>", unsafe_allow_html=True)
            st.markdown('<div class="timer-display">00:00:00</div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            c1.button("▶️ INICIAR", use_container_width=True)
            c2.button("🛑 PARAR", use_container_width=True)
            
            # Reintegração do campo de foto DEPOIS
            st.file_uploader("📷 FOTO DEPOIS DO ABASTECIMENTO", type=['jpg', 'png', 'jpeg'])

        st.markdown("---")
        st.markdown("<label>ASSINATURA DIGITAL</label>", unsafe_allow_html=True)
        st_canvas(stroke_width=3, stroke_color="#000", background_color="#f8f9fa", height=150, key="canvas_final_ajustado")

        if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
             st.success("Tudo pronto!")
            
        st.markdown('</div>', unsafe_allow_html=True)
