import streamlit as st
from datetime import date
import time

# =========================================================
# BLOCO 1: CONFIGURAÇÃO DE AMBIENTE E ESTILO (UI/UX)
# =========================================================
st.set_page_config(
    page_title="ZION TECNOLOGIA", 
    page_icon="⛽", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Estilização para dispositivos móveis e alertas coloridos
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
        background-color: rgba(0, 8, 20, 0.85); z-index: -1;
    }
    .login-box {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px; border-radius: 15px;
        border: 1px solid #007bff; backdrop-filter: blur(10px);
        text-align: center;
    }
    label { color: #007bff !important; font-weight: bold; font-size: 16px !important; }
    .alerta-erro { 
        background-color: #ff4b4b; color: white; padding: 15px; 
        border-radius: 10px; font-weight: bold; text-align: center; 
    }
    .alerta-sucesso { 
        background-color: #28a745; color: white; padding: 15px; 
        border-radius: 10px; font-weight: bold; text-align: center; 
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# BLOCO 2: BANCO DE DADOS E GESTÃO DE ESTADO
# =========================================================

# Tabela oficial de capacidades de tanques
CAPACIDADES = {
    "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
    "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
    "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
    "TIMBORANA": 19792, "JATOBA": 84000
}

# Lista de 13 usuários para governança
USUARIOS = {
    "admin": "zion01", "gestor": "zion02", "operador1": "123", "operador2": "234",
    "operador3": "345", "operador4": "456", "operador5": "567", "operador6": "678",
    "operador7": "789", "operador8": "890", "operador9": "901", "operador10": "012",
    "operador11": "111"
}

# Inicialização de variáveis de sessão para evitar tela em branco
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'user_atual' not in st.session_state: st.session_state.user_atual = ""

# =========================================================
# BLOCO 3: TELA DE ACESSO (LOGIN)
# =========================================================
if not st.session_state.autenticado:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.image("ZION.jpg", width=220) # Logo do Robô
    st.markdown('<h2 style="color:white; margin-top:10px;">Acesso Restrito</h2>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.form_submit_button("ENTRAR NO SISTEMA", use_container_width=True):
            if u in USUARIOS and USUARIOS[u] == s:
                st.session_state.autenticado = True
                st.session_state.user_atual = u
                st.rerun()
            else:
                st.error("Usuário ou Senha inválidos.")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# BLOCO 4: TELA DE REGISTRO E LÓGICA DE SEGURANÇA
# =========================================================
else:
    # Identificação do usuário logado
    st.markdown(f'<p style="color:white; text-align:right;">👤 {st.session_state.user_atual}</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Abastecimento</h2>', unsafe_allow_html=True)
    
    # Início do formulário de registro
    with st.container():
        st.markdown('<div style="background-color: white; padding: 20px; border-radius: 15px; margin-bottom:20px;">', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            navio = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys()))
            cap_max = CAPACIDADES[navio] # Puxa o limite da tabela
            st.info(f"Capacidade Tanque: {cap_max:,} lts")
            nf = st.text_input("Nº NOTA FISCAL")
        
        with col_b:
            dt = st.date_input("DATA", format="DD/MM/YYYY") #
            qtd_pedido = st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0, step=1)

        st.markdown("---")
        st.markdown('<p style="color: #007bff; font-weight: bold;">📊 Volumes Atuais (LTS)</p>', unsafe_allow_html=True)
        
        # Campos de Medição
        m1, m2, m3 = st.columns(3)
        s_bb = m1.number_input("SALDO BB", min_value=0)
        s_be = m2.number_input("SALDO BE", min_value=0)
        s_rem = m3.number_input("REMANESCENTE", min_value=0)

        # LÓGICA DE CÁLCULO SOLICITADA
        soma_total = s_bb + s_be + s_rem + qtd_pedido
        
        if soma_total > 0:
            if soma_total > cap_max:
                # Alerta Vermelho de Transbordo
                st.markdown(f'''
                    <div class="alerta-erro">
                        ⚠️ ATENÇÃO: A SOMA REMANESCENTE MAIS QUANTO FOI PEDIDO ULTRAPASSA A CAPACIDADE DO TANQUE!<br>
                        Volume Calculado: {soma_total:,} lts
                    </div>
                ''', unsafe_allow_html=True)
            else:
                # Alerta Verde de Segurança
                st.markdown(f'''
                    <div class="alerta-sucesso">
                        ✅ EMPURRADOR HABILITADO PARA RECEBER ODM.<br>
                        Espaço disponível confirmado.
                    </div>
                ''', unsafe_allow_html=True)

        st.write("")
        chave_nf = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
        
        if st.button("🚀 CONFERIR E SALVAR", use_container_width=True, type="primary"):
            if soma_total > cap_max:
                st.error("BLOQUEADO: O volume total excede o limite físico do navio.")
            else:
                st.success("Dados prontos para envio ao Notion!")
        
        if st.button("Sair do Sistema"):
            st.session_state.autenticado = False
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
