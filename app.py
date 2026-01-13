import streamlit as st
from datetime import date
import pandas as pd
import time
import requests #

# --- 1. CONFIGURAÇÃO E ESTILO COM SUAS IMAGENS ---
st.set_page_config(page_title="ZION - Gestão PRO", page_icon="⛽", layout="centered")

# CSS para carregar plataforma.jpg como fundo
st.markdown("""
    <style>
    .stApp {
        background-image: url("app/static/plataforma.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 31, 63, 0.85); /* Overlay azul marinho */
        z-index: -1;
    }
    .login-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 40px;
        border-radius: 20px;
        border: 2px solid #007bff;
        backdrop-filter: blur(15px);
        text-align: center;
    }
    label, .stWidgetLabel p { color: #007bff !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO SEGURA DO ESTADO (EVITA KEYERROR) ---
#
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tela' not in st.session_state: st.session_state.tela = 'registro'
if 'dados_nf' not in st.session_state: st.session_state.dados_nf = {}

# --- 3. GOVERNANÇA (13 USUÁRIOS) ---
USUARIOS = {
    "admin": "zion01", "gestor": "zion02", "usuario1": "123", "usuario2": "234",
    "usuario3": "345", "usuario4": "456", "usuario5": "567", "usuario6": "678",
    "usuario7": "789", "usuario8": "890", "usuario9": "901", "usuario10": "012",
    "usuario11": "124"
}

# --- 4. TELA DE LOGIN COM ZION.jpg ---
if not st.session_state.autenticado:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    try:
        st.image("ZION.jpg", width=200) #
    except:
        st.markdown('<h1 style="color:white;">ZION</h1>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        # O uso de form_submit_button previne o erro de 'Missing Submit Button'
        if st.form_submit_button("ACESSAR SISTEMA"):
            if u in USUARIOS and USUARIOS[u] == s:
                st.session_state.autenticado = True
                st.session_state.user_logado = u
                st.rerun()
            else:
                st.error("Credenciais Inválidas")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 5. TELA DE REGISTRO (DATA CORRIGIDA) ---
if st.session_state.tela == 'registro':
    st.markdown(f'<p style="color:white; text-align:right;">Sessão: {st.session_state.user_logado}</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("registro_form"):
        col1, col2 = st.columns(2)
        with col1:
            emp = st.selectbox("EMPURRADOR", options=["JACARANDA", "CUMARU", "SAMAUMA", "JATOBA", "TIMBORANA", "ANGELO", "QUARUBA", "BRENO", "CANJERANA", "IPE", "LUIZ FELLIPE", "AROEIRA", "ANGICO"])
            nf_num = st.text_input("Nº DA NOTA")
        with col2:
            # Data forçada para o formato brasileiro
            dt = st.date_input("DATA", value=date.today(), format="DD/MM/YYYY") 
            qtd_real = st.number_input("QUANTIDADE (LTS)", step=1)

        st.write("---")
        st.markdown('<p style="color:#00FF00; font-weight:bold;">📸 Tanques e Chave</p>', unsafe_allow_html=True)
        chave_nf = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        t_bb = st.number_input("TANQUE BB (m³)", step=0.01)
        t_be = st.number_input("TANQUE BE (m³)", step=0.01)

        if st.form_submit_button("CONFERIR DADOS"):
            # Salvando no session_state para evitar KeyError na próxima tela
            st.session_state.dados_nf = {
                "emp": emp, "nf": nf_num, "dt": dt, 
                "qtd": qtd_real, "chave": chave_nf, 
                "t_bb": t_bb, "t_be": t_be
            }
            st.session_state.tela = 'edicao'
            st.rerun()

# --- 6. TELA DE CONFERÊNCIA (ESTÁVEL) ---
elif st.session_state.tela == 'edicao':
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    
    # Verificação de segurança para evitar KeyError se os dados sumirem
    if not st.session_state.dados_nf:
        st.warning("Dados não encontrados. Retorne ao início.")
        if st.button("VOLTAR"):
            st.session_state.tela = 'registro'
            st.rerun()
        st.stop()

    d = st.session_state.dados_nf
    with st.form("conferencia_form"):
        # Exibição conferida dos dados salvos
        st.write(f"**Empurrador:** {d['emp']} | **Nota:** {d['nf']}")
        st.write(f"**Realizado:** {d['qtd']} LTS | **Data:** {d['dt'].strftime('%d/%m/%Y')}")
        
        st.write("---")
        if st.form_submit_button("✅ SALVAR NO NOTION"):
            # Aqui entraria a função enviar_ao_notion(d)
            st.success("SIMULAÇÃO: DADOS SALVOS!")
            time.sleep(1)
            st.session_state.tela = 'registro'
            st.rerun()

    if st.button("🔄 CORRIGIR"):
        st.session_state.tela = 'registro'
        st.rerun()
