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
    
    /* ESTILO USUÁRIO LOGADO TOPO DIREITO */
    .user-header { position: fixed; top: 10px; right: 10px; color: #00FF00; font-weight: bold; background: rgba(0,0,0,0.7); padding: 8px 15px; border-radius: 20px; border: 1px solid #00FF00; z-index: 999; }
    
    /* ESTILOS DAS MENSAGENS DE LOGIN */
    .msg-sucesso { color: #008000 !important; background-color: #FFFFFF !important; padding: 20px; border-radius: 10px; text-align: center; font-size: 20px !important; font-weight: bold !important; border: 3px solid #008000; margin-bottom: 20px; }
    .msg-erro { color: #FF0000 !important; background-color: #000000 !important; padding: 20px; border-radius: 10px; text-align: center; font-size: 20px !important; font-weight: bold !important; border: 3px solid #FF0000; margin-bottom: 20px; }
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

# EXIBE USUÁRIO LOGADO NO CANTO SUPERIOR DIREITO
if st.session_state.usuario_logado:
    st.markdown(f'<div class="user-header">👤 ONLINE: {st.session_state.usuario_logado}</div>', unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#            TELA 1: INICIAL (SOMENTE LOGO E BOTÃO)
# #-------------------------------------------------------------------------#
if st.session_state.pagina == "inicio":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<h1 style="color:white; text-align:center; font-size: 100px; font-weight: 900; margin-bottom: 0px;">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:white; font-size: 20px; letter-spacing: 5px;">SISTEMA DE GESTÃO NAVAL</p>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚀 INICIAR SESSÃO", use_container_width=True):
        st.session_state.pagina = "login"
        st.rerun()

# #-------------------------------------------------------------------------#
#            TELA 2: LOGIN (OS CAMPOS VOLTARAM AQUI)
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "login":
    st.markdown('<h1 style="color:white; text-align:center; font-size: 40px;">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<div class="banner-interno-verde">ACESSO AO SISTEMA</div>', unsafe_allow_html=True)
    
    with st.container():
        empurrador_login = st.selectbox("SELECIONE O EMPURRADOR", options=list(LOGINS_VALIDOS.keys()))
        user_input = st.text_input("NOME DE USUÁRIO")
        pw_input = st.text_input("SENHA DE ACESSO", type="password")
        
        if st.button("ENTRAR NO SISTEMA", use_container_width=True, type="primary"):
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
#            TELA 3: MENU CENTRAL (PÓS-LOGIN)
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "menu_central":
    st.markdown('<h1 style="color:white; text-align:center;">MENU PRINCIPAL</h1>', unsafe_allow_html=True)
    
    col_menu1, col_menu2 = st.columns(2)
    with col_menu1:
        if st.button("🏠 TELA INICIAL (SAIR)", use_container_width=True):
            st.session_state.pagina = "inicio"
            st.session_state.usuario_logado = None
            st.rerun()
        if st.button("⛽ ACOMPANHAMENTO ABASTECIMENTO", use_container_width=True):
            st.session_state.pagina = "abastecimento"
            st.rerun()
    with col_menu2:
        if st.button("📄 DADOS DA NOTA FISCAL", use_container_width=True):
            st.session_state.pagina = "nota_fiscal"
            st.rerun()
        if st.button("📊 TABELA DE CONSUMO RECEBIDA", use_container_width=True):
            st.session_state.pagina = "tabela_consumo"
            st.rerun()

# #-------------------------------------------------------------------------#
#            TELA 4: ABASTECIMENTO (SEU CÓDIGO ORIGINAL)
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "abastecimento":
    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        if st.button("⬅️ VOLTAR AO MENU"): st.session_state.pagina = "menu_central"; st.rerun()
    with col_nav2:
        if st.button("➕ NOVO ABASTECIMENTO"): reset_lancamento(); st.rerun()

    st.markdown('<h1 style="color:white; text-align:center; font-size: 40px;">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<div class="banner-interno-verde">ACOMPANHAMENTO DE ABASTECIMENTO</div>', unsafe_allow_html=True)
    
    # ... AQUI SEGUE EXATAMENTE O SEU CÓDIGO DE CAPACIDADES E PDF ...
    st.info("O restante do seu código de abastecimento está processando abaixo...")
