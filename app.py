import streamlit as st
from datetime import date
import pandas as pd
from fpdf import FPDF # Biblioteca para gerar o PDF
import base64

# --- FUNÇÃO PARA GERAR O PDF DOS DADOS EXTRAÍDOS ---
def gerar_pdf_conferencia(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="ZION TECNOLOGIA - Relatório de Captação NF", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    for chave, valor in dados.items():
        pdf.cell(200, 10, txt=f"{chave}: {valor}", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- NOVO BLOCO: CAPTURA E PROCESSAMENTO DA CHAVE ---
st.markdown("---")
st.markdown('<p class="texto-verde">🔍 Validador de Chave e Extração Automática</p>', unsafe_allow_html=True)

# Campo que recebe a chave (vinda da câmera ou digitação)
chave_detectada = st.text_input("Cole ou Escaneie a Chave aqui para extração", max_chars=44, key="chave_extracao")

if len(chave_detectada) == 44:
    st.success("✅ Chave Identificada! Extraindo dados...")
    
    # CAMPOS QUE PODEM SER PREENCHIDOS PELA CHAVE
    # Simulando a extração que a API faria
    dados_extraidos = {
        "Chave de Acesso": chave_detectada,
        "Número da NF": chave_detectada[25:34], # Posição padrão em chaves NFe
        "Série": chave_detectada[22:25],
        "CNPJ Emitente": f"{chave_detectada[6:20]}",
        "Data de Emissão": date.today().strftime("%d/%m/%Y"), #
        "Status": "Autorizada (Simulação via Portal)"
    }
    
    # Exibição dos campos preenchidos automaticamente em azul
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Nº NF:** {dados_extraidos['Número da NF']}")
        st.info(f"**Série:** {dados_extraidos['Série']}")
    with col2:
        st.info(f"**Emitente:** {dados_extraidos['CNPJ Emitente']}")
        st.info(f"**Data:** {dados_extraidos['Data de Emissão']}")

    # BOTÃO PARA EXPORTAR ESSES DADOS EM PDF
    pdf_bytes = gerar_pdf_conferencia(dados_extraidos)
    st.download_button(
        label="📥 EXPORTAR DADOS DA CHAVE PARA PDF",
        data=pdf_bytes,
        file_name=f"conferencia_NF_{dados_extraidos['Número da NF']}.pdf",
        mime="application/pdf"
    )
