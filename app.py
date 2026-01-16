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

st.set_page_config(page_title="ZION - ABASTECIMENTO NAVAL", layout="centered")

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
        font-size: 19px !important; color: #FFFFFF !important;  
        font-weight: bold !important; text-shadow: 1px 1px 3px #000;
    }
    .stSelectbox div, .stNumberInput input, .stDateInput input, .stFileUploader section {
        background-color: white !important; color: black !important;
        font-size: 19px !important; border-radius: 8px !important;
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
    .alerta-sucesso-custom {
        background-color: rgba(0, 128, 0, 0.8); color: white; padding: 15px; 
        border-radius: 5px; font-size: 14px; font-weight: bold;
        text-align: center; margin-top: 10px;
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

col1, col2 = st.columns(2)

with col1:
    data_abast = st.date_input("DATA", format="DD/MM/YYYY")
    saldo_bb = st.number_input("SALDO BB (LTS)", min_value=0)
    saldo_be = st.number_input("SALDO BE (LTS)", min_value=0)
    remanescente = st.number_input("REMANESCENTE (LTS)", min_value=0)
    foto_antes = st.file_uploader("📷 FOTO ANTES (A)", type=['jpg', 'png', 'jpeg'])

with col2:
    qtd_pedida = st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0)
    st.markdown("<p style='margin-bottom: 0px;'>CONTROLE DE TEMPO</p>", unsafe_allow_html=True)
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
        time.sleep(1); st.rerun()
    else:
        placeholder_tempo.markdown(f'<div class="timer-display">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)
    
    foto_depois = st.file_uploader("📷 FOTO DEPOIS (D)", type=['jpg', 'png', 'jpeg'])

st.markdown("---")
st.markdown("<p>ASSINATURA DIGITAL</p>", unsafe_allow_html=True)
canvas_result = st_canvas(stroke_width=3, stroke_color="#000", background_color="#FFFFFF", height=150, key="canvas_final_v4")

# #-------------------------------------------------------------------------#
#                     GERAÇÃO DO PDF (LAYOUT TRAVADO)
# #-------------------------------------------------------------------------#

if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Cabeçalho
        pdf.set_font("Arial", "B", 20)
        pdf.set_text_color(0, 102, 255)
        pdf.cell(200, 10, "ZION", ln=True, align="C")
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, "Comunicado de Abastecimento", ln=True, align="C")
        pdf.ln(10)
        
        # Texto Profissional
        pdf.set_font("Arial", "", 12)
        total_pos = saldo_bb + saldo_be + remanescente + qtd_pedida
        texto_corpo = (
            f"Comunico que o empurrador {navio_selecionado} está apto a receber o consumo de {qtd_pedida:,} lts, "
            f"visto que possui um saldo de {saldo_bb:,} lts (BB) e {saldo_be:,} lts (BE), somados ao saldo remanescente de {remanescente:,} lts.\n\n"
            f"Portanto, o saldo total após o abastecimento será de {total_pos:,} lts.\n"
            f"Ressaltamos que a capacidade total do empurrador é de {CAPACIDADES[navio_selecionado]:,} lts.\n\n"
            f"Informo que o empurrador levou {st.session_state.tempo_final_str} para abastecer.\n\n"
            f"Segue abaixo as fotos do antes e depois do abastecimento:"
        )
        pdf.multi_cell(0, 8, texto_corpo)
        
        # POSICIONAMENTO FIXO DAS FOTOS (Lado a lado, menores)
        y_fotos = pdf.get_y() + 5
        largura_foto = 45 # Tamanho reduzido para apresentação limpa
        
        if foto_antes:
            pdf.image(Image.open(foto_antes), x=40, y=y_fotos, w=largura_foto) # Posição A
        if foto_depois:
            pdf.image(Image.open(foto_depois), x=115, y=y_fotos, w=largura_foto) # Posição D
        
        # ÁREA DE ASSINATURA (Sempre abaixo das fotos)
        pdf.set_y(y_fotos + 55) 
        if canvas_result.image_data is not None:
            sig_img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
            sig_buf = io.BytesIO()
            sig_img.save(sig_buf, format='PNG')
            pdf.image(sig_buf, x=80, y=pdf.get_y(), w=40)

        # Linha Curta e Centralizada
        pdf.ln(12)
        pdf.line(70, pdf.get_y(), 140, pdf.get_y()) 
        pdf.set_font("Arial", "I", 8)
        data_hora = datetime.now().strftime('%d/%m/%Y às %H:%M:%S')
        pdf.cell(0, 8, f"Assinado digitalmente em: {data_hora}", ln=True, align="C")
        
        pdf_bytes = pdf.output(dest='S')
        st.download_button(
            label="📥 BAIXAR COMUNICADO FINAL",
            data=bytes(pdf_bytes),
            file_name=f"Comunicado_{navio_selecionado}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown('<div class="alerta-sucesso-custom">SEU PDF ESTA PRONTO PEGUE-O E ENVIE PARA O CIOP.</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erro ao gerar: {e}")
