import streamlit as st
from datetime import datetime
from fpdf import FPDF
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import time

# #-------------------------------------------------------------------------#
#                             BLOCO 1: CONFIGURAÇÕES
# #-------------------------------------------------------------------------#

st.set_page_config(page_title="ZION TECNOLOGIA", layout="centered")

# CSS focado em acessibilidade (Fontes tamanho 14)
st.markdown("""
    <style>
    /* Fundo sólido e limpo */
    .stApp { background-color: #f4f7f6; }
    
    .box-branco { background-color: white; padding: 25px; border-radius: 15px; border: 1px solid #ddd; }
    
    /* Aumento de fonte para labels e campos (Tamanho 14) */
    label, .stSelectbox, .stNumberInput, .stDateInput, p { 
        font-size: 16px !important; /* Ajustado para legibilidade ideal em 14pt/16px */
        color: #007bff !important; 
        font-weight: bold !important;
    }
    
    input { font-size: 16px !important; }

    .banner-interno-verde {
        color: #28a745;
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        padding: 15px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }
    
    .timer-display { font-size: 32px; font-weight: bold; color: #d32f2f; text-align: center; padding: 10px; background: #f0f0f0; border-radius: 10px; border: 2px solid #007bff; }
    </style>
    """, unsafe_allow_html=True)

CAPACIDADES = {
    "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
    "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
    "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
    "TIMBORANA": 19792, "JATOBA": 84000
}

if 'passo' not in st.session_state: st.session_state.passo = 'INICIAL'
if 't_rodando' not in st.session_state: st.session_state.t_rodando = False
if 't_inicio' not in st.session_state: st.session_state.t_inicio = 0
if 'tempo_final_str' not in st.session_state: st.session_state.tempo_final_str = "00:00:00"

# #-------------------------------------------------------------------------#
#                             BLOCO 2: TELA INICIAL
# #-------------------------------------------------------------------------#

if st.session_state.passo == 'INICIAL':
    st.markdown('<h1 style="color:#007bff; text-align:center;">ZION TECNOLOGIA</h1>', unsafe_allow_html=True)
    if st.button("INICIAR NOVO REGISTRO", use_container_width=True, type="primary"):
        st.session_state.passo = 'INPUT'
        st.rerun()

# #-------------------------------------------------------------------------#
#                             BLOCO 3: INPUT E CRONÔMETRO
# #-------------------------------------------------------------------------#

elif st.session_state.passo == 'INPUT':
    st.markdown('<h1 style="color:#007bff; text-align:center; margin-bottom:10px;">ZION</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="box-branco">', unsafe_allow_html=True)
        
        # Banner verde limpo
        st.markdown('<div class="banner-interno-verde">ACOMPANHAMENTO DE ABASTECIMENTO</div>', unsafe_allow_html=True)
        
        navio = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys()))
        limite = CAPACIDADES[navio]
        st.info(f"Capacidade do Tanque: {limite:,} lts")
        
        col1, col2 = st.columns(2)
        with col1:
            dt_input = st.date_input("DATA", format="DD/MM/YYYY")
            s_bb = st.number_input("SALDO BB (LTS)", min_value=0)
            s_be = st.number_input("SALDO BE (LTS)", min_value=0)
            s_rem = st.number_input("REMANESCENTE (LTS)", min_value=0)
            foto_antes = st.file_uploader("📷 Foto ANTES", type=['jpg', 'png', 'jpeg'])
            
        with col2:
            pedido = st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0)
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("<label>CONTROLE DE TEMPO</label>", unsafe_allow_html=True)
            placeholder_tempo = st.empty()
            
            c_t1, c_t2 = st.columns(2)
            if c_t1.button("▶️ INICIAR", use_container_width=True):
                st.session_state.t_inicio = time.time()
                st.session_state.t_rodando = True
            
            if c_t2.button("🛑 PARAR", use_container_width=True):
                st.session_state.t_rodando = False
            
            if st.session_state.t_rodando:
                segundos = int(time.time() - st.session_state.t_inicio)
                st.session_state.tempo_final_str = time.strftime('%H:%M:%S', time.gmtime(segundos))
                placeholder_tempo.markdown(f'<div class="timer-display">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)
                time.sleep(0.1)
                st.rerun()
            else:
                placeholder_tempo.markdown(f'<div class="timer-display">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)

            foto_depois = st.file_uploader("📷 Foto DEPOIS", type=['jpg', 'png', 'jpeg'])

        st.markdown("---")
        # Texto "(TELA TOUCH)" removido
        st.markdown("<label>ASSINATURA DIGITAL</label>", unsafe_allow_html=True)
        canvas_result = st_canvas(stroke_width=3, stroke_color="#000", background_color="#f8f9fa", height=150, key="canvas_v_final")

        if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
            if canvas_result.image_data is not None:
                st.session_state.assinatura = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                st.session_state.foto_antes = Image.open(foto_antes) if foto_antes else None
                st.session_state.foto_depois = Image.open(foto_depois) if foto_depois else None
                st.session_state.dados_pdf = {
                    "navio": navio, "pedido": pedido, "s_bb": s_bb, "s_be": s_be, 
                    "s_rem": s_rem, "total": s_bb+s_be+s_rem+pedido, "limite": limite,
                    "tempo": st.session_state.tempo_final_str,
                    "timestamp": datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
                }
                st.session_state.passo = 'RELATORIO'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#                             BLOCO 4: RELATÓRIO PDF
# #-------------------------------------------------------------------------#

elif st.session_state.passo == 'RELATORIO':
    d = st.session_state.dados_pdf
    st.markdown('<div class="box-branco">', unsafe_allow_html=True)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_text_color(0, 123, 255)
    pdf.set_font("Helvetica", 'B', 26)
    pdf.cell(0, 20, "ZION", ln=True, align='C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "Comunicado de Abastecimento", ln=True, align='C')
    
    pdf.set_font("Helvetica", size=12)
    pdf.ln(10)
    texto_corpo = (f"Comunico que o empurrador {d['navio']} está apto a receber o consumo de "
                   f"{d['pedido']:,} lts, visto que possui um saldo de {d['s_bb']:,} lts (BB) "
                   f"e {d['s_be']:,} lts (BE), somados ao saldo remanescente de {d['s_rem']:,} lts.\n\n"
                   f"Portanto, o saldo total após o abastecimento será de {d['total']:,} lts.\n"
                   f"Ressaltamos que a capacidade total do empurrador é de {d['limite']:,} lts.")
    pdf.multi_cell(0, 8, texto_corpo)
    
    h, m, s = d['tempo'].split(':')
    pdf.ln(5)
    pdf.multi_cell(0, 8, f"Informo que o empurrador levou {h} horas, {m} minutos e {s} segundos para abastecer.")

    pdf_output = pdf.output()
    st.download_button("📥 BAIXAR RELATÓRIO FINAL", data=bytes(pdf_output), file_name=f"ZION_{d['navio']}.pdf", use_container_width=True)
    if st.button("NOVO REGISTRO"): 
        st.session_state.passo = 'INICIAL'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
