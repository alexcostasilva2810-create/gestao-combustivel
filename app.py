import streamlit as st
from datetime import datetime, timezone, timedelta
from fpdf import FPDF
from streamlit_drawable_canvas import st_canvas
import time
from PIL import Image
import io

# #-------------------------------------------------------------------------#
#                                CONFIGURAÇÕES VISUAIS
# #-------------------------------------------------------------------------#
st.set_page_config(page_title="ZION - SISTEMA DE GESTÃO", layout="centered")

st.markdown("""
    <style>
    @keyframes blinking { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .piscando { animation: blinking 1s infinite; }
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1524522173746-f628baad3644?q=80&w=2000&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.75); z-index: -1;
    }
    label, .stMarkdown p { font-size: 16px !important; color: #FFFFFF !important; font-weight: bold !important; text-shadow: 1px 1px 3px #000; }
    .banner-interno-verde { color: #28a745; text-align: center; font-weight: 900; font-size: 24px; margin-bottom: 20px; background: rgba(255, 255, 255, 0.95); padding: 12px; border-radius: 10px; }
    
    /* MENSAGENS DE LOGIN */
    .msg-sucesso { color: #008000 !important; background-color: #FFFFFF !important; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px !important; font-weight: bold !important; border: 3px solid #008000; margin-top: 10px; }
    .msg-erro { color: #FF0000 !important; background-color: #000000 !important; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px !important; font-weight: bold !important; border: 3px solid #FF0000; margin-top: 10px; }
    
    /* USUÁRIO NO TOPO ESQUERDO - TAMANHO 25 */
    .user-header-left { position: fixed; top: 10px; left: 10px; color: #00FF00; font-weight: bold; font-size: 25px; z-index: 1000; text-shadow: 2px 2px 4px #000; }

    /* LOGO ZION DOURADA */
    .logo-zion {
        text-align: center; font-size: 85px; font-weight: 900;
        background: linear-gradient(to bottom, #cfac48, #ffecb3, #b8860b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(2px 4px 6px black); margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#                LÓGICA DE NAVEGAÇÃO E ESTADO
# #-------------------------------------------------------------------------#
if 'pagina' not in st.session_state: st.session_state.pagina = "inicio"
if 'usuario_logado' not in st.session_state: st.session_state.usuario_logado = None
if 'navio_atual' not in st.session_state: st.session_state.navio_atual = "ANGELO"
if 'form_id' not in st.session_state: st.session_state.form_id = 0
if 't_rodando' not in st.session_state: st.session_state.t_rodando = False
if 'tempo_final_str' not in st.session_state: st.session_state.tempo_final_str = "00:00:00"

LOGINS_VALIDOS = {
    "ANGELO": {"user": "ALEX", "pass": "2463"},
    "ANGICO": {"user": "angico_zion", "pass": "zion02"},
    "AROEIRA": {"user": "aroeira_zion", "pass": "zion03"},
    "BRENO": {"user": "breno_zion", "pass": "zion04"},
    "CANJERANA": {"user": "canjerana_zion", "pass": "zion05"},
    "CUMARU": {"user": "cumaru_zion", "pass": "zion06"},
    "IPE": {"user": "ipe_zion", "pass": "zion07"},
    "SAMAUMA": {"user": "samauma_zion", "pass": "zion08"},
    "JACARANDA": {"user": "jacaranda_zion", "pass": "zion09"},
    "LUIZ FELIPE": {"user": "luizf_zion", "pass": "zion10"},
    "QUARUBA": {"user": "quaruba_zion", "pass": "zion11"},
    "TIMBORANA": {"user": "timborana_zion", "pass": "zion12"},
    "JATOBA": {"user": "jatoba_zion", "pass": "zion13"},
    "CEDRO": {"user": "cedro_zion", "pass": "zion14"},
    "MOGNO": {"user": "mogno_zion", "pass": "zion15"},
    "FREIJO": {"user": "freijo_zion", "pass": "zion16"},
    "SUCUPIRA": {"user": "sucupira_zion", "pass": "zion17"}
}

def reset_lancamento():
    st.session_state.form_id += 1
    st.session_state.t_rodando = False
    st.session_state.tempo_final_str = "00:00:00"

# EXIBE USUÁRIO LOGADO NO CANTO SUPERIOR ESQUERDO
if st.session_state.usuario_logado:
    st.markdown(f'<div class="user-header-left">👤 ONLINE: {st.session_state.usuario_logado}</div>', unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#            TELA 1: LOGO ZION DOURADA E BOTÃO INICIAR
# #-------------------------------------------------------------------------#
if st.session_state.pagina == "inicio":
    st.markdown('<h1 class="logo-zion">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:white; font-size: 20px; letter-spacing: 5px;">SISTEMA DE GESTÃO NAVAL</p>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚀 INICIAR SESSÃO", use_container_width=True):
        st.session_state.pagina = "login"
        st.rerun()

# #-------------------------------------------------------------------------#
#            TELA 2: LOGIN COM CAMPOS E ALERTAS
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "login":
    st.markdown('<h1 class="logo-zion">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<div class="banner-interno-verde">ACESSO AO SISTEMA</div>', unsafe_allow_html=True)
    
    empurrador_login = st.selectbox("EMPURRADOR", options=list(LOGINS_VALIDOS.keys()))
    user_input = st.text_input("USUÁRIO")
    pw_input = st.text_input("SENHA", type="password")
    
    if st.button("ENTRAR", use_container_width=True, type="primary"):
        credenciais = LOGINS_VALIDOS.get(empurrador_login)
        if user_input == credenciais["user"] and pw_input == credenciais["pass"]:
            st.markdown(f'<div class="msg-sucesso">👍 SEJA BEM VINDO <b>{user_input}</b> ao Sistema Zion !</div>', unsafe_allow_html=True)
            st.session_state.usuario_logado = user_input
            st.session_state.navio_atual = empurrador_login
            time.sleep(2)
            st.session_state.pagina = "menu_central"
            st.rerun()
        else:
            st.markdown('<div class="msg-erro">👎 SUAS CREDENCIAS ESTÃO INCONSISTENTE ENTRE EM CONTATO PELO ZAP 91-9-9349-7079...</div>', unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#            TELA 3: MENU CENTRAL
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "menu_central":
    st.markdown('<h1 class="logo-zion">ZION</h1>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏠 TELA INICIAL (SAIR)", use_container_width=True):
            st.session_state.pagina = "inicio"; st.session_state.usuario_logado = None; st.rerun()
        if st.button("⛽ ACOMPANHAMENTO ABASTECIMENTO", use_container_width=True):
            st.session_state.pagina = "abastecimento"; st.rerun()
    with c2:
        if st.button("📄 DADOS DA NOTA FISCAL", use_container_width=True):
            st.session_state.pagina = "nota_fiscal"; st.rerun()
        if st.button("📊 TABELA DE CONSUMO RECEBIDA", use_container_width=True):
            st.session_state.pagina = "tabela_consumo"; st.rerun()

# #-------------------------------------------------------------------------#
#            TELA: DADOS DA NOTA FISCAL (COM SCANNER E BUSCA)
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "nota_fiscal":
    if st.button("⬅️ VOLTAR"): st.session_state.pagina = "menu_central"; st.rerun()
    st.markdown('<div class="banner-interno-verde">📄 DADOS DA NOTA FISCAL</div>', unsafe_allow_html=True)
    
    col_scan, col_manual = st.columns(2)
    with col_scan:
        st.markdown("### 📷 SCANNER QR CODE")
        st.camera_input("APONTE PARA O QR CODE DA NOTA")
    with col_manual:
        st.markdown("### ✍️ BUSCA MANUAL")
        chave = st.text_input("CHAVE DE ACESSO (44 DÍGITOS)")
        if st.button("🔍 BUSCAR DADOS NF", use_container_width=True):
            if len(chave) == 44: st.info("Buscando dados...")
            else: st.warning("A chave deve conter 44 dígitos.")
    
    st.markdown("---")
    st.text_input("Nº DA NOTA FISCAL")
    st.date_input("DATA DE EMISSÃO", format="DD/MM/YYYY")
    st.number_input("QUANTIDADE TOTAL (LTS)", min_value=0)
    
    if st.button("💾 SALVAR DADOS DA NOTA", use_container_width=True, type="primary"):
        st.markdown('<div class="msg-sucesso">👍 Dados da Nota Salvos com Sucesso!</div>', unsafe_allow_html=True)


# #-------------------------------------------------------------------------#
#                             BLOCO 4: RELATÓRIO E PDF
# #-------------------------------------------------------------------------#

elif st.session_state.passo == 'RELATORIO':
    d = st.session_state.dados_pdf
    st.markdown('<div class="box-branco">', unsafe_allow_html=True)
    
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho ZION
    pdf.set_text_color(0, 123, 255)
    pdf.set_font("Helvetica", 'B', 26)
    pdf.cell(0, 20, "ZION", ln=True, align='C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "Comunicado de Abastecimento", ln=True, align='C')
    
    # Texto com Normas Gramaticais
    pdf.set_font("Helvetica", size=12)
    pdf.ln(10)
    texto_corpo = (f"Comunico que o empurrador {d['navio']} está apto a receber o consumo de "
                   f"{d['pedido']:,} lts, visto que possui um saldo de {d['s_bb']:,} lts (BB) "
                   f"e {d['s_be']:,} lts (BE), somados ao saldo remanescente de {d['s_rem']:,} lts.\n\n"
                   f"Portanto, o saldo total após o abastecimento será de {d['total']:,} lts.\n"
                   f"Ressaltamos que a capacidade total do empurrador é de {d['limite']:,} lts.")
    pdf.multi_cell(0, 8, texto_corpo)
    
    # Informação de Tempo e Fotos
    h, m, s = d['tempo'].split(':')
    pdf.ln(5)
    pdf.multi_cell(0, 8, f"Informo que o empurrador levou {h} horas, {m} minutos e {s} segundos para abastecer.")
    pdf.ln(5)
    pdf.multi_cell(0, 8, "Segue abaixo as fotos do antes e depois do abastecimento:")
    
    # Inserção das Fotos
    y_fotos = pdf.get_y() + 5
    if st.session_state.foto_antes:
        buf1 = io.BytesIO()
        st.session_state.foto_antes.save(buf1, format='PNG')
        pdf.image(buf1, x=10, y=y_fotos, w=85)
    if st.session_state.foto_depois:
        buf2 = io.BytesIO()
        st.session_state.foto_depois.save(buf2, format='PNG')
        pdf.image(buf2, x=105, y=y_fotos, w=85)
    
    # Assinatura
    pdf.set_y(y_fotos + 65)
    buf_sign = io.BytesIO()
    st.session_state.assinatura.save(buf_sign, format='PNG')
    pdf.image(buf_sign, x=65, w=80)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 10, f"Assinado digitalmente em: {d['timestamp']}", ln=True, align='C')

    pdf_output = pdf.output()
    st.download_button("📥 BAIXAR COMUNICADO FINAL (PDF)", data=bytes(pdf_output), file_name=f"ZION_{d['navio']}.pdf", use_container_width=True)
    if st.button("REALIZAR NOVO REGISTRO"): 
        st.session_state.passo = 'INICIAL'
        st.session_state.tempo_final_str = "00:00:00"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
