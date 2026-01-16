import streamlit as st
from datetime import datetime
from fpdf import FPDF
from streamlit_drawable_canvas import st_canvas
import time

# #-------------------------------------------------------------------------#
#                             CONFIGURAÇÕES VISUAIS
# #-------------------------------------------------------------------------#

st.set_page_config(page_title="ZION - ABASTECIMENTO NAVAL", layout="centered")

st.markdown("""
    <style>
    /* Plano de fundo aprovado: Navio Cargueiro e Mar */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1524522173746-f628baad3644?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp::before {
        content: "";
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.75); z-index: -1;
    }
    /* Letras brancas para contraste conforme solicitado */
    label, .stMarkdown p { 
        font-size: 19px !important; 
        color: #FFFFFF !important;  
        font-weight: bold !important;
        text-shadow: 1px 1px 3px #000;
    }
    .stSelectbox div, .stNumberInput input, .stDateInput input, .stFileUploader section {
        background-color: white !important;
        color: black !important;
        font-size: 19px !important;
        border-radius: 8px !important;
    }
    .banner-interno-verde {
        color: #28a745; text-align: center; font-weight: 900; font-size: 28px;
        margin-bottom: 20px; text-transform: uppercase;
        background: rgba(255, 255, 255, 0.95); padding: 12px; border-radius: 10px;
    }
    .timer-display { 
        font-size: 36px; font-weight: bold; color: #d32f2f; text-align: center; 
        padding: 10px; background: white; border-radius: 10px; border: 3px solid #007bff; 
    }
    </style>
    """, unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#                             LÓGICA E ESTADO
# #-------------------------------------------------------------------------#

CAPACIDADES = {"ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "CANJERANA": 18000, "JATOBA": 84000}

if 't_rodando' not in st.session_state: st.session_state.t_rodando = False
if 't_inicio' not in st.session_state: st.session_state.t_inicio = 0
if 'tempo_final_str' not in st.session_state: st.session_state.tempo_final_str = "00:00:00"

# #-------------------------------------------------------------------------#
#                             TELA DE ENTRADA
# #-------------------------------------------------------------------------#

st.markdown('<h1 style="color:white; text-align:center; font-size: 45px; margin-bottom: 5px;">ZION</h1>', unsafe_allow_html=True)
st.markdown('<div class="banner-interno-verde">ACOMPANHAMENTO DE ABASTECIMENTO</div>', unsafe_allow_html=True)

navio_selecionado = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys()))
# Alerta de capacidade restituído
st.info(f"Capacidade do Tanque: {CAPACIDADES[navio_selecionado]:,} lts")

col1, col2 = st.columns(2)

with col1:
    data_abast = st.date_input("DATA", format="DD/MM/YYYY")
    saldo_bb = st.number_input("SALDO BB (LTS)", min_value=0)
    saldo_be = st.number_input("SALDO BE (LTS)", min_value=0)
    remanescente = st.number_input("REMANESCENTE (LTS)", min_value=0)
    foto_antes = st.file_uploader("📷 FOTO ANTES DO ABASTECIMENTO", type=['jpg', 'png', 'jpeg'])

with col2:
    qtd_pedida = st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0)
    st.markdown("<p style='margin-bottom: 0px;'>CONTROLE DE TEMPO</p>", unsafe_allow_html=True)
    placeholder_tempo = st.empty()
    
    c1, c2 = st.columns(2)
    if c1.button("▶️ INICIAR", use_container_width=True):
        st.session_state.t_inicio = time.time()
        st.session_state.t_rodando = True
    
    if c2.button("🛑 PARAR", use_container_width=True):
        st.session_state.t_rodando = False
    
    # Cronômetro funcionando segundo a segundo
    if st.session_state.t_rodando:
        segundos = int(time.time() - st.session_state.t_inicio)
        st.session_state.tempo_final_str = time.strftime('%H:%M:%S', time.gmtime(segundos))
        placeholder_tempo.markdown(f'<div class="timer-display">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)
        time.sleep(1)
        st.rerun()
    else:
        placeholder_tempo.markdown(f'<div class="timer-display">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)
    
    foto_depois = st.file_uploader("📷 FOTO DEPOIS DO ABASTECIMENTO", type=['jpg', 'png', 'jpeg'])

st.markdown("---")
st.markdown("<p>ASSINATURA DIGITAL</p>", unsafe_allow_html=True)
canvas_result = st_canvas(stroke_width=3, stroke_color="#000", background_color="#FFFFFF", height=150, key="canvas_final_ok")

# #-------------------------------------------------------------------------#
#                     GERAÇÃO DO PDF (LÓGICA BLINDADA)
# #-------------------------------------------------------------------------#

if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "ZION - COMUNICADO DE ABASTECIMENTO", ln=True, align="C")
        
        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        pdf.cell(200, 10, f"Empurrador: {navio_selecionado}", ln=True)
        pdf.cell(200, 10, f"Data: {data_abast.strftime('%d/%m/%Y')}", ln=True)
        pdf.cell(200, 10, f"Tempo Total: {st.session_state.tempo_final_str}", ln=True)
        pdf.cell(200, 10, f"Quantidade Pedida: {qtd_pedida} LTS", ln=True)
        
        # Correção para evitar erro de 'bytearray'
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        st.download_button(
            label="📥 BAIXAR RELATÓRIO PDF",
            data=pdf_bytes,
            file_name=f"Relatorio_{navio_selecionado}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.success("PDF gerado com sucesso! Clique acima para baixar.")
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")
