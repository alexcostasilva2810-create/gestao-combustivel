import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="ZION - Gestão Naval", layout="wide")

# Inicialização de estados
if 'dados_nf' not in st.session_state:
    st.session_state.dados_nf = None

# --- CABEÇALHO ESTILIZADO ---
st.markdown("""
    <div style='background-color: #1E3A8A; padding: 20px; border-radius: 10px; margin-bottom: 20px'>
        <h1 style='color: white; text-align: center; margin: 0;'>ZION - SISTEMA DE GESTÃO NAVAL</h1>
        <p style='color: white; text-align: center; margin: 0;'>CHECK LIST DE ABASTECIMENTO DE EMPURRADOR</p>
    </div>
    """, unsafe_allow_html=True)

# --- SEÇÃO 1: IDENTIFICAÇÃO E NOTA FISCAL ---
with st.expander("📝 IDENTIFICAÇÃO E NF-e", expanded=True):
    col_a, col_b = st.columns(2)
    with col_a:
        empurrador = st.text_input("EMPURRADOR/COMANDANTE")
        operacao = st.text_input("OPERAÇÃO FLUVIAL")
    with col_b:
        data_atual = st.date_input("DATA", datetime.now())
        # Captura de QR Code/Barcode simplificada via Input de Câmera nativo
        foto_nfe = st.camera_input("ESCANEIE A CHAVE DA NF (OU TIRE FOTO)")

    chave_acesso = st.text_input("CHAVE DE ACESSO (44 DÍGITOS)", max_chars=44)
    
    if len(chave_acesso) == 44:
        st.success(f"✅ NF-e {chave_acesso[25:34]} DETECTADA")
        st.session_state.dados_nf = {
            "UF": "AMAZONAS",
            "CNPJ": chave_acesso[6:20],
            "NUMERO": chave_acesso[25:34],
            "CHAVE": chave_acesso
        }

# --- SEÇÃO 2: TABELA DE VOLUMES ---
st.markdown("### ⛽ CONTROLE DE CARGA")
df_volumes = pd.DataFrame([
    {"Nº TANQUE": "1", "PRODUTO": "DIESEL", "VOL. REMANESCENTE": 0, "VOL. A CARREGAR": 0},
    {"Nº TANQUE": "2", "PRODUTO": "DIESEL", "VOL. REMANESCENTE": 0, "VOL. A CARREGAR": 0}
])
edited_df = st.data_editor(df_volumes, num_rows="dynamic", use_container_width=True)

# --- SEÇÃO 3: CHECKLIST OPERACIONAL ---
st.markdown("### 📋 ITENS DE VERIFICAÇÃO")
perguntas = [
    "O empurrador está amarrado com segurança?",
    "HÁ meio seguro de acesso a BT e fuga em caso de emergência?",
    "Existe serviço de vigilância no convés para detecção de vazamentos?",
    "A cozinha foi avisada da operação? Fogões desligados?",
    "O CT foi aterrado?",
    "Os mangotes de abastecimento estão em boas condições?"
]

respostas = {}
for i, pergunta in enumerate(perguntas):
    col_p, col_r = st.columns([0.8, 0.2])
    with col_p:
        st.write(f"{i+1}. {pergunta}")
    with col_r:
        respostas[pergunta] = st.radio(f"Opção {i}", ["SIM", "NÃO"], key=f"p_{i}", label_visibility="collapsed")

# --- SEÇÃO 4: CONCLUSÃO E PDF ---
st.markdown("---")
observacao = st.text_area("OBSERVAÇÃO / AÇÃO DE CORREÇÃO")

if st.button("🚀 FINALIZAR E GERAR RELATÓRIO PDF", use_container_width=True):
    if not empurrador:
        st.error("Por favor, preencha o nome do Empurrador.")
    else:
        # Geração do PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, "CHECKLIST DE ABASTECIMENTO - ZION", ln=True, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(100, 10, f"EMPURRADOR: {empurrador}")
        pdf.cell(90, 10, f"DATA: {data_atual}", ln=True)
        
        if st.session_state.dados_nf:
            pdf.cell(190, 10, f"NF-e: {st.session_state.dados_nf['NUMERO']} | CHAVE: {st.session_state.dados_nf['CHAVE']}", ln=True)
        
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(190, 10, "RESULTADO DO CHECKLIST:", ln=True)
        pdf.set_font("Arial", size=10)
        for p, r in respostas.items():
            pdf.cell(190, 7, f"- {p}: {r}", ln=True)
            
        nome_arq = f"Checklist_{empurrador}_{data_atual}.pdf"
        pdf.output(nome_arq)
        
        with open(nome_arq, "rb") as f:
            st.download_button("📥 BAIXAR RELATÓRIO FINAL", f, file_name=nome_arq)
        st.success("Relatório gerado com sucesso!")

st.caption("Sistema Zion - v2.0 | Desenvolvido para Gestão Naval")
