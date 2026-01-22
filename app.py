import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="ZION - Gestão Naval", layout="wide")

# ############################################################
#                    ESTILIZAÇÃO (CSS)
# ############################################################
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stHeader { background-color: #1E3A8A; color: white; padding: 20px; border-radius: 10px; }
    div[data-testid="stExpander"] { border: 1px solid #1E3A8A; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ############################################################
#                          MENU 
# ############################################################
st.markdown("<div class='stHeader'><h1 style='text-align:center;'>ZION - GESTÃO NAVAL</h1></div>", unsafe_allow_html=True)
st.write("")

col_menu1, col_menu2, col_menu3 = st.columns(3)
with col_menu1:
    if st.button("🏠 TELA INICIAL"):
        st.session_state.clear()
        st.rerun()
with col_menu2:
    st.button("📋 NOVO CHECKLIST")
with col_menu3:
    st.button("📊 HISTÓRICO")

# ############################################################
#                IDENTIFICAÇÃO E LEITURA NF-e
# ############################################################
st.markdown("### 📝 1. IDENTIFICAÇÃO")
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        empurrador = st.text_input("EMPURRADOR / COMANDANTE")
        operacao = st.text_input("OPERAÇÃO FLUVIAL")
    with c2:
        data_insp = st.date_input("DATA DA INSPEÇÃO", datetime.now())
        # Câmera Nativa (Resolve o problema do "Allow Access")
        st.write("📸 Captura de NF-e")
        foto_nfe = st.camera_input("Scanner de NF", label_visibility="collapsed")

    # Bloco da Chave (Trava Automática)
    chave_acesso = st.text_input("CHAVE DE ACESSO (44 DÍGITOS)", max_chars=44)
    chave_limpa = "".join(filter(str.isdigit, chave_acesso))

    if len(chave_limpa) == 44:
        st.session_state.dados_nf = {
            "UF": "AMAZONAS - AM",
            "COMPETÊNCIA": f"{chave_limpa[4:6]}/{chave_limpa[2:4]}",
            "CNPJ": chave_limpa[6:20],
            "NÚMERO": chave_limpa[25:34],
            "CHAVE": chave_limpa
        }
        st.success(f"✅ NF-e {st.session_state.dados_nf['NÚMERO']} CARREGADA")

# ############################################################
#                   CONTROLE DE TANQUES
# ############################################################
st.markdown("### ⛽ 2. VOLUMES DE ABASTECIMENTO")
dados_tanques = [
    {"Nº TANQUE": 1, "PRODUTO": "DIESEL", "VOL. REMANESCENTE": 0, "VOL. A CARREGAR": 0, "TOTAL": 0},
    {"Nº TANQUE": 2, "PRODUTO": "DIESEL", "VOL. REMANESCENTE": 0, "VOL. A CARREGAR": 0, "TOTAL": 0},
    {"Nº TANQUE": 3, "PRODUTO": "DIESEL", "VOL. REMANESCENTE": 0, "VOL. A CARREGAR": 0, "TOTAL": 0}
]
df_tanques = pd.DataFrame(dados_tanques)
tabela_editavel = st.data_editor(df_tanques, use_container_width=True, num_rows="dynamic")

# ############################################################
#                  CHECKLIST OPERACIONAL
# ############################################################
st.markdown("### 📋 3. LISTA DE VERIFICAÇÃO")
perguntas = [
    "O empurrador está amarrado com segurança?",
    "HÁ meio seguro de acesso a BT e fuga em caso de emergência?",
    "Existe serviço de vigilância no convés para detecção de vazamentos?",
    "A cozinha foi avisada da operação? Fogões desligados?",
    "O CT foi aterrado?",
    "Os mangotes de abastecimento estão em boas condições?",
    "Há espaço no tanque do empurrador para receber todo o produto?"
]

respostas = {}
for i, pergunta in enumerate(perguntas):
    col_perg, col_resp = st.columns([0.8, 0.2])
    with col_perg:
        st.write(f"**{i+1}.** {pergunta}")
    with col_resp:
        respostas[pergunta] = st.selectbox("", ["SIM", "NÃO", "N/A"], key=f"check_{i}")

# ############################################################
#                OBSERVAÇÕES E GERAÇÃO DE PDF
# ############################################################
st.markdown("### 🖊️ 4. FINALIZAÇÃO")
obs = st.text_area("OBSERVAÇÕES / AÇÕES DE CORREÇÃO")

if st.button("💾 GERAR E SALVAR RELATÓRIO FINAL"):
    if not empurrador or len(chave_limpa) != 44:
        st.error("ERRO: Preencha o nome do Empurrador e a Chave da NF-e (44 dígitos).")
    else:
        # Criação do PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "CHECK LIST DE ABASTECIMENTO DE EMPURRADOR", ln=True, align='C')
        
        pdf.set_font("Arial", size=10)
        pdf.ln(5)
        pdf.cell(95, 8, f"EMPURRADOR: {empurrador}")
        pdf.cell(95, 8, f"DATA: {data_insp}", ln=True)
        pdf.cell(190, 8, f"CHAVE NF: {chave_limpa}", ln=True)
        
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(190, 8, "ITENS VERIFICADOS:", ln=True)
        pdf.set_font("Arial", size=9)
        for p, r in respostas.items():
            pdf.cell(190, 6, f"- {p}: {r}", ln=True)
            
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(190, 8, "OBSERVAÇÕES:", ln=True)
        pdf.set_font("Arial", size=9)
        pdf.multi_cell(190, 6, obs if obs else "Nenhuma observação registrada.")

        nome_pdf = f"Checklist_{empurrador}.pdf".replace(" ", "_")
        pdf.output(nome_pdf)
        
        with open(nome_pdf, "rb") as f:
            st.download_button("📥 BAIXAR CHECKLIST (PDF)", f, file_name=nome_pdf)
        st.success("RELATÓRIO GERADO COM SUCESSO!")
