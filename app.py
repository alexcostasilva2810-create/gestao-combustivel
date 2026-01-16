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
        font-size: 16px !important; color: #FFFFFF !important;  
        font-weight: bold !important; text-shadow: 1px 1px 3px #000;
    }
    .banner-interno-verde {
        color: #28a745; text-align: center; font-weight: 900; font-size: 24px;
        margin-bottom: 20px; background: rgba(255, 255, 255, 0.95); padding: 12px; border-radius: 10px;
    }
    .quadro-seguro {
        color: #00FF00 !important; background: rgba(0, 0, 0, 0.8) !important;
        padding: 10px; border-radius: 8px; border: 2px solid #00FF00;
        font-weight: bold; text-align: center; font-size: 16px;
    }
    .alerta-transbordo-flutuante {
        background-color: #FFFF00 !important; color: #FF0000 !important; 
        padding: 15px; border-radius: 10px; border: 4px solid #FF0000;
        font-weight: 900; text-align: center; font-size: 18px;
        margin-bottom: 15px; box-shadow: 0px 10px 30px rgba(255, 0, 0, 0.7);
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
#                             MENU DE NAVEGAÇÃO
# #-------------------------------------------------------------------------#

st.markdown("### 📋 MENU DE NAVEGAÇÃO")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    if st.button("🏠 TELA INICIAL", use_container_width=True): st.session_state.pagina = "inicio"
with col_m2:
    if st.button("📂 MENU PRINCIPAL", use_container_width=True): st.session_state.pagina = "menu"
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

    CAPACIDADES = {
        "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
        "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
        "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
        "TIMBORANA": 19792, "JATOBA": 84000
    }

    navio_selecionado = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys()), key=f"navio_{st.session_state.form_id}")
    st.markdown(f'<div style="color: #FFFF00; font-weight: bold; background: rgba(0,0,0,0.5); padding: 5px; border-radius: 5px; display: inline-block;">Capacidade do Tanque: {CAPACIDADES[navio_selecionado]:,} lts</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        data_abast = st.date_input("DATA", format="DD/MM/YYYY", key=f"dt_{st.session_state.form_id}")
        saldo_bb = st.number_input("SALDO BB (LTS)", min_value=0, key=f"bb_{st.session_state.form_id}")
        saldo_be = st.number_input("SALDO BE (LTS)", min_value=0, key=f"be_{st.session_state.form_id}")
    with col_b:
        qtd_pedida = st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0, key=f"qp_{st.session_state.form_id}")
        remanescente = st.number_input("REMANESCENTE (LTS)", min_value=0, key=f"rm_{st.session_state.form_id}")

    total_geral = saldo_bb + saldo_be + remanescente + qtd_pedida
    limite = CAPACIDADES[navio_selecionado]
    transbordou = total_geral > limite

    if transbordou:
        st.markdown(f'<div style="color:red; background:white; padding:10px; border:2px solid red; font-weight:bold; text-align:center; border-radius:8px;">⚠️ EXCESSO: {total_geral:,} lts / {limite:,} lts</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="quadro-seguro">✅ VOLUME SEGURO: {total_geral:,} lts</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    c_timer, c_fotos = st.columns([1, 2])
    with c_timer:
        st.markdown("<p style='text-align:center;'>CRONÔMETRO</p>", unsafe_allow_html=True)
        if 't_rodando' not in st.session_state: st.session_state.t_rodando = False
        if st.session_state.t_rodando:
            segundos = int(time.time() - st.session_state.t_inicio)
            st.session_state.tempo_final_str = time.strftime('%H:%M:%S', time.gmtime(segundos))
        st.markdown(f'<div style="background:white; color:red; font-size:24px; text-align:center; border-radius:8px; border:2px solid blue; padding:5px;">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        if b1.button("▶️ INICIAR", use_container_width=True):
            st.session_state.t_inicio = time.time(); st.session_state.t_rodando = True
        if b2.button("🛑 PARAR", use_container_width=True):
            st.session_state.t_rodando = False

    with c_fotos:
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            foto_antes = st.camera_input("FOTO ANTES (A)", key=f"fa_{st.session_state.form_id}")
        with f_col2:
            foto_depois = st.camera_input("FOTO DEPOIS (D)", key=f"fd_{st.session_state.form_id}")

    st.markdown("---")
    st.markdown("<p>ASSINATURA DIGITAL</p>", unsafe_allow_html=True)
    canvas_result = st_canvas(stroke_width=3, stroke_color="#000", background_color="#FFFFFF", height=120, key=f"canvas_{st.session_state.form_id}")

    if transbordou:
        st.markdown(f'<div class="alerta-transbordo-flutuante">🚨 BLOQUEIO DE SEGURANÇA: TRANSBORDO! 🚨</div>', unsafe_allow_html=True)
        st.button("GERAR COMUNICADO FINAL (BLOQUEADO)", use_container_width=True, disabled=True)
    else:
        if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(200, 10, "ZION - Comunicado de Abastecimento", ln=True, align="C")
                pdf.ln(10)
                pdf.set_font("Arial", "", 12)
                texto = (f"Empurrador: {navio_selecionado}\n"
                         f"Data: {data_abast.strftime('%d/%m/%Y')}\n"
                         f"Volume Total: {total_geral:,} lts\n"
                         f"Tempo de Operação: {st.session_state.tempo_final_str}")
                pdf.multi_cell(0, 10, texto)
                
                # Inserção das fotos no PDF
                if foto_antes and foto_depois:
                    img_a = Image.open(foto_antes)
                    img_d = Image.open(foto_depois)
                    pdf.image(img_a, x=10, y=70, w=90)
                    pdf.image(img_d, x=110, y=70, w=90)
                
                # Assinatura
                if canvas_result.image_data is not None:
                    img_sig = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                    sig_buffer = io.BytesIO()
                    img_sig.save(sig_buffer, format="PNG")
                    pdf.image(sig_buffer, x=70, y=160, w=60)
                
                st.session_state.pdf_output = pdf.output(dest='S')
                st.success("Documento preparado com sucesso!")
                st.download_button("📥 BAIXAR COMUNICADO FINAL", data=bytes(st.session_state.pdf_output), file_name=f"Zion_{navio_selecionado}.pdf", use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")

# ... (outras telas ignoradas para brevidade)
