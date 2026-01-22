import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

# Configuração da Página
st.set_page_config(page_title="ZION - Gestão Naval", layout="wide")

# ############################################################
#                    BLOCO 1: MENU E CABEÇALHO
# ############################################################
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>ZION - SISTEMA DE GESTÃO NAVAL</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>CHECK LIST DE ABASTECIMENTO DE EMPURRADOR</h4>", unsafe_allow_html=True)

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    if st.button("🏠 TELA INICIAL"):
        st.session_state.clear()
        st.rerun()
with col_m2: st.button("📋 NOVO CHECKLIST")
with col_m3: st.button("📄 HISTÓRICO")

# ############################################################
#              BLOCO 2: IDENTIFICAÇÃO E NF-e
# ############################################################
st.markdown("---")
col_id1, col_id2 = st.columns(2)
with col_id1:
    empurrador = st.text_input("EMPURRADOR / COMANDANTE")
    operacao = st.text_input("OPERAÇÃO FLUVIAL")
with col_id2:
    data_insp = st.date_input("DATA", datetime.now())
    # Câmera para capturar a imagem da NF (resolvendo o problema de acesso direto)
    foto_nfe = st.camera_input("SCANNER NF-e")

chave_acesso = st.text_input("CHAVE DE ACESSO (44 DÍGITOS)", max_chars=44)
if len(chave_acesso) == 44:
    st.success("✅ NOTA FISCAL IDENTIFICADA")

# ############################################################
#               BLOCO 3: TABELA DE VOLUMES
# ############################################################
st.markdown("### ⛽ VOLUMES (TANQUES)")
df_init = pd.DataFrame([
    {"Nº TANQUE": "1", "PRODUTO": "DIESEL", "VOL. REMANESCENTE": 0, "VOL. A CARREGAR": 0, "VOLUME TOTAL": 0},
    {"Nº TANQUE": "2", "PRODUTO": "DIESEL", "VOL. REMANESCENTE": 0, "VOL. A CARREGAR": 0, "VOLUME TOTAL": 0}
])
tabela_vols = st.data_editor(df_init, use_container_width=True, num_rows="dynamic")

# ############################################################
#               BLOCO 4: CHECKLIST OPERACIONAL
# ############################################################
st.markdown("### 📋 LISTA DE VERIFICAÇÃO")
perguntas = [
    "O empurrador está amarrado com segurança?",
    "Há meio seguro de acesso a BT e fuga em caso de emergência?",
    "Existe serviço de vigilância no convés para detecção de vazamentos?",
    "A cozinha foi avisada da operação? Fogões desligados?",
    "O CT foi aterrado?",
    "Os mangotes de abastecimento estão em boas condições?"
]
respostas = {}
for i, p in enumerate(perguntas):
    c_p, c_r = st.columns([0.8, 0.2])
    respostas[p] = c_r.selectbox(f"item_{i}", ["SIM", "NÃO", "N/A"], key=f"q{i}", label_visibility="collapsed")
    c_p.write(f"{i+1}. {p}")

# ############################################################
#            BLOCO 5: DECLARAÇÃO E ASSINATURAS (NOVO)
# ############################################################
st.markdown("---")
st.markdown("### 📜 DECLARAÇÃO DE CONFORMIDADE")
texto_declaracao = """Verificou-se, onde apropriado conjuntamente, os itens da Lista de Verificação anexa... 
Os lançamentos realizados no registro da qualidade que segue, RQ 048, foram conferidos e estão em conformidade 
com as diretrizes de segurança da Transdourada Navegação Ltda."""
st.info(texto_declaracao)

st.markdown("#### ✍️ ASSINATURAS DIGITAIS")
col_ass1, col_ass2 = st.columns(2)

with col_ass1:
    st.write("TRANSDOURADA NAVEGAÇÃO")
    canvas_trans = st_canvas(fill_color="#eee", stroke_width=2, stroke_color="#000", background_color="#fff", height=100, key="ass1")

with col_ass2:
    st.write("MOTORISTA DO CT")
    canvas_mot = st_canvas(fill_color="#eee", stroke_width=2, stroke_color="#000", background_color="#fff", height=100, key="ass2")

# ############################################################
#                BLOCO 6: GERAÇÃO DO PDF COMPLETO
# ############################################################
if st.button("💾 FINALIZAR E GERAR PDF COM DECLARAÇÃO"):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, "CHECK LIST DE ABASTECIMENTO DE EMPURRADOR", ln=True, align='C')
    
    # Dados NF
    pdf.set_font("Arial", size=10)
    pdf.cell(190, 8, f"EMPURRADOR: {empurrador} | DATA: {data_insp}", ln=True)
    pdf.cell(190, 8, f"CHAVE NF: {chave_acesso}", ln=True)
    pdf.ln(5)

    # Checklist
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 8, "LISTA DE VERIFICAÇÃO:", ln=True)
    pdf.set_font("Arial", size=9)
    for p, r in respostas.items():
        pdf.cell(190, 6, f"- {p}: {r}", ln=True)
    
    pdf.ln(10)
    
    # Parte Inferior: Declaração de Conformidade
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 10, "DECLARAÇÃO DE CONFORMIDADE", ln=True, align='C')
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(190, 5, texto_declaracao)
    
    pdf.ln(20)
    
    # Linhas de Assinatura
    y_ass = pdf.get_y()
    pdf.line(10, y_ass, 90, y_ass) # Linha esquerda
    pdf.line(110, y_ass, 190, y_ass) # Linha direita
    pdf.set_y(y_ass + 2)
    pdf.cell(90, 5, "TRANSDOURADA NAVEGAÇÃO LTDA", align='C')
    pdf.cell(10, 5, "")
    pdf.cell(90, 5, "MOTORISTA DO CT", align='C')

    nome_arquivo = f"Checklist_{empurrador}.pdf"
    pdf.output(nome_arquivo)
    
    with open(nome_arquivo, "rb") as f:
        st.download_button("📥 BAIXAR DOCUMENTO COMPLETO", f, file_name=nome_arquivo)
