import streamlit as st
import time
from datetime import date
from fpdf import FPDF  # Biblioteca para gerar o PDF

# =========================================================
# BLOCO 1: CONFIGURAÇÕES E BANCO DE DADOS
# =========================================================
st.set_page_config(page_title="ZION TECNOLOGIA", layout="centered")

# Estilos Visuais
st.markdown("""
    <style>
    .stApp { background-image: url("app/static/plataforma.jpg"); background-size: cover; }
    .stApp::before { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: -1; }
    .box-branco { background-color: white; padding: 25px; border-radius: 15px; border: 1px solid #ddd; }
    .alerta-erro { background-color: #ff4b4b; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; }
    .alerta-sucesso { background-color: #28a745; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; }
    label { color: #007bff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Tabela de Capacidades Oficiais
CAPACIDADES = {
    "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
    "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
    "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
    "TIMBORANA": 19792, "JATOBA": 84000
}

# Gerenciador de Estados (Evita tela em branco)
if 'passo' not in st.session_state: st.session_state.passo = 'INICIAL'

# =========================================================
# BLOCO 2: TELA INICIAL
# =========================================================
if st.session_state.passo == 'INICIAL':
    st.image("ZION.jpg", width=250) #
    st.markdown('<h1 style="color:white; text-align:center;">ZION TECNOLOGIA</h1>', unsafe_allow_html=True)
    if st.button("INICIAR REGISTRO", use_container_width=True, type="primary"):
        st.session_state.passo = 'INPUT'
        st.rerun()

# =========================================================
# BLOCO 3: INPUT DE DADOS E LÓGICA DE SOMA
# =========================================================
elif st.session_state.passo == 'INPUT':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Abastecimento</h2>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="box-branco">', unsafe_allow_html=True)
        
        navio = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys())) #
        limite = CAPACIDADES[navio]
        st.info(f"Capacidade do Tanque: {limite:,} lts")
        
        col1, col2 = st.columns(2)
        with col1:
            dt = st.date_input("DATA", format="DD/MM/YYYY")
            s_bb = st.number_input("SALDO BB (LTS)", min_value=0)
            s_rem = st.number_input("REMANESCENTE (LTS)", min_value=0)
        with col2:
            pedido = st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0)
            s_be = st.number_input("SALDO BE (LTS)", min_value=0)

        # Lógica de Cálculo
        soma_total = s_bb + s_be + s_rem + pedido
        
        if soma_total > 0:
            if soma_total > limite:
                excesso = soma_total - limite
                st.markdown(f'<div class="alerta-erro">⚠️ ATENÇÃO A SOMA ULTRAPASSA A CAPACIDADE! <br> Excesso: {excesso:,} lts | CONTATE PCO/SUPRIMENTOS.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alerta-sucesso">✅ EMPURRADOR HABILITADO PARA RECEBER ODM.</div>', unsafe_allow_html=True)
                st.write(f"Volume Total Calculado: **{soma_total:,} lts**")

        if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
            st.session_state.dados_pdf = {
                "navio": navio, "pedido": pedido, "s_bb": s_bb, "s_be": s_be, 
                "s_rem": s_rem, "total": soma_total, "limite": limite, "data": dt
            }
            st.session_state.passo = 'RELATORIO'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# BLOCO 4: RELATÓRIO E GERADOR DE PDF
# =========================================================
elif st.session_state.passo == 'RELATORIO':
    d = st.session_state.dados_pdf
    st.markdown('<h2 style="color:white; text-align:center;">📄 Comunicado de Abastecimento</h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="box-branco">', unsafe_allow_html=True)
        
        texto_corpo = f"""
        Comunico que o empurrador {d['navio']} está apto a receber o consumo de ({d['pedido']:,} lts) 
        devido ter o Saldo de ({d['s_bb']:,} lts BB) e saldo de ({d['s_be']:,} lts BE) 
        mais o saldo Remanescente de ({d['s_rem']:,} lts).

        Portanto o saldo total após o abastecimento é de ({d['total']:,} lts).
        A Capacidade do Empurrador é ({d['limite']:,} lts).
        """
        st.write(texto_corpo)

        # Função para criar o PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Comunicado de Abastecimento", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        pdf.multi_cell(0, 10, texto_corpo.replace('**', ''))
        
        pdf_output = pdf.output(dest='S').encode('latin-1')

        st.download_button(label="📥 BAIXAR RELATÓRIO EM PDF", data=pdf_output, 
                           file_name=f"Comunicado_{d['navio']}.pdf", mime="application/pdf", use_container_width=True)

        if st.button("FINALIZAR E REINICIAR", use_container_width=True):
            st.session_state.passo = 'INICIAL'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
