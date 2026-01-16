import streamlit as st
from datetime import datetime
from fpdf import FPDF
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

# #-------------------------------------------------------------------------#
#                             BLOCO 1: CONFIGURAÇÕES
# #-------------------------------------------------------------------------#

st.set_page_config(page_title="ZION TECNOLOGIA", layout="centered")

st.markdown("""
    <style>
    .stApp { background-image: url("app/static/plataforma.jpg"); background-size: cover; }
    .stApp::before { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: -1; }
    .box-branco { background-color: white; padding: 25px; border-radius: 15px; }
    .alerta-erro { background-color: #ff4b4b; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; }
    .alerta-sucesso { background-color: #28a745; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; }
    label { color: #007bff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

CAPACIDADES = {
    "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
    "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
    "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
    "TIMBORANA": 19792, "JATOBA": 84000
}

if 'passo' not in st.session_state: 
    st.session_state.passo = 'INICIAL'

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
#                             BLOCO 3: INPUT DE DADOS E ASSINATURA
# #-------------------------------------------------------------------------#

elif st.session_state.passo == 'INPUT':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Abastecimento</h2>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="box-branco">', unsafe_allow_html=True)
        
        navio = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys()))
        limite = CAPACIDADES[navio]
        st.info(f"Capacidade do Tanque: {limite:,} lts")
        
        c1, c2 = st.columns(2)
        with c1:
            dt_input = st.date_input("DATA", format="DD/MM/YYYY")
            s_bb = st.number_input("SALDO BB (LTS)", min_value=0)
            s_rem = st.number_input("REMANESCENTE (LTS)", min_value=0)
        with c2:
            pedido = st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0)
            s_be = st.number_input("SALDO BE (LTS)", min_value=0)

        soma_total = s_bb + s_be + s_rem + pedido
        
        if soma_total > limite:
            st.markdown(f'<div class="alerta-erro">⚠️ ATENÇÃO: A SOMA ULTRAPASSA A CAPACIDADE! Excesso: {soma_total-limite:,} lts</div>', unsafe_allow_html=True)
        elif soma_total > 0:
            st.markdown('<div class="alerta-sucesso">✅ EMPURRADOR HABILITADO PARA RECEBER ODM.</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<label>ASSINATURA DIGITAL (TELA TOUCH)</label>", unsafe_allow_html=True)
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 1)",
            stroke_width=3,
            stroke_color="#000000",
            background_color="#f8f9fa",
            height=150,
            update_streamlit=True,
            key="canvas_assinatura",
        )

        if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
            if canvas_result.image_data is not None:
                img_res = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                st.session_state.assinatura = img_res
                st.session_state.dados_pdf = {
                    "navio": navio, "pedido": pedido, "s_bb": s_bb, "s_be": s_be, 
                    "s_rem": s_rem, "total": soma_total, "limite": limite,
                    "timestamp": datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
                }
                st.session_state.passo = 'RELATORIO'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#                             BLOCO 4: RELATÓRIO E PDF
# #-------------------------------------------------------------------------#

elif st.session_state.passo == 'RELATORIO':
    d = st.session_state.dados_pdf
    st.markdown('<h2 style="color:white; text-align:center;">📄 Documento Gerado</h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="box-branco">', unsafe_allow_html=True)
        
        # Texto com correções gramaticais aplicadas
        texto_corpo = (f"Comunico que o empurrador {d['navio']} está apto a receber o consumo de "
                       f"{d['pedido']:,} lts, visto que possui um saldo de {d['s_bb']:,} lts (BB) "
                       f"e {d['s_be']:,} lts (BE), somados ao saldo remanescente de {d['s_rem']:,} lts.\n\n"
                       f"Portanto, o saldo total após o abastecimento será de {d['total']:,} lts.\n"
                       f"Ressaltamos que a capacidade total do empurrador é de {d['limite']:,} lts.")

        # Geração do PDF Corrigida
        pdf = FPDF()
        pdf.add_page()
        
        # Cabeçalho ZION Centralizado e Azul
        pdf.set_text_color(0, 123, 255)
        pdf.set_font("Helvetica", 'B', 26)
        pdf.cell(0, 20, "ZION", ln=True, align='C')
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "Comunicado de Abastecimento", ln=True, align='C')
        
        pdf.set_font("Helvetica", size=12)
        pdf.ln(15)
        pdf.multi_cell(0, 8, texto_corpo)
        
        # Área de Assinatura com maior afastamento e linha
        if 'assinatura' in st.session_state:
            pdf.ln(30) # Afastamento do corpo do texto
            img_byte_arr = io.BytesIO()
            st.session_state.assinatura.save(img_byte_arr, format='PNG')
            
            # Centraliza a imagem da assinatura
            pdf.image(img_byte_arr, x=65, w=80)
            
            # Linha de assinatura e registro de data/hora
            pdf.set_draw_color(255, 0, 0) # Linha vermelha conforme solicitado visualmente
            pdf.line(60, pdf.get_y(), 150, pdf.get_y())
            pdf.ln(2)
            pdf.set_font("Helvetica", 'I', 10)
            pdf.cell(0, 10, f"Assinado digitalmente em: {d['timestamp']}", ln=True, align='C')

        pdf_output = pdf.output()

        st.download_button(
            label="📥 BAIXAR COMUNICADO ASSINADO (PDF)",
            data=bytes(pdf_output),
            file_name=f"Comunicado_ZION_{d['navio']}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        if st.button("REALIZAR NOVO REGISTRO"):
            st.session_state.passo = 'INICIAL'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
