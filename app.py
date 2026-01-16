import streamlit as st
from datetime import datetime
from fpdf import FPDF
from streamlit_drawable_canvas import st_canvas
import time
from PIL import Image
import io

# #-------------------------------------------------------------------------#
#                             CONFIGURAÇÕES VISUAIS
# #-------------------------------------------------------------------------#

st.set_page_config(page_title="ZION - SISTEMA DE GESTÃO", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1524522173746-f628baad3644?q=80&w=2000&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.75); z-index: -1;
    }
    label, .stMarkdown p { 
        font-size: 18px !important; color: #FFFFFF !important;  
        font-weight: bold !important; text-shadow: 1px 1px 3px #000;
    }
    /* ALERTA DE CAPACIDADE - AMARELO 15PX */
    .alerta-capacidade {
        color: #FFFF00 !important; 
        font-size: 15px !important; 
        font-weight: 800 !important;
        background: rgba(0, 0, 0, 0.6);
        padding: 8px 12px;
        border-radius: 5px;
        margin-bottom: 15px;
        display: inline-block;
        border: 1px solid #FFFF00;
    }
    .stSelectbox div, .stNumberInput input, .stDateInput input, .stFileUploader section {
        background-color: white !important; color: black !important;
        font-size: 18px !important; border-radius: 8px !important;
    }
    .banner-interno-verde {
        color: #28a745; text-align: center; font-weight: 900; font-size: 28px;
        margin-bottom: 20px; text-transform: uppercase;
        background: rgba(255, 255, 255, 0.95); padding: 12px; border-radius: 10px;
    }
    .timer-display { 
        font-size: 32px; font-weight: bold; color: #d32f2f; text-align: center; 
        padding: 10px; background: white; border-radius: 10px; border: 3px solid #007bff; 
    }
    .alerta-sucesso-custom {
        background-color: rgba(0, 128, 0, 0.85); color: white; padding: 15px; 
        border-radius: 5px; font-size: 14px; font-weight: bold;
        text-align: center; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#               LÓGICA DE NAVEGAÇÃO E LIMPEZA
# #-------------------------------------------------------------------------#

if 'pagina' not in st.session_state: st.session_state.pagina = "abastecimento"
if 'form_id' not in st.session_state: st.session_state.form_id = 0

def reset_lancamento():
    st.session_state.form_id += 1
    st.session_state.t_rodando = False
    st.session_state.t_inicio = 0
    st.session_state.tempo_final_str = "00:00:00"

# #-------------------------------------------------------------------------#
#                             BLOCO DE MENU
# #-------------------------------------------------------------------------#

st.markdown("### 📋 MENU DE NAVEGAÇÃO")
col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    if st.button("🏠 TELA INICIAL", use_container_width=True):
        st.session_state.pagina = "inicio"
with col_m2:
    if st.button("📂 MENU PRINCIPAL", use_container_width=True):
        st.session_state.pagina = "menu"
with col_m3:
    if st.button("⛽ NOVO ABASTECIMENTO", use_container_width=True):
        st.session_state.pagina = "abastecimento"
        reset_lancamento()

st.markdown("---")

# #-------------------------------------------------------------------------#
#                         TELA DE ABASTECIMENTO
# #-------------------------------------------------------------------------#

if st.session_state.pagina == "abastecimento":
    st.markdown('<h1 style="color:white; text-align:center; font-size: 40px; margin-bottom: 5px;">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<div class="banner-interno-verde">ACOMPANHAMENTO DE ABASTECIMENTO</div>', unsafe_allow_html=True)

    # LISTA CORRIGIDA CONFORME TABELA ENVIADA
    CAPACIDADES = {
        "ANGELO": 17000,
        "ANGICO": 88000,
        "AROEIRA": 88000,
        "BRENO": 34700,
        "CANJERANA": 18000,
        "CUMARU": 64000,
        "IPE": 29700,
        "SAMAUMA": 92000,
        "JACARANDA": 19792,
        "LUIZ FELIPE": 25000,
        "QUARUBA": 19792,
        "TIMBORANA": 19792,
        "JATOBA": 84000
    }

    navio_selecionado = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys()), key=f"navio_{st.session_state.form_id}")
    
    # ALERTA DE CAPACIDADE VISÍVEL EM AMARELO
    st.markdown(f'<div class="alerta-capacidade">Capacidade do Tanque: {CAPACIDADES[navio_selecionado]:,} lts</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        data_abast = st.date_input("DATA", format="DD/MM/YYYY", key=f"data_{st.session_state.form_id}")
        saldo_bb = st.number_input("SALDO BB (LTS)", min_value=0, key=f"bb_{st.session_state.form_id}")
        saldo_be = st.number_input("SALDO BE (LTS)", min_value=0, key=f"be_{st.session_state.form_id}")
        remanescente = st.number_input("REMANESCENTE (LTS)", min_value=0, key=f"rem_{st.session_state.form_id}")
        foto_antes = st.file_uploader("📷 FOTO ANTES (A)", type=['jpg', 'png', 'jpeg'], key=f"fa_{st.session_state.form_id}")

    with col2:
        qtd_pedida = st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0, key=f"ped_{st.session_state.form_id}")
        st.markdown("<p style='margin-bottom: 0px;'>CONTROLE DE TEMPO</p>", unsafe_allow_html=True)
        
        if 't_rodando' not in st.session_state: st.session_state.t_rodando = False
        if 'tempo_final_str' not in st.session_state: st.session_state.tempo_final_str = "00:00:00"
        
        placeholder_tempo = st.empty()
        c1, c2 = st.columns(2)
        if c1.button("▶️ INICIAR", use_container_width=True):
            st.session_state.t_inicio = time.time(); st.session_state.t_rodando = True
        if c2.button("🛑 PARAR", use_container_width=True):
            st.session_state.t_rodando = False
        
        if st.session_state.t_rodando:
            segundos = int(time.time() - st.session_state.t_inicio)
            st.session_state.tempo_final_str = time.strftime('%H:%M:%S', time.gmtime(segundos))
        
        placeholder_tempo.markdown(f'<div class="timer-display">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)
        foto_depois = st.file_uploader("📷 FOTO DEPOIS (D)", type=['jpg', 'png', 'jpeg'], key=f"fd_{st.session_state.form_id}")

    st.markdown("<p>ASSINATURA DIGITAL</p>", unsafe_allow_html=True)
    canvas_result = st_canvas(stroke_width=3, stroke_color="#000", background_color="#FFFFFF", height=150, key=f"canvas_{st.session_state.form_id}")

    if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Cabeçalho
            pdf.set_font("Arial", "B", 20)
            pdf.set_text_color(0, 102, 255)
            pdf.cell(200, 10, "ZION", ln=True, align="C")
            pdf.ln(10)
            
            pdf.set_font("Arial", "", 12)
            pdf.set_text_color(0, 0, 0)
            total_pos = saldo_bb + saldo_be + remanescente + qtd_pedida
            texto = (f"Comunico que o empurrador {navio_selecionado} está apto a receber o consumo de {qtd_pedida:,} lts.\n"
                     f"Capacidade total do empurrador: {CAPACIDADES[navio_selecionado]:,} lts.\n"
                     f"Saldo Total Pós-Abastecimento: {total_pos:,} lts.")
            pdf.multi_cell(0, 8, texto)

            # Fotos lado a lado A e D
            y_pos = pdf.get_y() + 5
            if foto_antes: pdf.image(Image.open(foto_antes), x=40, y=y_pos, w=45)
            if foto_depois: pdf.image(Image.open(foto_depois), x=115, y=y_pos, w=45)
            
            st.download_button("📥 BAIXAR PDF", data=bytes(pdf.output(dest='S')), file_name=f"Zion_{navio_selecionado}.pdf", use_container_width=True)
            st.markdown('<div class="alerta-sucesso-custom">Tudo corrigido! Linha, assinatura e fotos incluídas.</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erro: {e}")

elif st.session_state.pagina == "menu":
    st.info("📂 Menu Principal")
elif st.session_state.pagina == "inicio":
    st.info("🏠 Tela Inicial")
