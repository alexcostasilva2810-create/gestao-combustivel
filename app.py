import streamlit as st
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import time

# #-------------------------------------------------------------------------#
#                             CONFIGURAÇÕES VISUAIS
# #-------------------------------------------------------------------------#

st.set_page_config(page_title="ZION - ABASTECIMENTO", layout="centered")

st.markdown("""
    <style>
    /* Fundo: Operação de Mangueiras e Abastecimento Naval */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1544436521-04285e0c0347?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Escurecimento reforçado para não comprometer a leitura */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.82); 
        z-index: -1;
    }

    /* Caixa de preenchimento branca e nítida */
    .box-branco { 
        background-color: rgba(255, 255, 255, 0.98); 
        padding: 30px; 
        border-radius: 12px;
        box-shadow: 0px 8px 24px rgba(0,0,0,0.6);
    }
    
    /* Acessibilidade: Tamanho 14pt (aprox 19px) */
    label, .stSelectbox, .stNumberInput, .stDateInput, p, .stButton { 
        font-size: 19px !important; 
        color: #004a99 !important; 
        font-weight: bold !important;
    }
    
    input { font-size: 19px !important; color: #000 !important; }

    /* Título Verde Centralizado */
    .banner-interno-verde {
        color: #28a745;
        text-align: center;
        font-weight: 900;
        font-size: 26px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }

    .timer-display { 
        font-size: 34px; 
        font-weight: bold; 
        color: #d32f2f; 
        text-align: center; 
        padding: 10px; 
        background: #fdfdfd; 
        border-radius: 8px; 
        border: 2px solid #007bff; 
    }
    </style>
    """, unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#                             TELA DE DADOS
# #-------------------------------------------------------------------------#

if 'passo' not in st.session_state: st.session_state.passo = 'INPUT'

if st.session_state.passo == 'INPUT':
    st.markdown('<h1 style="color:white; text-align:center;">ZION</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="box-branco">', unsafe_allow_html=True)
        
        # Título centralizado sem espaços vazios acima
        st.markdown('<div class="banner-interno-verde">ACOMPANHAMENTO DE ABASTECIMENTO</div>', unsafe_allow_html=True)
        
        navio = st.selectbox("EMPURRADOR", options=["ANGELO", "ANGICO", "AROEIRA", "CANJERANA", "JATOBA"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("DATA", format="DD/MM/YYYY")
            st.number_input("SALDO BB (LTS)", min_value=0)
            st.number_input("SALDO BE (LTS)", min_value=0)
            
        with col2:
            st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0)
            st.markdown("<label>CONTROLE DE TEMPO</label>", unsafe_allow_html=True)
            st.markdown('<div class="timer-display">00:00:00</div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            c1.button("▶️ INICIAR", use_container_width=True)
            c2.button("🛑 PARAR", use_container_width=True)

        st.markdown("---")
        # Assinatura limpa
        st.markdown("<label>ASSINATURA DIGITAL</label>", unsafe_allow_html=True)
        st_canvas(stroke_width=3, stroke_color="#000", background_color="#f8f9fa", height=150, key="canvas_final")

        if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
             st.success("Relatório processado!")
            
        st.markdown('</div>', unsafe_allow_html=True)
