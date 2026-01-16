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
    /* NOME DO USUÁRIO NO CANTO SUPERIOR ESQUERDO */
    .user-header-left {
        position: fixed;
        top: 15px;
        left: 15px;
        color: #00FF00;
        font-weight: bold;
        font-size: 25px; /* Tamanho pedido */
        z-index: 9999;
        text-shadow: 2px 2px 4px #000;
    }

    /* LOGO ZION DOURADO ESTILO CUSTOMIZADO */
    .logo-zion {
        text-align: center;
        font-size: 80px;
        font-weight: 900;
        background: linear-gradient(to bottom, #cfac48, #ffecb3, #b8860b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(2px 4px 6px black);
        margin-top: 20px;
    }

    .stApp {
        background-image: url("https://images.unsplash.com/photo-1524522173746-f628baad3644?q=80&w=2000&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.75); z-index: -1;
    }
    label, .stMarkdown p { font-size: 16px !important; color: #FFFFFF !important; font-weight: bold !important; }
    .banner-interno-verde { color: #28a745; text-align: center; font-weight: 900; font-size: 24px; margin-bottom: 20px; background: rgba(255, 255, 255, 0.95); padding: 12px; border-radius: 10px; }
    
    /* MENSAGENS DE LOGIN PEDIDAS */
    .msg-sucesso { color: #008000 !important; background-color: #FFFFFF !important; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px !important; font-weight: bold !important; border: 3px solid #008000; margin-top: 10px; }
    .msg-erro { color: #FF0000 !important; background-color: #000000 !important; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px !important; font-weight: bold !important; border: 3px solid #FF0000; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#                LÓGICA DE NAVEGAÇÃO E ESTADO
# #-------------------------------------------------------------------------#
if 'pagina' not in st.session_state: st.session_state.pagina = "inicio"
if 'usuario_logado' not in st.session_state: st.session_state.usuario_logado = None
if 'navio_atual' not in st.session_state: st.session_state.navio_atual = "ANGELO"
if 'form_id' not in st.session_state: st.session_state.form_id = 0
if 'num_nf_auto' not in st.session_state: st.session_state.num_nf_auto = ""
if 'qtd_nf_auto' not in st.session_state: st.session_state.qtd_nf_auto = 0

LOGINS_VALIDOS = {
    "ANGELO": {"user": "ALEX", "pass": "2463"},
    "ANGICO": {"user": "angico_zion", "pass": "zion02"}
    # Adicionar os outros logins aqui...
}

# EXIBE USUÁRIO NO TOPO ESQUERDO EM TODAS AS TELAS
if st.session_state.usuario_logado:
    st.markdown(f'<div class="user-header-left">👤 ONLINE: {st.session_state.usuario_logado}</div>', unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#            TELA 1: INICIAL (LOGO E START)
# #-------------------------------------------------------------------------#
if st.session_state.pagina == "inicio":
    st.markdown('<h1 class="logo-zion">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:white; letter-spacing: 5px;">SISTEMA DE GESTÃO NAVAL</p>', unsafe_allow_html=True)
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
            st.markdown('<div class="msg-erro">👎 SUAS CREDENCIAS ESTÃO INCONSISTENTE ENTRE EM CONTATO PELO ZAP 91-9-9349-7079 E DIGA QUE NÃO ESTA CONSEGUINDO ACESSA O SITEMA .</div>', unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#            TELA 3: MENU CENTRAL (4 BOTÕES)
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "menu_central":
    st.markdown('<h1 class="logo-zion">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="color:white; text-align:center;">MENU PRINCIPAL</h3>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏠 TELA INICIAL (SAIR)", use_container_width=True):
            st.session_state.pagina = "inicio"
            st.session_state.usuario_logado = None
            st.rerun()
        if st.button("⛽ ACOMPANHAMENTO ABASTECIMENTO", use_container_width=True):
            st.session_state.pagina = "abastecimento"
            st.rerun()
    with c2:
        if st.button("📄 DADOS DA NOTA FISCAL", use_container_width=True):
            st.session_state.pagina = "nota_fiscal"
            st.rerun()
        if st.button("📊 TABELA DE CONSUMO RECEBIDA", use_container_width=True):
            st.session_state.pagina = "tabela_consumo"
            st.rerun()

# #-------------------------------------------------------------------------#
#            TELA 4: DADOS DA NOTA FISCAL (LEITOR E BOTÕES)
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "nota_fiscal":
    if st.button("⬅️ VOLTAR AO MENU"): 
        st.session_state.pagina = "menu_central"
        st.rerun()
    st.markdown('<div class="banner-interno-verde">📄 DADOS DA NOTA FISCAL</div>', unsafe_allow_html=True)
    
    col_scan1, col_scan2 = st.columns(2)
    with col_scan1:
        st.markdown("### 📷 LEITOR DE NOTA FISCAL")
        st.camera_input("APONTE PARA O QR CODE DA NOTA")
    with col_scan2:
        st.markdown("### ✍️ ENTRADA MANUAL")
        chave_acesso = st.text_input("CHAVE DE ACESSO (44 DÍGITOS)")
        if st.button("🔍 BUSCAR DADOS DA NOTA", use_container_width=True):
            if len(chave_acesso) == 44:
                st.session_state.num_nf_auto = "987654" # Exemplo
                st.session_state.qtd_nf_auto = 20000   # Exemplo
                st.info("Dados da nota localizados!")
            else:
                st.warning("Chave inválida!")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("NÚMERO DA NOTA FISCAL", value=st.session_state.num_nf_auto)
        st.date_input("DATA DE EMISSÃO", format="DD/MM/YYYY")
    with c2:
        st.number_input("QUANTIDADE TOTAL DA NOTA (LTS)", value=st.session_state.qtd_nf_auto)
        st.text_input("FORNECEDOR")
    
    if st.button("💾 SALVAR DADOS DA NOTA", use_container_width=True, type="primary"):
        st.markdown('<div class="msg-sucesso">👍 Dados da Nota Salvos com Sucesso!</div>', unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#            TELA 5: ABASTECIMENTO (INTEGRIDADE TOTAL)
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "abastecimento":
    if st.button("⬅️ VOLTAR AO MENU"): st.session_state.pagina = "menu_central"; st.rerun()
    st.markdown('<h1 class="logo-zion">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<div class="banner-interno-verde">ACOMPANHAMENTO DE ABASTECIMENTO</div>', unsafe_allow_html=True)
    st.info("Seu sistema de cálculo de litros e PDF continua aqui abaixo...")
    # Aqui entra o bloco do seu código que calcula o transbordo e gera o PDF
