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

st.markdown("""
    <style>
    .stApp { background-image: url("app/static/plataforma.jpg"); background-size: cover; }
    .stApp::before { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: -1; }
    .box-branco { background-color: white; padding: 25px; border-radius: 15px; border: 1px solid #ddd; }
    
    /* Estilo para o texto verde DENTRO da caixa branca */
    .banner-interno-verde {
        background-color: white;
        color: #28a745;
        text-align: center;
        font-weight: bold;
        font-size: 22px;
        padding: 10px;
        border: 2px solid #eee;
        border-radius: 10px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }
    
    .alerta-erro { background-color: #ff4b4b; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; }
    label { color: #007bff !important; font-weight: bold; }
    .timer-display { font-size: 28px; font-weight: bold; color: #d32f2f; text-align: center; padding: 10px; background: #f0f0f0; border-radius: 10px; border: 2px solid #007bff; }
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
    st.image("ZION.jpg", width=250) 
    st.markdown('<h1 style="color:white; text-align:center;">ZION TECNOLOGIA</h1>', unsafe_allow_html=True)
    if st.button("INICIAR REGISTRO", use_container_width=True, type="primary"):
        st.session_state.passo = 'INPUT'
        st.rerun()

# #-------------------------------------------------------------------------#
#                             BLOCO 3: INPUT E CRONÔMETRO
# #-------------------------------------------------------------------------#

elif st.session_state.passo == 'INPUT':
    # Título ZION no topo
    st.markdown('<h1 style="color:#007bff; text-align:center; margin-bottom:10px;">ZION</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="box-branco">', unsafe_allow_html=True)
        
        # O Nome verde posicionado DENTRO da área de conteúdo
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
            foto_antes = st.file_uploader("📷 Foto ANTES do Abastecimento", type=['jpg', 'png', 'jpeg'])
            
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
            
            while st.session_state.t_rodando:
                segundos = int(time.time() - st.session_state.t_inicio)
                st.session_state.tempo_final_str = time.strftime('%H:%M:%S', time.gmtime(segundos))
                placeholder_tempo.markdown(f'<div class="timer-display">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)
                time.sleep(1)
            else:
                placeholder_tempo.markdown(f'<div class="timer-display">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)

            foto_depois = st.file_uploader("📷 Foto DEPOIS do Abastecimento", type=['jpg', 'png', 'jpeg'])

        soma_total = s_bb + s_be + s_rem + pedido
        if soma_total > limite:
            st.markdown(f'<div class="alerta-erro">⚠️ EXCESSO DE {soma_total-limite:,} LTS!</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<label>ASSINATURA DIGITAL (TELA TOUCH)</label>", unsafe_allow_html=True)
        canvas_result = st_canvas(stroke_width=3, stroke_color="#000", background_color="#f8f9fa", height=150, key="canvas_v_final")

        if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
            if canvas_result.image_data is not None:
                st.session_state.assinatura = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                st.session_state.foto_antes = Image.open(foto_antes) if foto_antes else None
                st.session_state.foto_depois = Image.open(foto_depois) if foto_depois else None
                st.session_state.dados_pdf = {
                    "navio": navio, "pedido": pedido, "s_bb": s_bb, "s_be": s_be, 
                    "s_rem": s_rem, "total": soma_total, "limite": limite,
                    "tempo": st.session_state.tempo_final_str,
                    "timestamp": datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
                }
                st.session_state.passo = 'RELATORIO'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#                             BLOCO 4: RELATÓRIO FINAL
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
    
    pdf.ln(5)
    pdf.multi_cell(0, 8, "Segue abaixo as fotos do antes e depois do abastecimento:")
    y_fotos = pdf.get_y() + 5
    if st.session_state.foto_antes:
        buf1 = io.BytesIO(); st.session_state.foto_antes.save(buf1, format='PNG')
        pdf.image(buf1, x=10, y=y_fotos, w=85)
    if st.session_state.foto_depois:
        buf2 = io.BytesIO(); st.session_state.foto_depois.save(buf2, format='PNG')
        pdf.image(buf2, x=105, y=y_fotos, w=85)
    
    pdf.set_y(y_fotos + 65)
    buf_sign = io.BytesIO(); st.session_state.assinatura.save(buf_sign, format='PNG')
    pdf.image(buf_sign, x=65, w=80)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 10, f"Assinado digitalmente em: {d['timestamp']}", ln=True, align='C')

    pdf_output = pdf.output()
    st.download_button("📥 BAIXAR RELATÓRIO FINAL", data=bytes(pdf_output), file_name=f"ZION_{d['navio']}.pdf", use_container_width=True)
    if st.button("NOVO REGISTRO"): 
        st.session_state.passo = 'INICIAL'
        st.session_state.tempo_final_str = "00:00:00"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
