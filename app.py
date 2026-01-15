import streamlit as st
from datetime import date
import time

# Configurações de Identidade Visual
st.set_page_config(page_title="ZION TECNOLOGIA", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-image: url("app/static/plataforma.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 8, 20, 0.7); z-index: -1;
    }
    .alerta-erro { background-color: #ff4b4b; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; }
    .alerta-sucesso { background-color: #28a745; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; }
    label { color: #007bff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Tabela de Capacidades (Referência: image_dba3a6.png)
CAPACIDADES = {
    "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
    "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
    "JACARANDA": 19792, "LUIZ FELLIPE": 25000, "QUARUBA": 19792,
    "TIMBORANA": 19792, "JATOBA": 84000
}

# 13 Usuários Autorizados
USUARIOS = {"admin": "zion01", "gestor": "zion02", "usuario1": "123"} # Complete com os demais

# Inicialização de Estados para evitar KeyError
if 'tela' not in st.session_state: st.session_state.tela = 'home'
if 'autenticado' not in st.session_state: st.session_state.autenticado = False

if st.session_state.tela == 'home':
    st.image("ZION.jpg", width=300) #
    st.markdown('<h1 style="color:white; text-align:center;">ZION TECNOLOGIA</h1>', unsafe_allow_html=True)
    if st.button("INICIAR REGISTRO", use_container_width=True, type="primary"):
        st.session_state.tela = 'login'
        st.rerun()

elif st.session_state.tela == 'login':
    with st.form("login_form"):
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.form_submit_button("ACESSAR"):
            if u in USUARIOS and USUARIOS[u] == s:
                st.session_state.autenticado = True
                st.session_state.tela = 'registro'
                st.rerun()
            else: st.error("Acesso Negado")
elif st.session_state.tela == 'registro' and st.session_state.autenticado:
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div style="background-color: white; padding: 25px; border-radius: 15px;">', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            # Filtro por Empurrador
            emp = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys())) #
            cap_max = CAPACIDADES[emp] #
            st.info(f"Atenção: este empurrador só pode receber {cap_max:,} lts conforme a tabela.") #
            nf = st.text_input("Nº NOTA FISCAL")
        
        with c2:
            dt = st.date_input("DATA", format="DD/MM/YYYY") #
            qtd_nf = st.number_input("QUANTIDADE (LTS) NA NOTA", min_value=0)
            remanescente = st.number_input("VOLUME REMANESCENTE NO TANQUE (LTS)", min_value=0)

        # LÓGICA DE VALIDAÇÃO (Melhoria Solicitada)
        total_previsto = qtd_nf + remanescente #
        
        st.markdown("---")
        if total_previsto > 0:
            if total_previsto <= cap_max:
                st.markdown('<div class="alerta-sucesso">✅ EMPURRADOR COM CAPACIDADE PARA RECEBER COMBUSTÍVEL</div>', unsafe_allow_html=True) #
            else:
                st.markdown(f'<div class="alerta-erro">⚠️ PROCURE SEU GESTOR PARA REPORTAR QUE NÃO DÁ PARA RECEBER. (Total: {total_previsto:,} > Limite: {cap_max:,})</div>', unsafe_allow_html=True)

        if st.button("CONFERIR REGISTRO", use_container_width=True):
            if total_previsto <= cap_max:
                st.success("Dados validados!")
                # Aqui você seguiria para o bloco de salvamento
        st.markdown('</div>', unsafe_allow_html=True)


