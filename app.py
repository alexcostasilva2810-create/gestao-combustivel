import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="ZION - Gestão Naval", layout="wide")

# ############################################################
#                    BLOCO 1: MENU
# ############################################################
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>ZION - SISTEMA DE GESTÃO NAVAL</h1>", unsafe_allow_html=True)

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    if st.button("🏠 TELA INICIAL (RESET)"):
        st.session_state.clear()
        st.rerun()
with col_menu2:
    st.button("📋 NOVO CHECKLIST")
with col_menu3:
    st.button("📄 DADOS DA NOTA FISCAL")

st.markdown("---")

# ############################################################
#              BLOCO 2: LEITOR E IDENTIFICAÇÃO
# ############################################################
st.markdown("### 📸 1. CAPTURA DE DADOS E NF-e")

col_ident1, col_ident2 = st.columns(2)

with col_ident1:
    empurrador = st.text_input("EMPURRADOR / COMANDANTE")
    operacao = st.text_input("OPERAÇÃO FLUVIAL")
    data_hoje = st.date_input("DATA", datetime.now())

with col_ident2:
    st.write("🔧 **Câmera do Sistema**")
    # Uso do componente nativo SEM redirecionamento externo
    foto_nfe = st.camera_input("Capturar Chave NF", label_visibility="collapsed")

# Bloco de Validação da Chave (Trava Automática)
chave_acesso = st.text_input("DIGITE OU COLE A CHAVE DE ACESSO (44 DÍGITOS)", max_chars=44)
chave_limpa = "".join(filter(str.isdigit, chave_acesso))

if len(chave_limpa) == 44:
    st.session_state.dados_nf = {
        "UF": "AMAZONAS - AM",
        "COMPETÊNCIA": f"{chave_limpa[4:6]}/{chave_limpa[2:4]}",
        "CNPJ": chave_limpa[6:20],
        "MOD": chave_limpa[20:22],
        "SÉRIE": chave_limpa[22:25],
        "NÚMERO": chave_limpa[25:34],
        "CHAVE": chave_limpa
    }
    st.success(f"✅ NF-e {st.session_state.dados_nf['NÚMERO']} CARREGADA!")

# ############################################################
#                BLOCO 3: CONTROLE DE TANQUES
# ############################################################
st.markdown("### ⛽ 2. VOLUMES DE ABASTECIMENTO")
df_tanques = pd.DataFrame([
    {"Nº TANQUE": "1", "PRODUTO": "DIESEL", "VOL. REMANESCENTE": 0, "VOL. A CARREGAR": 0},
    {"Nº TANQUE": "2", "PRODUTO": "DIESEL", "VOL. REMANESCENTE": 0, "VOL. A CARREGAR": 0},
])
tabela_editavel = st.data_editor(df_tanques, use_container_width=True, num_rows="dynamic")

# ############################################################
#               BLOCO 4: CHECKLIST OPERACIONAL
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
for i, p in enumerate(perguntas):
    c_p, c_r = st.columns([0.8, 0.2])
    with c_p:
        st.write(f"**{i+1}.** {p}")
    with c_r:
        respostas[p] = st.selectbox("", ["SIM", "NÃO", "N/A"], key=f"q_{i}")

# ############################################################
#                BLOCO 5: FINALIZAÇÃO E PDF
# ############################################################
st.markdown("### 🖊️ 4. CONCLUSÃO")
obs = st.text_area("OBSERVAÇÕES")

if st.button("💾 GERAR RELATÓRIO PDF"):
    if not empurrador or len(chave_limpa) != 44:
        st.error("Preencha o Empurrador e a Chave da NF!")
    else:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "CHECK LIST DE ABASTECIMENTO - ZION", ln=True, align='C')
        pdf.set_font("Arial", size=10)
        pdf.ln(5)
        pdf.cell(190, 7, f"EMPURRADOR: {empurrador}", ln=True)
        pdf.cell(190, 7, f"DATA: {data_hoje} | NF: {chave_limpa}", ln=True)
        
        pdf.ln(5)
        for p, r in respostas.items():
            pdf.cell(190, 6, f"- {p}: {r}", ln=True)
            
        nome_pdf = f"Checklist_{empurrador}.pdf"
        pdf.output(nome_pdf)
        with open(nome_pdf, "rb") as f:
            st.download_button("📥 Baixar PDF", f, file_name=nome_pdf)
        st.success("PDF Gerado!")
